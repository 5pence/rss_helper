from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import Feed, FeedItem, Comment


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
    """View to handle detail page for individual feed item and saving is_read to True"""
    feed_item = FeedItem.objects.get(id=request.GET.get('id'))
    comments = Comment.objects.filter(feed_item=feed_item).order_by('-created_at')
    feed_item.is_read = True
    feed_item.save()
    return render(request, 'account/feed_detail.html', {'feed_item': feed_item, 'comments': comments})


@login_required
def toggle_favourite_feed_item(request):
    """Toggles is_favourite on feed item"""
    feed_item = FeedItem.objects.get(id=request.GET.get('id'))
    feed_item.is_bookmarked = not feed_item.is_bookmarked
    feed_item.save()
    return render(request, 'account/feed_detail.html', {'feed_item': feed_item})

# TODO: Add somewhere to subscribe(follow) to available feeds
# TODO: Add comment/note section for feed item detail
# TODO: Maybe add a bookmarks view that returns a list of previously bookmarked feed items
# TODO: Put celery task in own container
# TODO: Docker containerize app
# TODO: Write tests cover main functions including testing for backoff
# TODO: Copy my notes Readme
