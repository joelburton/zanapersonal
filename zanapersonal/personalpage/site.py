"""
Middleware to manage multiple sites in this instance.
"""

from .models import Website


class SiteMiddleware(object):
    """Middleware to manage sites."""

    def process_request(self, request):
        """If this request matches a website domain, mark this in the request."""

        try:
            request.site = Website.objects.get(domain=request.META['HTTP_HOST'])
        except Website.DoesNotExist:
            pass

