# Readme

Bytely is a url shortener.  The user inputs a source url, and the app creates a unique hashed link that redirects to the source.


### Installation
You need Python 2.7^ and pip. If you don't have these, see how [here][pip].

```sh
$ git clone [git-repo-url] extra-credit
$ cd extra-credit
$ pip install -r requirements.txt
```

### Running the program
Build the JS
```sh
$ cd ./bytely/browser
npm install
webpack
```
To run on the development server:
```sh
$ ./manage.py runserver
```

### Testing
```sh
$ ./manage.py test bytely
```
These are meant to be a sample, not a complete testing suite.

### Thoughts behind some decisions

I chose my strategy to 

I chose not to use any of Django's templating becuase I did not to send any data to the front end initially (only as the return of an ajax request for the short url).  Instead, the base url serves an html document, which requests the JS bundle containing the React elements, etc, and all the templating is done through React.

I chose my hashing strategy to ensure short urls, while obscuring the generation algorithm (so that the links are not easilly guessable) and aiming for few duplicate urls in the database.  

To make the short link, I hash the url using shaw224 becuase this algorithm has very low unintentional collision. (I would not expect too many people to try to manufacture colisions in this scenario, and if they did, they would just end up with longer links.)  After hashing the url, I try to find the shortest slice starting from the front that is not already taken (or return the hash for the url if it is already in the database.  I set it to max out at a length of four characters, and if it has not found an avalable hash, it rehashes, and increases the max length by one.  In this way, it should be able to handle colisions. This would not find the shortest possible hash, but should be able to return reasonably short hashes for whatever size the existing data set is.

Other strategies considered were to count up in base 60 (guessable) or simply generate a reandom string (and try again if there was a colision). (And probably incerase the length as the data set grew) This would avoid the premature lengthening of hashes, but would make it slower to manage duplicates (because the hashes are primary keys, so it is fastest to search by that).  

[pip]: <https://pip.pypa.io/en/stable/installing/>
