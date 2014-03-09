import urllib
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from cms.utils.page_resolver import get_page_from_request
import settings


class RedirectFallbackMiddleware(object):
    def process_request(self, request):
        if self.is_admin(request):
            return None
        try:
            page = get_page_from_request(request)
            if page and page.redirects_to:
                if page.id == page.redirects_to.id:
                    return None #disable infinite recursion
                return redirect(page.redirects_to.page_to.get_absolute_url())
        except Exception:
            pass

        return None

    def is_admin(self, request):
        pages_root = urllib.unquote(reverse("pages-root"))
        if 'django.contrib.admin' in settings.INSTALLED_APPS:
            admin_base = reverse('admin:index').lstrip('/')
        else:
            admin_base = None
        if not admin_base:
            return False

        path = request.path[len(pages_root):]
        return path.startswith(admin_base)

