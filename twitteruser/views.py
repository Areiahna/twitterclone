from django.shortcuts import render, HttpResponseRedirect, reverse
from twitteruser.models import MyUser
from django.contrib.auth.decorators import login_required
from tweet.models import Tweet
from notifications.models import Notification
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


# @login_required
# def index_views(request):
#     # RECIEVED HELP FROM PAUL R
#     my_user = MyUser.objects.filter(username=request.user.username).first()
#     follower_tweet = Tweet.objects.filter(
#         author__in=request.user.followers.all())
#     user_tweets = Tweet.objects.filter(author=request.user).all()
#     all_tweets = follower_tweet | user_tweets
#     all_tweets = all_tweets.order_by('-post_date')
#     user_notications = Notification.objects.filter(
#         tagged_user=request.user).all()
#     notifications = user_notications.count()
#     return render(request, "index.html", {"users": my_user, "tweets": all_tweets, "count": notifications})

class IndexView(LoginRequiredMixin, TemplateView):

    def get(self, request):
        # RECIEVED HELP FROM PAUL R
        my_user = MyUser.objects.filter(username=request.user.username).first()
        follower_tweet = Tweet.objects.filter(
            author__in=request.user.followers.all())
        user_tweets = Tweet.objects.filter(author=request.user).all()
        all_tweets = follower_tweet | user_tweets
        all_tweets = all_tweets.order_by('-post_date')
        user_notications = Notification.objects.filter(
            tagged_user=request.user).all()
        notifications = user_notications.count()
        return render(request, "index.html", {"users": my_user, "tweets": all_tweets, "count": notifications})


def userdetail_view(request, user_username):
    userobj = MyUser.objects.filter(username=user_username).first()
    my_user = MyUser.objects.filter(username=user_username).first()
    user_tweets = Tweet.objects.filter(author=userobj).order_by('-post_date')
    count = user_tweets.count()
    followers = my_user.followers.all()
    follower_count = followers.count()
    if follower_count == -1:
        follower_count += 1

    follow = "Follow"
    if my_user in request.user.followers.all():
        follow = "Un-Follow"

    user_notications = Notification.objects.filter(
        tagged_user=request.user).all()
    notify_count = user_notications.count()

    return render(request, "user_details.html", {"user": my_user, "tweets": user_tweets, "count": count, "follower_count": follower_count, "button_display": follow, "notify_count": notify_count})


def follow_user(request, user_username):
    follow_user = MyUser.objects.filter(
        username=user_username).first()
    my_user = MyUser.objects.filter(username=request.user.username).first()
    if follow_user in my_user.followers.all():
        my_user.followers.remove(follow_user)
        my_user.save()
    else:
        my_user.followers.add(follow_user)
        my_user.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', "/"))
