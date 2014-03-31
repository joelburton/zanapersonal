from django.db import models
from ckeditor.fields import RichTextField
from django.db.models import permalink
import django.contrib.auth

import imagekit.models

from pilkit.processors import ResizeToFit


STYLESHEET_NAMES = [
    'Amelia',
    'Cerulean',
    'Cosmo',
    'Cyborg',
    'Flatly',
    'Journal',
    'Lumen',
    'Readable',
    'Simplex',
    'Slate',
    'Spacelab',
    'Superhero',
    'United',
    'Yeti',
    'Darkly',
]

STYLESHEET_URL = "http://netdna.bootstrapcdn.com/bootswatch/3.1.1/%s/bootstrap.min.css"

STYLESHEET_CHOICES = [(STYLESHEET_URL % s.lower(), s) for s in STYLESHEET_NAMES]


class Website(models.Model):
    """Personal website."""

    title = models.CharField(
        max_length=50,
        help_text="Title of the website."
    )

    domain = models.CharField(
        max_length=100,
        help_text="Domain name to use for this site.",
        unique=True,
    )

    stylesheet = models.CharField(
        max_length=100,
        choices=STYLESHEET_CHOICES,
        help_text="You can see <a href='http://www.bootstrapcdn.com/#bootswatch_tab'"
                  " target='_blank'>examples of these styles</a>",
        default=STYLESHEET_CHOICES[0],
    )

    name = models.CharField(
        max_length=30,
        blank=True,
        help_text="Your name, as it should appear at the top of your bio block.",
    )

    headshot = imagekit.models.ProcessedImageField(
        max_length=200,
        upload_to="headshot",
        processors=[ResizeToFit(150, 200)],
        format='JPEG',
        options={'quality': 80},
        blank=True,
        help_text='This will be resized to be 150 wide by 200 high.',
    )

    bio = RichTextField(
        blank=True,
        help_text="Bio block for page. This should include contact links, if you'd like."
    )

    twitter = models.CharField(
        max_length=64,
        blank=True,
        help_text="Your twitter handle."
    )

    footer = RichTextField(
        blank=True,
        help_text="Footer that will appear at the bottom of pages.",
    )

    css = models.TextField(
        verbose_name="custom CSS",
        help_text="Custom CSS for this site (for advanced users).",
        blank=True,
    )

    homepage_title = models.CharField(
        verbose_name='title',
        max_length=100,
        default='Welcome to My Site',
    )

    homepage_description = models.TextField(
        verbose_name='description',
        blank=True,
    )

    homepage_body = RichTextField(
        verbose_name='body',
        blank=True,
    )

    users = models.ManyToManyField(
        django.contrib.auth.get_user_model(),
        verbose_name='editors',
        help_text='Select users that can edit this site.',
    )

    @permalink
    def get_absolute_url(self):
        return "website.detail", (), {}

    def get_admin_url(self):
        return "/-settings/"

    def __unicode__(self):
        return self.title


class Page(models.Model):
    website = models.ForeignKey(
        Website,
    )

    title = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        blank=True,
        help_text='Appears at the top of the page.'
    )

    body = RichTextField(
        blank=True,
    )

    navigation_title = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default=None,
        help_text='Title of page as it appears in navigation. Leave blank to not show in navbar.',
    )

    slug = models.SlugField(
        help_text='Name of page as it appears in URL.',
    )

    priority = models.PositiveSmallIntegerField(
        default=100,
        help_text='Order of page (lower appear first).'
    )

    published = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ['priority', 'id']
        unique_together = [
            ('title', 'website'),
            ('navigation_title', 'website'),
            ('slug', 'website'),
        ]

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return "page.detail", (), {'slug': self.slug}

    @permalink
    def get_admin_url(self):
        return "page.update", (), {'slug': self.slug}



