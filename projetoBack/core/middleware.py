import re
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware

class CSRFExemptMiddleware(CsrfViewMiddleware):
    def process_request(self, request):
        if hasattr(settings, 'CSRF_EXEMPT_URLS'):
            for url_pattern in settings.CSRF_EXEMPT_URLS:
                if re.match(url_pattern, request.path_info.lstrip('/')):
                    setattr(request, '_dont_enforce_csrf_checks', True)
        return super().process_request(request)