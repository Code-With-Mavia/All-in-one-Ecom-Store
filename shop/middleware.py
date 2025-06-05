from django.utils import timezone
from django.contrib.auth import logout
# Middleware for auto-logout after a period of inactivity
class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.timeout = 300  # 5 minutes in seconds

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')

            now = timezone.now().timestamp()  # current time in seconds

            if last_activity:
                elapsed = now - last_activity
                if elapsed > self.timeout:
                    logout(request)
                    # Optionally: clear session completely
                    request.session.flush()
            # update last activity time on each request
            request.session['last_activity'] = now

        response = self.get_response(request)
        return response
