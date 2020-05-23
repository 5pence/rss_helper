from django import forms
from django.contrib.auth.models import User
from .models import Comment, Feed
from feed.utils import fetch_rss


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        """ To ensure the two passwords match on the registration form"""
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']


class AddFeedForm(forms.ModelForm):
    """ Form for logged in user to add feeds """
    title = forms.CharField(label='Title', required=True)
    url = forms.URLField(label='URL', required=True)

    class Meta:
        model = Feed
        fields = ('title', 'url')

    def clean_url(self):
        url = self.cleaned_data['url']
        result = fetch_rss(url)
        if 'bozo' in result and result['bozo'] == 1:
            raise forms.ValidationError('Invalid RSS Feed')
        return url

    def clean(self):
        cleaned_data = super(AddFeedForm, self).clean()
        title = cleaned_data.get('title')
        url = cleaned_data.get('url')
        if Feed.objects.filter(title=title).count():
            raise forms.ValidationError(
                "You are already that title in your feed, please choose another."
            )
        if Feed.objects.filter(url=url).count():
            raise forms.ValidationError(
                "You are already following that feed url, you don't need to follow it twice."
            )


class CommentForm(forms.ModelForm):
    """ Form for logged in user to enter comment """
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('text',)

