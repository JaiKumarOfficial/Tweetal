from django import forms
from .models import Users, Tweet, DmUserList, ScheduledTweet
from .models import Template
from django.utils import timezone


class UserLoginForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = ('name', 'consumer_key', 'consumer_secret_key', 'access_token', 'access_secret_token')


class PostTweet(forms.ModelForm):

    class Meta:
        model = Tweet
        fields = ('tweet', 'document', 'schedule_post')
        widgets = {
            'tweet': forms.Textarea(attrs={'placeholder': 'Tweet Me !!'}),
            'schedule': forms.DateTimeInput(attrs={'type': 'datetime'}),
        }


class ScheduledTweetForm(forms.ModelForm):

    class Meta:
        model = ScheduledTweet
        fields = ('tweet', 'document', 'schedule_post')
        widgets = {
            'tweet': forms.Textarea(attrs={'placeholder': 'Tweet Me !!'}),
            'schedule': forms.DateTimeInput(attrs={'type': 'datetime'}),
        }


class Search(forms.Form):
    search_text = forms.CharField(max_length=100, label='Search Tweet', required=True)
    since = forms.DateTimeField(label='From date, Note: Date should be formatted as YYYY-MM-DD.', required=True)
    until = forms.DateTimeField(label='Till date, Note: Date should be formatted as YYYY-MM-DD.', required=False)
    count = forms.IntegerField(label='No. of Tweets preferred, Note: Maximum 100 Tweets', required=False)
    result_type = forms.CharField(label='Sort Tweets, Valid inputs "mixed", "recent", "popular"', required=False)
    geo_location_lat = forms.FloatField(label='Latitude', required=False)
    geo_location_long = forms.FloatField(label='Longitude', required=False)
    radius = forms.CharField(label='Radius, Note: Valid inputs are "mi" or "km" only; ex- 1km', required=False)


class DmForm(forms.Form):
    text = forms.CharField(label='Text', required=True)
    # document = forms.FileField(label='Document')


class DmUserListForm(forms.ModelForm):
    class Meta:
        model = DmUserList
        fields = '__all__'


class TemplateForm(forms.ModelForm):
    save_text = forms.BooleanField(widget=forms.CheckboxInput, required=False)

    class Meta:
        model = Template
        fields = ('text', 'temp_name')


# class TemplateResponse(forms.ModelForm):
#     class Meta:
#         model = TemplateText
#         fields = 'text'
