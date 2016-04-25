from django.test import TestCase
import unittest
from .models import Url
from .createurlhash import create_entry

# this is not meant to be complete, it is just a sample

class CreateEntryTestCase(TestCase):
    def setUp(self):
        Url.objects.create(short_url='a', source_url='http://google.com')
        # not the right hash - used to make colision
        Url.objects.create(short_url='a8', source_url='http://zulip.com')

    def test_new_entry(self):
        """unique source urls get new entry in db"""
        flocabulary = create_entry('http://flocabulary.com')
        in_db = Url.objects.get(source_url='http://flocabulary.com')
        all_with_hash = Url.objects.filter(short_url=flocabulary.short_url)
        # is in db
        self.assertEqual(flocabulary.short_url, in_db.short_url)
        # is the only thing with that hash in db
        self.assertEqual(len(all_with_hash), 1)

    def test_makes_shortest(self):
        """returns shortest cut of hash"""
        recurse = create_entry('http://recurse.com')
        # g = create_entry('google.com')
        # g = create_entry('http://google.com')
        # g = create_entry('chandragalbiati.com')
        # g = create_entry('flocabulary.com')
        #initially would try 1, but that is used by recurse
        self.assertEqual(recurse.short_url, 'a85')

    def test_create_dup(self):
        """if asked to create a short url for a url already in db, returns existing hash"""
        google = create_entry('http://google.com')
        self.assertEqual(google.short_url, 'a')

    def test_get_format(self):
        """returns existing hash if input without http"""
        google2 = create_entry('google.com')
        self.assertEqual(google2.short_url, 'a')

    def test_create_format(self):
        """if input without http, adds http"""
        me = create_entry('me.com')
        self.assertEqual(me.source_url, 'http://me.com')
