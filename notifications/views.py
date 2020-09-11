from notifications.models import Notification
from django.shortcuts import render, HttpResponseRedirect
import copy

# Create your views here.


def notification_view(request):
    user_notications = Notification.objects.filter(
        tagged_user=request.user).all()

    notications = copy.copy(user_notications)

    count = Notification.objects.filter(
        tagged_user=request.user).count()

    Notification.objects.filter(tagged_user=request.user).delete()
    count = Notification.objects.filter(
        tagged_user=request.user).count()

    return render(request, "notification_detail.html", {"notifications": notications, "count": count})


def clear_notifications(request):
    Notification.objects.filter(tagged_user=request.user).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', "/"))
