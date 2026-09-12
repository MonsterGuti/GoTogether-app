from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags

from rides.models import Ride
from reviews.models import Review
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            profile, created = Profile.objects.get_or_create(user=user)

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            profile.phone_number = form.cleaned_data.get('phone_number')
            profile.car_model = form.cleaned_data.get('car_model')
            profile.facebook_url = form.cleaned_data.get('facebook_url')
            profile.instagram_url = form.cleaned_data.get('instagram_url')
            profile.save()

            login(request, user)

            if user.email:
                subject = 'Добре дошли в TakeTheTrip!'
                html_content = f"""
                <html>
                    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
                        <div style="max-width: 600px; margin: 0 auto; padding: 25px; border: 1px solid #e0e0e0; border-radius: 8px;">
                            <h2 style="color: #0d6efd; margin-top: 0;">TakeTheTrip</h2>
                            <p>Здравейте, <strong>{user.username}</strong>!</p>
                            <p>Благодарим ви, че се регистрирахте в TakeTheTrip. Сега можете да споделяте пътуванията си или да намерите удобен транспорт.</p>
                            <p>Желаем ви приятни и безаварийни пътувания!</p>
                        </div>
                    </body>
                </html>
                """
                plain_message = strip_tags(html_content)

                try:
                    send_mail(
                        subject=subject,
                        message=plain_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        html_message=html_content,
                        fail_silently=True,
                    )
                except Exception:
                    pass

            messages.success(request, 'Успешна регистрация!')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})