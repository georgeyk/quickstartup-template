# coding: utf8


from __future__ import unicode_literals

from django.db import models, migrations

from ..bootstrap import bootstrap_website_pages


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name=b'Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'slug', models.SlugField(max_length=255, blank=b'')),
                (b'variation', models.IntegerField(default=0)),
                (b'template', models.CharField(max_length=255)),
                (b'login_required', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': set([(b'slug', b'variation')]),
                'index_together': set([(b'slug', b'variation')]),
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(bootstrap_website_pages)
    ]