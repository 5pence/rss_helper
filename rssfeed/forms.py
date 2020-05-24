from django import forms
from django.contrib.auth.models import User
from .models import Comment, Feed
from feed.utils import fetch_rss


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
        feed_query = Feed.objects.filter(title=title)
        if self.instance.id:
            feed_query = feed_query.exclude(id=self.instance.id)
        if feed_query.count():
            raise forms.ValidationError(
                "You already have that title in your feed, please choose another."
            )
        feed_query = Feed.objects.filter(url=url)
        if self.instance.id:
            feed_query = feed_query.exclude(id=self.instance.id)
        if feed_query.count():
            raise forms.ValidationError(
                "You are already following that feed url, you don't need to follow it twice."
            )


class CommentForm(forms.ModelForm):
    """ Form for logged in user to enter comment """
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('text',)

