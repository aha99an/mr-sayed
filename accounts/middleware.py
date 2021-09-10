#Session model stores the session data
from django.contrib.sessions.models import Session
from accounts.models import CustomUser
class OneSessionPerUserMiddleware:
    # Called only once when the web server starts
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated and request.user.user_type == CustomUser.STUDENT:
            stored_session_key = request.user.session_key

            # if there is a stored_session_key  in our database and it is
            # different from the current session, delete the stored_session_key
            # session_key with from the Session table
            if stored_session_key != request.session.session_key:
                Session.objects.filter(session_key=stored_session_key).delete()
                request.user.session_key = request.session.session_key
                request.user.save()

        response = self.get_response(request)

        # This is where you add any extra code to be executed for each request/response after
        # the view is called.
        # For this tutorial, we're not adding any code so we just return the response

        return response