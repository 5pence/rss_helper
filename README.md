 # RSS Feed Manager
 
 ## About
 
 This django app provides a management system for RSS feeds. It uses Celery and Celery beats to call the user added
 RSS feeds, a Postgres DB and Django. 
 
 ### Register / Login
 
 Upon a user registering they can login and see the pages detailed below:
 
 ### Add Feed page
 
 This is where you can add feeds. Note a user cannot add duplicate titles or feed urls.  Also if the user tries to
 add feed that does not resolve correctly the system will not allow them to add it.
 
 ### My Feeds page
 
 This page shows all added feeds within an accordion. The unread feed items are displayed on the my feeds page on
 the top of each feed's accordion, the number is marked using the HTML `<mark>` tag. Once the feed accordion is
 expanded the feed items that are unread are also marked. Upon clicking on a feed item you go to the feed item
 detail page, at this point the feed is updated as being read.
 
 On this page you can remove feeds, update feed, or click feed items to review their details
 
 ### My Favourites page
 
 This is similar to the My Feeds page accept it only shows bookmarked feed items (and the feed they belong to).
       
 ### Feed item details page
 
 Here a user can read the feed item and add and remove a bookmark (all added bookmarks are shown in the my My
 Favourites page). You can also add and remove comments which are shown underneath.  
 
 ### Failed feed fallback mechanism
 
 I decided to use an exponential fall back when a feed failed to update. To see this code it is at ~/feed/tasks.py
 The FAIL_COUNT_THRESHOLD is set in .env locally and is set to 10 although if none is given it defaults to 10 in
 settings.py. In this case every minute a check is made to fetch feeds that have a FAIL_COUNT_THRESHOLD less than 10
 and a last_checked_at time in the past. If the fetch fails it increments the fail_count by one and sets the
 last_checked_at time to 2 exponential fail_count minutes in the future. Upon a successful fetch the feed's
 fail_count is reset back to zero.
 
 ## How to run this app locally using docker
 
 1. Clone this project using `git clone`
 2. cd into the project directory.
 3. run `docker-compose build`
 4. run `docker-compose up`
 
 After these processes you can visit the site at 0.0.0.0:8000 and register and login and start using the site.    
 
 I have tested this on 4 separate machines so do not envisage any problems, if you do have any issues then please
 contact me.
 
 Other commands that you may want to try are:
 
 - `docker-compose run web pipenv run /code/manage.py createsuperuser`
 - `docker-compose run web pipenv run /code/manage.py test`
 