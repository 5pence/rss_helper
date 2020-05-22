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
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(
                                        attrs={"style": "resize: none"}),
                                  required=True)
    url = forms.URLField(label='URL', required=True)

    def clean_url(self):
        url = self.cleaned_data['url']
        ret = fetch_rss(url)
        if 'bozo' in ret and ret['bozo'] == 1:
            raise forms.ValidationError('Invalid RSS Feed')
        return url


    class Meta:
        model = Feed
        fields = ('title', 'description', 'url')


class CommentForm(forms.ModelForm):
    """ Form for logged in user to enter comment """
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('text',)

