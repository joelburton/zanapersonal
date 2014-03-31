from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from .views import PageDetailView, HomepageView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', HomepageView.as_view(), name='website.detail'),
    url(r'^(?P<slug>[\w-]*)/$', PageDetailView.as_view(), name='page.detail'),

)


