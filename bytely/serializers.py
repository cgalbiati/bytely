from .models import Url
from rest_framework import serializers


class UrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Url
        fields = ('source_url', 'short_url')

