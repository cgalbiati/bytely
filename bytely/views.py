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

# returns unique string for the short link or existing short link if url is already in db
def create_entry(source_url):
    # shaw hash
    hashed_url = hashlib.sha224(source_url).hexdigest()

    # add http so redirect works
    if not 'http' in source_url:
        source_url = 'http://' + source_url
    # it's up to the user to put in a valid link
    print('creating for', source_url)

    #max length of hash to try
    max_length = 4
    avail_hash = ''
    
    while not avail_hash:
        # build string list of slices to use in query 
        hash_slices = [hashed_url[0]]
        for i in range(2, max_length):
            hash_slices.append(hashed_url[0:i])

        print('hash slices', hash_slices)
        # query db for slices
        found = Url.objects.filter(short_url__in=hash_slices).extra(select={'length':'Length(short_url)'}).order_by('-length')
        print('found', found)

        # find shortest avail

        # look for url match
        for item in found: 
            if item.source_url == source_url:
                return item

        # see if there is an available hash with length less than or equal to max_length
        if len(found) == 0:
            avail_hash = hashed_url[0]
        else :
            avail_len = len(found[-1]) + 1
            if avail_len <= max_length:
                avail_hash = hashed_url[0:avail_len]
            else:
                #increase max length and rehash
                max_length += 1
                hashed_url = hashlib.sha224(hashed_url).hexdigest()
                # this will not find the shortest possbile hash - 
                # there could be a high number of collisions for reasons of cioncidence or malevolence
                # if production shows longer-than-expected urls being generated, changes could be made - 
                # this could be changed to generate random stings, use a dift hash, just increment in base 60, etc

    
    new_entry = Url(short_url=avail_hash, source_url=source_url)
    new_entry.save()
    return new_entry



