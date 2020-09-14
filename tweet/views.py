from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from tweet.models import Tweet
from twitteruser.models import MyUser
from notifications.models import Notification
from tweet.forms import AddTweetForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class CreateTweet(LoginRequiredMixin, TemplateView):
    # https://stackoverflow.com/questions/9616569/django-cannot-assign-u1-staffprofile-user-must-be-a-user-instance

    def get(self, request, user_username):
        form = AddTweetForm()
        return render(request, "addtweet.html", {"form": form})

    def post(self, request, user_username):
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
                    username = word[1:].lower()
                    target_user = MyUser.objects.filter(
                        username=username).first()
                    if target_user.username.lower() == username.lower():
                        Notification.objects.create(
                            tagged_user=target_user,
                            tweet=new_tweet
                        )
                else:
                    HttpResponseRedirect(reverse("homepage"))

            return HttpResponseRedirect(reverse("homepage"))


def tweetdetail_view(request, tweet_id):
    my_user = MyUser.objects.all()
    tweets = Tweet.objects.filter(id=tweet_id).first()
    return render(request, "tweet_details.html", {"tweets": tweets})


# @login_required
# def create_tweet(request, user_username):
#     # https://stackoverflow.com/questions/9616569/django-cannot-assign-u1-staffprofile-user-must-be-a-user-instance
#     if request.method == "POST":
#         userobj = MyUser.objects.filter(username=user_username).first()
#         form = AddTweetForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             new_tweet = Tweet.objects.create(
#                 text=data.get('text'),
#                 author=userobj,
#             )
#             new_tweet.save()

#             tweet_text = data['text']
#             tweet_text.lower()
#             split_tweet = tweet_text.split()
#             for word in split_tweet:
#                 if "@" in word:
#                     username = word[1:]
#                     target_user = MyUser.objects.filter(
#                         username=username).first()
#                     if target_user.username.lower() == username:
#                         Notification.objects.create(
#                             tagged_user=target_user,
#                             tweet=new_tweet
#                         )

#         return HttpResponseRedirect(reverse("homepage"))

#     form = AddTweetForm()
#     return render(request, "addtweet.html", {"form": form})
