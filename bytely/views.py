from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets

from .models import Url
from .serializers import UrlSerializer
from .createurlhash import create_entry


# subclass of HttpResponse that we can use to render any data we return into json
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# takes source_url as response body
# returns db object (source and short)
@csrf_exempt
def shorten_url(request):
    """
    search for url, and return or create.
    """
    if request.method == 'POST':
        # source url is in request.body.data
        source_url = request.body

        try:
            # find in db
            url = Url.objects.get(source_url=source_url)
        except Url.DoesNotExist:
            # not found - must create
            url = create_entry(source_url)

        serializer = UrlSerializer(url)
        #return url object
        return JSONResponse(serializer.data)

    else:
        return HttpResponse(status=504)

#takes url hash as arg
#redirects to source url
@csrf_exempt
def go_to_site(request, short_url):
    """
    Retrieve url and redirect.
    """
    if request.method == 'GET':
        try:
            # find in db
            url = Url.objects.get(short_url=short_url)
        except Url.DoesNotExist:
            # not found 
            return HttpResponse(status=404)

        # redirect to source
        return HttpResponseRedirect(url.source_url)

    else:
        return HttpResponse(status=504)

