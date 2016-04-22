# from django.shortcuts import render

from django.http import HttpResponse

from .models import Url
from rest_framework import viewsets
from .serializers import UrlSerializer


class UrlViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Url.objects.all().order_by('-date_joined')
    serializer_class = UrlSerializer



# def main(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     output = ', '.join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)


from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# subclass of HttpResponse that we can use to render any data we return into json
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

# view that supports listing all the existing snippets, or creating a new snippet
@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)

# takes short
# returns db object (source and short)
@csrf_exempt
def get_source_url(request, short_url):
    """
    Retrieve url.
    """
    if request.method == 'GET':
        # find in db
        try:
            url = Url.objects.get(short_url=short_url)
        except Url.DoesNotExist:
            return HttpResponse(status=404)
        #serialize and send
        serializer = UrlSerializer(url)
        return JSONResponse(serializer.data)
    else
        # only accept get reqs
        return HttpResponse(status=504)

# takes source_url
# returns db object (source and short)
@csrf_exempt
def make_short_url(request, source_url):
    """
    Retrieve url.
    """
    if request.method == 'POST':
        try:
            # find in db
            url = Url.objects.get(source_url=source_url)
        except Url.DoesNotExist:
            # not found - must create
            url = createEntry(source_url);
            # return HttpResponse(status=404)

        serializer = UrlSerializer(url)
        return JSONResponse(serializer.data)
    else
        return HttpResponse(status=504)




# get method with key
# searches db and returns url

# post method with url
# returns short_url

# generates hash of url
# searches db for item with all front-edged subsets of that hash
# if one contains same url, return
# return shortest with no val
# if none avail, rehash and try again


def createEntry(source_url)
    return Url.objects.get(short_url='a1')

