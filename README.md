# django-google-analytics-reporter
Report events to google analytics through your Python/Django code.

# Required Settings


GOOGLE_ANALYTICS_ID = 'UA-xxxxxxxxx-1' # your google analytics

DEFAULT_TRACKING_DOMAIN = 'yourdomain.com' # can be passed in, but if nothing is passed, it defaults to this


# Usage
**Make sure Celery is installed and working.**

At the core, here's a way to send a pageview using the **Tracker** class:

    from google_analytics_reporter import Tracker
    
    Tracker(request=self.request).send(t='pageview', dh='yourdomain.com', dp='/newsletter/thankyou/', el='An optional label')

**request** isn't required, but it'll extract the **user.id** (if possible) and the analytics **client_id** from the _ga cookie if it exists. Otherwise, it makes its own client_id. Always include it if you have access to it. You can also feed it user_id=user.id and client_id=client_id yourself if necessary. You can use the **Tracker** class to send any type of google analytics type. So if this library doesn't have an easy to use class to use for your specific needs, you can always use **Tracker**.

**OR**

Since that's a little confusing to remember how to use it properly, Use the **PageView** class, which subclasses the Tracker class and allows you to pass in more human-readable args.

To send a pageview with the user_id and client_id extracted from the request. **This does the same thing as the Tracker example above.**

    from google_analytics_reporter import PageView
    
    PageView(request=self.request).send(page='/newsletter/thankyou/', label='An optional label')



**Send an event**

    from google_analytics_reporter import Event
    
    Event(request=self.request).send(category='video', action='play')
