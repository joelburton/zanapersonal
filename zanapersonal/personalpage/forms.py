"""

"""
from django import forms

from .models import Website, Page


class WebsiteSettingsForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['title', 'domain', 'footer']


class WebsiteBiographicalForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['name', 'headshot', 'bio', 'twitter']


class WebsiteAppearanceForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['stylesheet', 'css']


class WebsiteHomepageForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['homepage_title', 'homepage_description', 'homepage_body']


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['website', 'title', 'slug', 'description', 'body', 'published', 'navigation_title', 'priority']
