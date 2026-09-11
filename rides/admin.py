from django.contrib import admin
from .models import Ride, Booking, RideMessage, User

admin.site.register(Ride)
admin.site.register(Booking)
admin.site.register(RideMessage)
admin.site.register(User)