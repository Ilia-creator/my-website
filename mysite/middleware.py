import os


class AdminSubdomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]

        admin_host = os.getenv('DJANGO_ADMIN_HOST', '')
        shop_host = os.getenv('DJANGO_SHOP_HOST', '')

        if admin_host and host == admin_host:
            request.urlconf = 'mysite.admin_urls'
        elif shop_host and host == shop_host:
            request.urlconf = 'mysite.shop_urls'

        response = self.get_response(request)
        return response
