# from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import hashlib

from .models import Url
from rest_framework import viewsets
from .serializers import UrlSerializer
from .createurlhash import create_entry


# class UrlViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Url.objects.all().order_by('-date_joined')
#     serializer_class = UrlSerializer



# def main(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     output = ', '.join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)



# subclass of HttpResponse that we can use to render any data we return into json
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# takes source_url
# returns db object (source and short)
@csrf_exempt
def shorten_url(request):
    """
    search for url, and return or create.
    """
    if request.method == 'POST':
        # source url is in request.body.data
        print(request.body)
        source_url = request.body

        try:
            # find in db
            url = Url.objects.get(source_url=source_url)
        except Url.DoesNotExist:
            # not found - must create
            url = create_entry(source_url)
            # return HttpResponse(status=404)

        serializer = UrlSerializer(url)
        print('returning', serializer.data)
        return JSONResponse(serializer.data)

        print('here', source_url)
        return JSONResponse('hi')
    else:
        return HttpResponse(status=504)

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


# get method with key
# searches db and returns url

# post method with url
# returns short_url

# generates hash of url
# searches db for item with all front-edged subsets of that hash
# if one contains same url, return

#max lengthof ?4, add one with each pass
# add comment with alternatives considered/pros/cons

# select * from Url where colName in (comma-sep-list)
# return shortest with no val
# if none avail, rehash and try again
