import time
from django.core.exceptions import PermissionDenied

class PerformanceTimerMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

    def __call__(self, request):
        # 1. Logic BEFORE the view is called (Request Phase)
        start_time = time.time()

        # 2. Pass the request to the next layer/view
        response = self.get_response(request)

        # 3. Logic AFTER the view is called (Response Phase)
        duration = time.time() - start_time
        
        # We can add the duration to the response headers for debugging
        response['X-Page-Generation-Duration-ms'] = int(duration * 1000)
        
        print(f"Standard Log: {request.path} took {duration:.2f} seconds.")

        return response
    
    

class SecurityFirewallMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # In a real global project, this list might come from a secure database
        self.WHITELISTED_IPS = ['127.0.0.1', '192.168.1.1']

    def __call__(self, request):
        # Identify the user's IP address
        user_ip = request.META.get('REMOTE_ADDR')

        # Check if the IP is authorized
        if user_ip not in self.WHITELISTED_IPS:
            # This stops the request immediately and returns a 403 error
            raise PermissionDenied("Unauthorized Access Detected.")

        # If authorized, proceed to the next layer
        response = self.get_response(request)
        return response