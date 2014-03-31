# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Website'
        db.create_table(u'personalpage_website', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('domain', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('stylesheet', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('headshot', self.gf('imagekit.models.fields.ProcessedImageField')(max_length=200, blank=True)),
            ('bio', self.gf('ckeditor.fields.RichTextField')(blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('footer', self.gf('ckeditor.fields.RichTextField')(blank=True)),
            ('css', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('homepage_title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('homepage_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('homepage_body', self.gf('ckeditor.fields.RichTextField')()),
        ))
        db.send_create_signal(u'personalpage', ['Website'])

        # Adding M2M table for field users on 'Website'
        m2m_table_name = db.shorten_name(u'personalpage_website_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('website', models.ForeignKey(orm[u'personalpage.website'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['website_id', 'user_id'])

        # Adding model 'Page'
        db.create_table(u'personalpage_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('website', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['personalpage.Website'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('body', self.gf('ckeditor.fields.RichTextField')(blank=True)),
            ('navigation_title', self.gf('django.db.models.fields.CharField')(default=None, max_length=20, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('priority', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=100)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'personalpage', ['Page'])

        # Adding unique constraint on 'Page', fields ['title', 'website']
        db.create_unique(u'personalpage_page', ['title', 'website_id'])

        # Adding unique constraint on 'Page', fields ['navigation_title', 'website']
        db.create_unique(u'personalpage_page', ['navigation_title', 'website_id'])

        # Adding unique constraint on 'Page', fields ['slug', 'website']
        db.create_unique(u'personalpage_page', ['slug', 'website_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Page', fields ['slug', 'website']
        db.delete_unique(u'personalpage_page', ['slug', 'website_id'])

        # Removing unique constraint on 'Page', fields ['navigation_title', 'website']
        db.delete_unique(u'personalpage_page', ['navigation_title', 'website_id'])

        # Removing unique constraint on 'Page', fields ['title', 'website']
        db.delete_unique(u'personalpage_page', ['title', 'website_id'])

        # Deleting model 'Website'
        db.delete_table(u'personalpage_website')

        # Removing M2M table for field users on 'Website'
        db.delete_table(db.shorten_name(u'personalpage_website_users'))

        # Deleting model 'Page'
        db.delete_table(u'personalpage_page')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'personalpage.page': {
            'Meta': {'ordering': "['priority', 'id']", 'unique_together': "[('title', 'website'), ('navigation_title', 'website'), ('slug', 'website')]", 'object_name': 'Page'},
            'body': ('ckeditor.fields.RichTextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'navigation_title': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '100'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['personalpage.Website']"})
        },
        u'personalpage.website': {
            'Meta': {'object_name': 'Website'},
            'bio': ('ckeditor.fields.RichTextField', [], {'blank': 'True'}),
            'css': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'footer': ('ckeditor.fields.RichTextField', [], {'blank': 'True'}),
            'headshot': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '200', 'blank': 'True'}),
            'homepage_body': ('ckeditor.fields.RichTextField', [], {}),
            'homepage_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'homepage_title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'stylesheet': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['personalpage']