from django import forms


class AddTweetForm(forms.Form):
    text = forms.CharField(max_length=140, widget=forms.Textarea)
