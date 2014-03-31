from django.contrib import admin

from .models import Website, Page
from .views import PageCreationView


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
            )}),
        ('Appearance', {
            'fields': (
                'stylesheet',
                'css',
            )}),
        ('Homepage', {
            'fields': (
                'homepage_title',
                'homepage_description',
                'homepage_body',
            )})
    )

    list_display = ('title', 'domain', 'name')

    list_display_links = ('title', 'domain', 'name')

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
            )}),
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