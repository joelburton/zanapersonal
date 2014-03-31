from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.views import generic

from .models import Page, Website
from .forms import WebsiteSettingsForm, WebsiteBiographicalForm, WebsiteHomepageForm, \
    WebsiteAppearanceForm, PageForm


class HomepageView(generic.DetailView):
    model = Website

    def dispatch(self, request, *args, **kwargs):
        if not getattr(request, 'site', None):
            messages.add_message(request, messages.WARNING,
                                 "No site found for this domain.")
            return redirect('/admin/personalpage/website')
        return super(HomepageView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.site

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)

        pages = Page.objects.filter(website=self.request.site, published=True)

        if pages:
            context['nav'] = (
                [{'title': 'Home', 'url': '/', 'active': True}] +
                [
                    {'title': p.navigation_title,
                     'url': p.get_absolute_url(),
                     'active': False}
                    for p in pages if p.navigation_title
                ]
            )

        if self.request.user in self.object.users.all():
            context['editable'] = True

        return context


class PageDetailView(generic.DetailView):
    """ """

    model = Page

    def dispatch(self, request, *args, **kwargs):
        if not getattr(request, 'site', None):
            messages.add_message(request, messages.WARNING,
                                 "No site found for this domain.")
            return redirect('/admin/personalpage/website')
        return super(PageDetailView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Page.objects.filter(website=self.request.site, published=True)

    def get_context_data(self, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)

        pages = Page.objects.filter(website=self.request.site, published=True)

        if pages:
            context['nav'] = (
                [{'title': 'Home', 'url': '/', 'active': False}] +
                [
                    {'title': p.navigation_title,
                     'url': p.get_absolute_url(),
                     'active': p == self.object}
                    for p in pages if p.navigation_title
                ]
            )

        if self.request.user in self.object.website.users.all():
            context['editable'] = True

        return context


class WebsiteBaseUpdate(generic.UpdateView):
    template_name = "personalpage/website_form.html"

    def get_object(self, queryset=None):
        return self.request.site

    def form_valid(self, form):
        messages.add_message(self.request,
                             messages.SUCCESS,
                             "Website updated.")
        return super(WebsiteBaseUpdate, self).form_valid(form)


class WebsiteSettingsUpdateView(WebsiteBaseUpdate):
    form_class = WebsiteSettingsForm
    settings_active = "active"
    title = "Settings"


class WebsiteBiographicalUpdateView(WebsiteBaseUpdate):
    form_class = WebsiteBiographicalForm
    biographical_active = "active"
    title = "Biographical Information"


class WebsiteAppearanceUpdateView(WebsiteBaseUpdate):
    form_class = WebsiteAppearanceForm
    appearance_active = "active"
    title = "Appearance"


class WebsiteHomepageUpdateView(WebsiteBaseUpdate):
    form_class = WebsiteHomepageForm
    homepage_active = "active"
    title = "Homepage"


class PageCreateView(generic.CreateView):
    form_class = PageForm
    model = Page

    def get_initial(self):
        sites = Website.objects.filter(users=self.request.user)
        return {'website': sites[0]}

    def form_valid(self, form):
        messages.add_message(self.request,
                             messages.SUCCESS,
                             "Page added.")
        return super(PageCreateView, self).form_valid(form)


class PageUpdateView(generic.UpdateView):
    model = Page
    form_class = PageForm

    def form_valid(self, form):
        messages.add_message(self.request,
                             messages.SUCCESS,
                             "Page updated.")
        return super(PageUpdateView, self).form_valid(form)



