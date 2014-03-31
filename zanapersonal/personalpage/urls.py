from django.conf.urls import patterns, url
from django.contrib import admin

from .views import PageDetailView, HomepageView, WebsiteSettingsUpdateView, \
    WebsiteBiographicalUpdateView, WebsiteAppearanceUpdateView, WebsiteHomepageUpdateView, \
    PageCreateView, PageUpdateView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', HomepageView.as_view(), name='website.detail'),
    url(r'^-settings/$', WebsiteSettingsUpdateView.as_view(), name='website.settings'),
    url(r'^-biographical/$', WebsiteBiographicalUpdateView.as_view(), name='website.biographical'),
    url(r'^-appearance/$', WebsiteAppearanceUpdateView.as_view(), name='website.appearance'),
    url(r'^-homepage/$', WebsiteHomepageUpdateView.as_view(), name='website.homepage'),
    url(r'^-add-page/$', PageCreateView.as_view(), name='page.create'),
    url(r'^(?P<slug>[\w-]*)/$', PageDetailView.as_view(), name='page.detail'),
    url(r'^(?P<slug>[\w-]*)/-edit/$', PageUpdateView.as_view(), name='page.update'),

)


