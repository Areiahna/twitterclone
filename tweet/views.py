from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from tweet.models import Tweet
from twitteruser.models import MyUser
from notifications.models import Notification
from tweet.forms import AddTweetForm
# Create your views here.


@login_required
def create_tweet(request, user_username):
    # https://stackoverflow.com/questions/9616569/django-cannot-assign-u1-staffprofile-user-must-be-a-user-instance
    if request.method == "POST":
        userobj = MyUser.objects.filter(username=user_username).first()
        form = AddTweetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_tweet = Tweet.objects.create(
                text=data.get('text'),
                author=userobj,
            )
            new_tweet.save()

            tweet_text = data['text']
            tweet_text.lower()
            split_tweet = tweet_text.split()
            for word in split_tweet:
                if "@" in word:
                    username = word[1:]
                    target_user = MyUser.objects.filter(
                        username=username).first()
                    if target_user.username.lower() == username:
                        Notification.objects.create(
                            tagged_user=target_user,
                            tweet=new_tweet
                        )

        return HttpResponseRedirect(reverse("homepage"))

    form = AddTweetForm()
    return render(request, "addtweet.html", {"form": form})


def tweetdetail_view(request, tweet_id):
    my_user = MyUser.objects.all()
    tweets = Tweet.objects.filter(id=tweet_id).first()
    return render(request, "tweet_details.html", {"tweets": tweets})
