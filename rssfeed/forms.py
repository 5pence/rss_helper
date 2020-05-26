from django import forms
from .models import Comment, Feed
from feed.utils import fetch_rss


class AddFeedForm(forms.ModelForm):
    """ Form for logged in user to add feeds """
    title = forms.CharField(label='Title', required=True)
    url = forms.URLField(label='URL', required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddFeedForm, self).__init__(*args, **kwargs)

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
        title_query = Feed.objects.filter(title=title, user=self.user.id)
        if self.instance.id:
            title_query = title_query.exclude(id=self.instance.id)
        if title_query.count():
            raise forms.ValidationError(
                "You already have that title in your feed, please choose another."
            )
        url_query = Feed.objects.filter(url=url, user=self.user.id)
        if self.instance.id:
            url_query = url_query.exclude(id=self.instance.id)
        if url_query.count():
            raise forms.ValidationError(
                "You are already following that feed url, you don't need to follow it twice."
            )


class CommentForm(forms.ModelForm):
    """ Form for logged in user to enter comment """
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('text',)

