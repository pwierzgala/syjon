class ForceDefaultLanguageMiddleware:
    """
    Ignore Accept-Language HTTP headers.

    Forces the I18N machinery to always choose settings.LANGUAGE_CODE
    as the default initial language, unless another one is set via sessions or cookies.

    Must be installed *before* LocaleMiddleware.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']

        response = self.get_response(request)
        return response
