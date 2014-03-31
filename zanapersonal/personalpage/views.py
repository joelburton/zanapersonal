from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.views import generic

from .models import Page, Website


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


class PageCreationView(generic.CreateView):
    model = Page

    def get_form(self, form_class):
        form = super(PageCreationView, self).get_form(form_class)
        import pdb; pdb.set_trace()

