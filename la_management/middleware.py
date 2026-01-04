from django.conf import settings
from django.shortcuts import redirect, resolve_url
from django.urls import reverse
import re

class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page
    other than the login, signup, and admin pages.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.public_prefixes = [
            '/admin/',
            '/static/',
            '/media/',
        ]

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            
            public_urls = [
                reverse('login'),
                reverse('signup'),
                reverse('logout'),
            ]
            
            # Check if path is in public_urls
            if path in public_urls:
                return self.get_response(request)
            
            # Check if path starts with any public_prefixes
            for prefix in self.public_prefixes:
                if path.startswith(prefix):
                    return self.get_response(request)
            
            # Redirect to login page
            login_url = resolve_url(settings.LOGIN_URL)
            return redirect(f"{login_url}?next={path}")

        return self.get_response(request)
