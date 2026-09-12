import threading
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from django.conf import settings
import os
import resend

from rides.models import Ride
from reviews.models import Review
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

User = get_user_model()

# Инициализиране на Resend API
resend.api_key = os.getenv("RESEND_API_KEY") or getattr(settings, "RESEND_API_KEY", None)

class ResendEmailThread(threading.Thread):
    def __init__(self, recipient_email, subject, html_content):
        self.recipient_email = recipient_email
        self.subject = subject
        self.html_content = html_content
        super().__init__()

    def run(self):
        try:
            params = {
                "from": "onboarding@resend.dev",
                "to": [self.recipient_email],
                "subject": self.subject,
                "html": self.html_content,
            }
            response = resend.Emails.send(params)
            print(f"--- USERS RESEND SUCCESS ---: {response}")
        except Exception as e:
            print(f"--- USERS RESEND ERROR ---: {e}")


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

                ResendEmailThread(user.email, subject, html_content).start()

            messages.success(request, f'Успешна регистрация! Добре дошли, {user.username}!')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=profile_obj
        )

        if profile_obj.avatar:
            p_form.fields['avatar'].required = False

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Профилът ви беше обновен успешно!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile_obj)
        if profile_obj.avatar:
            p_form.fields['avatar'].required = False

    driver_rides = Ride.objects.filter(driver=request.user).order_by('-departure_time')
    reviews = Review.objects.filter(driver=request.user).select_related('reviewer', 'reviewer__profile').order_by(
        '-created_at')
    avg_rating_val = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    avg_rating = round(avg_rating_val, 1)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_obj': request.user,
        'is_own_profile': True,
        'driver_rides': driver_rides,
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    return render(request, 'users/profile.html', context)


def public_profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    if request.user == profile_user:
        return redirect('profile')

    Profile.objects.get_or_create(user=profile_user)
    driver_rides = Ride.objects.filter(driver=profile_user).order_by('-departure_time')

    reviews = Review.objects.filter(driver=profile_user).select_related('reviewer', 'reviewer__profile').order_by(
        '-created_at')
    avg_rating_val = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    avg_rating = round(avg_rating_val, 1)

    context = {
        'profile_user': profile_user,
        'user_obj': profile_user,
        'is_own_profile': False,
        'driver_rides': driver_rides,
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    return render(request, 'users/profile.html', context)