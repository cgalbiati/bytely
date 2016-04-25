import hashlib
from .models import Url



# returns unique string for the short link or existing short link if url is already in db
def create_entry(source_url):

    # add http so redirect works
    if not 'http' in source_url:
        source_url = 'http://' + source_url
    # it's up to the user to put in a valid link

    # shaw hash
    hashed_url = hashlib.sha224(source_url).hexdigest()

    #max length of hash to try
    max_length = 4
    avail_hash = ''
    
    while not avail_hash:
        # build string list of slices to use in query 
        hash_slices = [hashed_url[0]]
        for i in range(2, max_length):
            hash_slices.append(hashed_url[0:i])

        # query db for slices
        found = Url.objects.filter(short_url__in=hash_slices).extra(select={'length':'Length(short_url)'}).order_by('-length')

        # find shortest avail

        # look for url match
        for item in found: 
            if item.source_url == source_url:
                # this will not match variations such as www vs no wwww, but it should catch most overlaps
                # to improve, could regext after the // or www (*would also have to check https, because those should be treated separately)
                return item

        # see if there is an available hash with length less than or equal to max_length
        if len(found) == 0:
            avail_hash = hashed_url[0]
        else :
            avail_len = len(found) + 1
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



