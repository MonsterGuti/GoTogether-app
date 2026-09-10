from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from rides.models import Ride, Booking
from notifications.models import Notification
from .models import Review
from .forms import ReviewForm


@login_required
def add_review(request, ride_pk):
    ride = get_object_or_404(Ride, pk=ride_pk)

    if ride.driver == request.user:
        messages.error(request, "Не можете да оставите отзив за себе си.")
        return redirect('ride_detail', pk=ride_pk)

    confirmed_booking = Booking.objects.filter(
        ride=ride,
        passenger=request.user,
        status__in=['APPROVED', 'CONFIRMED', 'approved', 'confirmed']
    ).exists()

    if not confirmed_booking:
        messages.error(
            request,
            "Можете да оставяте отзив само за пътувания, в които сте участвали с потвърдено място."
        )
        return redirect('ride_detail', pk=ride_pk)

    if ride.departure_time > timezone.now():
        messages.error(
            request,
            "Можете да оставите отзив едва след като пътуването е приключило."
        )
        return redirect('ride_detail', pk=ride_pk)

    already_reviewed = Review.objects.filter(ride=ride, reviewer=request.user).exists()
    if already_reviewed:
        messages.warning(request, "Вече сте оставили отзив за това пътуване.")
        return redirect('ride_detail', pk=ride_pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ride = ride
            review.reviewer = request.user
            review.driver = ride.driver
            review.save()

            reviewer_name = request.user.get_full_name() or request.user.username
            Notification.objects.create(
                recipient=ride.driver,
                sender=request.user,
                notification_type='review',
                message=f"{reviewer_name} ви остави отзив ({review.rating} ★)."
            )

            if ride.driver.email:
                subject = f'Нов отзив от {reviewer_name} в TakeTheTrip'
                message = (
                    f'Здравейте, {ride.driver.username}!\n\n'
                    f'Получихте нов отзив за пътуването си:\n'
                    f'Оценка: {review.rating}/5 ★\n'
                    f'Коментар: "{review.comment}"\n\n'
                    f'Можете да прегледате профила си тук: {settings.SITE_URL}/users/profile/\n\n'
                    f'Поздрави,\nЕкипът на TakeTheTrip'
                )
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[ride.driver.email],
                    fail_silently=True,
                )

            messages.success(request, "Благодарим ви! Вашият отзив беше добавен успешно.")
            return redirect('ride_detail', pk=ride_pk)
    else:
        form = ReviewForm()

    return render(request, 'reviews/add_review.html', {
        'form': form,
        'ride': ride
    })