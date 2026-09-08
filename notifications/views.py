from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification


@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')

    unread_notifications = notifications.filter(is_read=False)

    response = render(
        request,
        'notifications/notifications_list.html',
        {'notifications': notifications},
    )

    unread_notifications.update(is_read=True)

    return response


@login_required
def read_and_redirect(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)

    if not notification.is_read:
        notification.is_read = True
        notification.save()

    if hasattr(notification, 'get_absolute_url') and notification.get_absolute_url():
        return redirect(notification.get_absolute_url())

    return redirect('notifications_list')


@login_required
def unread_count_api(request):
    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'unread_count': count})