from django.contrib import admin
from django.db import models
from django import forms

from .models import Website, Page


class WebsiteAdmin(admin.ModelAdmin):
    """Admin for website."""

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'domain',
                'footer',
                'users',
            )}),
        ('Biographical', {
            'fields': (
                'name',
                'headshot',
                'bio',
                'twitter',
            ),
            'description': "Information for biographical block that appears in the right column.",
            }),
        ('Appearance', {
            'fields': (
                'stylesheet',
                'css',
            ),
            'description': "Settings for the appearance of the site.",
            }),
        ('Homepage', {
            'fields': (
                'homepage_title',
                'homepage_description',
                'homepage_body',
            ),
            'description': "Content for homepage of site."})
    )

    list_display = ('title', 'domain', 'name')

    list_display_links = ('title', 'domain', 'name')

    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple}
    }

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Website.objects.all()
        else:
            return Website.objects.filter(users=request.user)

admin.site.register(Website, WebsiteAdmin)


class PageAdmin(admin.ModelAdmin):
    """Admin for pages."""

    list_display = ('website', 'slug', 'title', 'description', 'published')

    list_display_links = ('slug', 'title')

    search_fields = ('slug', 'title', 'description', 'body')

    list_filter = ('website', 'published')

    fieldsets = (
        (None, {
            'fields': (
                'website',
                'title',
                'slug',
                'description',
                'body',
                'published',
            )}),
        ('Navigation', {
            'fields': (
                'navigation_title',
                'priority',
            ),
            'description': "Settings for the top navigation bar.",
            }),
    )

    prepopulated_fields = {"slug": ["title"]}

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Page.objects.all()
        else:
            return Page.objects.filter(website__users=request.user)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "website":
                sites = Website.objects.filter(users=request.user)
                if sites:
                    kwargs['initial'] = sites[0]
                kwargs['queryset'] = sites
        return super(PageAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Page, PageAdmin)