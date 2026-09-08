from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from rides.models import Ride

User = get_user_model()


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('booking', 'Нова резервация'),
        ('cancellation', 'Отказ от резервация'),
        ('chat', 'Ново съобщение'),
        ('review', 'Нов отзив'),
    )

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications'
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_notifications'
    )
    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPES
    )
    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications',
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Нотификация за {self.recipient.username}: {self.message[:30]}'

    @property
    def get_absolute_url(self):
        if self.notification_type == 'review':
            return reverse('public_profile', kwargs={'username': self.recipient.username}) + '#reviews'

        elif self.ride:
            return reverse('ride_detail', kwargs={'pk': self.ride.pk})

        return '#'