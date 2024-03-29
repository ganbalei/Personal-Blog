from django.urls import reverse
from notifications.models import Notification
from django.shortcuts import render, get_object_or_404,redirect

# Create your views here.
def my_notifications(request):
    context = {}
    return render(request, 'my_notifications/my_notifications.html', context)

def my_notification(request, my_notification_pk):
    my_notification = get_object_or_404(Notification, pk=my_notification_pk)
    my_notification.unread = False
    my_notification.save()
    return redirect(my_notification.data['url'])

def del_my_read_notifications(request):
    notifications = request.user.notifications.read()
    notifications.delete()
    return redirect(reverse('my_notifications'))