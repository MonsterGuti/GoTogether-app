from django.db import models
from django.contrib.auth.models import AbstractUser

from tripApp import settings


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_driver = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    car_model = models.CharField(max_length=100, blank=True, null=True)

    @property
    def display_name(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'.strip()
        return self.username


class Ride(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_rides')
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    available_seats = models.PositiveIntegerField()
    price_per_seat = models.DecimalField(max_digits=6, decimal_places=2)

    allows_smoking = models.BooleanField(default=False)
    allows_pets = models.BooleanField(default=False)
    has_big_trunk = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origin} -> {self.destination} ({self.departure_time.strftime('%Y-%m-%d %H:%M')})"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ]

    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='bookings')
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_bookings')
    seats_booked = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)


class RideMessage(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender}: {self.content[:20]}"
