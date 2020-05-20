from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import Feed, FeedItem


def register(request):
    """ Handles the registration view logic"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the user object
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def welcome(request):
    """Main home screen"""
    return render(request, 'account/welcome.html')


@login_required
def my_feeds(request):
    """View that shows logged in user their feeds ordered by latest created_at """
    feeds = Feed.objects.filter(user=request.user)
    feed_items = FeedItem.objects.filter(feed__user=request.user).order_by('-created_at')
    return render(request, 'account/my_feeds.html', {'feeds': feeds, 'feed_items': feed_items})


@login_required
def feed_item_detail(request):
    """View to handle detail page for individual feed item"""
    feed_item = FeedItem.objects.get(id=request.GET.get('id'))
    feed_item.is_read = True
    feed_item.save()
    return render(request, 'account/feed_detail.html', {'feed_item': feed_item})

# TODO: wire up front end and build templates
# TODO: add somewhere to subscribe(follow) to available feeds
# TODO: add view for feed item detail with favourite / unfavourite functionality and comment/note section
# TODO: maybe add a bookmarks view that returns a list of previously bookmarked feed items
# TODO: add favourites and un-favourite functionality for user
# TODO: add comments / note(comment) functionality
# TODO: put celery task in own container
# TODO: Docker containerize app
# TODO: write tests cover main functions including testing for backoff
# Todo: copy my notes Readme