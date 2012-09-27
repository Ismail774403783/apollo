from django.http import HttpResponse


class AllowOriginMiddleware(object):
    def process_request(self, request):
        if request.method == 'OPTIONS':
            return HttpResponse()

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, DELETE, PUT'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
