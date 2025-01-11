from django.http import HttpResponse

class MiddlewareLifeCycle:
    def __init__(self, get_response):
        # this is called only once when app starts;
        print("MiddlewareLifeCycle.__init__")
        self.get_response=get_response

    def __call__(self, request):
        print("Before the view is executed")
        # call the next middleware and capture its response.
        response = self.get_response(request)
        print("After the view is executed")
        # return the response
        return response
    

class ExceptionHandlingMiddlware:
    def __init__(self, get_response):
        # this is called only once when app starts;
        print("ExceptionHandlingMiddlware.__init__")
        self.get_response=get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        print(exception.__class__.__name__)
        return HttpResponse("<b>Issues found</b>")
    
