from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import UserRegistrationForm, CommentForm, AddFeedForm
from .models import Feed, FeedItem, Comment
from django.urls import reverse


def register(request):
    """ Handles the registration view logic"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def welcome(request):
    """ Main home screen """
    return render(request, 'account/welcome.html')


@login_required
def add_feed(request):
    """ View that allows logged in user to add their own feed  """
    form = AddFeedForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = request.user
            feed = form.save(commit=False)
            feed.user = user
            feed.last_checked_at = timezone.now()
            feed.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Your feed was added, it may take up to a minute '
                                 'for you to see some feed items')

    return render(request, 'account/add_feed.html', {'form': form})


@login_required
def available_feeds(request):
    """ View that shows available feeds """
    return render(request, 'account/add_feed.html')


@login_required
def my_feeds(request):
    """ View that shows logged in user their feeds ordered by latest created_at """
    feeds = Feed.objects.filter(user=request.user)
    return render(request, 'account/my_feeds.html', {'feeds': feeds})


@login_required
def remove_feed(request, pk):
    """ Logic to remove feed from logged in user's list """
    feed = Feed.objects.get(id=pk, user=request.user)
    feed.delete()
    messages.add_message(request, messages.WARNING, 'Your feed was deleted')
    return HttpResponseRedirect(reverse('my_feeds'))


@login_required
def reset_fail_count(request, pk):
    messages.add_message(request, messages.INFO, 'Restarted feed')
    feed = Feed.objects.get(id=pk, user=request.user)
    feed.fail_count = 0
    feed.last_checked_at = timezone.now()
    feed.save()
    return HttpResponseRedirect(reverse('my_feeds'))


@login_required
def my_favourite_feeds(request):
    """ View that shows logged in user their favourite feeds ordered by latest created_at """
    feeds = Feed.objects.filter(user=request.user)
    feed_items = FeedItem.objects.filter(feed__user=request.user).order_by('-created_at')
    feed_items = feed_items.filter(is_bookmarked=True)
    return render(request, 'account/my_favourite_feed_items.html', {'feeds': feeds,
                                                                    'feed_items': feed_items})


@login_required
def feed_item_detail(request, pk):
    """ View to handle detail page for individual feed item and saving is_read to True """
    feed_item = FeedItem.objects.get(id=pk, feed__user=request.user)
    comments = Comment.objects.filter(feed_item=feed_item).order_by('-created_at')
    feed_item.is_read = True
    feed_item.save()
    return render(request, 'account/feed_detail.html', {'feed_item': feed_item,
                                                        'comments': comments})


@login_required
def toggle_favourite_feed_item(request):
    """ Toggles is_favourite on feed item """
    feed_item = FeedItem.objects.get(id=request.GET.get('id'))
    feed_item.is_bookmarked = not feed_item.is_bookmarked
    feed_item.save()
    return render(request, 'account/feed_detail.html', {'feed_item': feed_item})


@login_required
def add_comment(request, pk):
    """ Saves comment to database """
    form = CommentForm(request.POST)
    feed_item = FeedItem.objects.get(id=pk)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.feed_item = feed_item
            comment.save()
        else:
            # send error message to user
            messages.add_message(request, messages.ERROR, 'Please fill in the form correctly')
    return HttpResponseRedirect(feed_item.get_absolute_url())


@login_required
def delete_comment(request, pk):
    """ Handles deleting a comment, also checks the correct user doing the deleting """
    comment = Comment.objects.get(pk=pk, feed_item__feed__user=request.user)
    feed_item_id = comment.feed_item_id
    comment.delete()
    messages.add_message(request, messages.WARNING, 'Your comment was deleted')
    return HttpResponseRedirect(reverse('feed_item', kwargs={'pk': feed_item_id}))

# TODO: Edit feed button
# TODO: Ensure user doesn't use same name or feed url to avoid duplicates when adding feed
# TODO: Input security
# TODO: Put celery task in own container
# TODO: Docker containerize app
# TODO: Write tests cover main functions including testing for backoff
# TODO: Copy my notes Readme
