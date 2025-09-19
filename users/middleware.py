from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse


class EmailVerificationMiddleware:
    """
    Middleware to ensure users verify their email before accessing protected views.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        # Skip middleware for these paths
        public_paths = [
            '/api/users/verify-email/',
            '/api/users/login/',
            '/api/users/register/',
            '/api/users/refresh/',
            '/api/schema/',
            '/api/docs/',
            '/admin/',  # Admin panel-ს დავუმატოთ
            '/static/',  # Static files-ისთვის
            '/media/',   # Media files-ისთვის
        ]
        
        if any(request.path.startswith(path) for path in public_paths):
            return self.get_response(request)
        
        # Check if user is authenticated and email is not verified
        if hasattr(request, 'user') and request.user.is_authenticated:
            # შევამოწმოთ აქვს თუ არა User მოდელს is_email_verified ატრიბუტი
            if hasattr(request.user, 'is_email_verified'):
                # თუ email არ არის verified
                if not request.user.is_email_verified:
                    # If it's an API request, return JSON response
                    if request.path.startswith('/api/'):
                        return JsonResponse(
                            {'detail': 'Please verify your email address.'},
                            status=403
                        )
                    # For web requests, redirect to verification page
                    return redirect('verify-email')
            else:
                # თუ is_email_verified ატრიბუტი არ არსებობს, 
                # მაშინ მოვკლოთ middleware-ს მუშაობა ამ იუზერისთვის
                print(f"Warning: User {request.user.email} doesn't have is_email_verified attribute")
                # გავაგრძელოთ request-ი ნორმალურად
                pass
        
        response = self.get_response(request)
        return response