import os


class AdminSubdomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]

        if host == os.getenv('DJANGO_ADMIN_HOST'):
            request.urlconf = 'mysite.admin_urls'

        response = self.get_response(request)
        return response
