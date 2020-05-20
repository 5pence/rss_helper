from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm


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
    return render(request, 'account/welcome.html')


# def my_feeds(request):
#     feeds =



# TODO: wire up front end and build templates
# TODO: add view to view feeds subbed to including unread feed item count
# TODO: add view for feed item detail with favourite / unfavourite functionality and comment/note section
# TODO: maybe add a bookmarks view that returns a list of previously bookmarked feed items
# TODO: add follow and unfollow functionality for user
# TODO: add favourites and unfavourite functionality for user
# TODO: add comments / note functionality
# TODO: add cerery or Asyncio to update feed asynchronously include an expotential fall back mechanism  - maybe in own container?
# TODO: Docker containerize app
# TODO: write tests cover main functions including testing for backoff
# Todo: copy my notes Readme