# from django.conf.urls import url
# from django.views.generic import TemplateView
# from django.views.generic.base import RedirectView

# from . import views

# urlpatterns = [
#     url(r'^$', views.index)
#     # url(r'^$', TemplateView.as_view(template_name='index.html'))
#     # url(r'^site/$', RedirectView.as_view(url='https://djangoproject.com'), name='go-to-django'),
#     # url(r'^shorten/(?P<pk>[0-9]+)/$', views.snippet_detail),
#     # url(r'^site/(?P<pk>[0-9]+)/$', views.snippet_detail),

# ]

from django.conf.urls import url
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import serve
from . import views


urlpatterns = [
    url('^$', TemplateView.as_view(template_name='index.html')),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^shorten/$', views.shorten_url, name='shorten'),
    # url(r'^shorten/(?P<source_url>.+)/$', views.shorten_url, name='shorten'),

    # static files
    url(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),

    # if the base is followed by anything else, it is a hash
    url(r'^(?P<short_url>.+)/$', views.go_to_site, name='go'),

] 
