from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class BlockBrowserByUA(MiddlewareMixin):
    """Middleware to redirect requests with a user agent containing "chorme/"
    to the invalid-browser path
    """    
    def process_request(self, request):
        user_agent = request.headers["User-Agent"]
        # breakpoint()
        if "chrome/" in user_agent.lower() and request.path != '/invalid/':
            return redirect('invalid-browser')
        