from django.shortcuts import render, HttpResponseRedirect, reverse
from twitteruser.models import MyUser
from django.contrib.auth.decorators import login_required
from tweet.models import Tweet


@login_required
def index_views(request):
    my_user = MyUser.objects.all()
    user_tweets = Tweet.objects.all().order_by('-post_date')
    return render(request, "index.html", {"users": my_user, "tweets": user_tweets})


def userdetail_view(request, user_username):
    userobj = MyUser.objects.filter(username=user_username).first()
    my_user = MyUser.objects.filter(username=user_username).first()
    user_tweets = Tweet.objects.filter(author=userobj).order_by('-post_date')
    count = user_tweets.count()
    return render(request, "user_details.html", {"user": my_user, "tweets": user_tweets, "count": count})
