# Generated by Django 3.0.5 on 2020-05-03 22:14

import colorful.fields
from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('blogApp', '0015_auto_20200503_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=colorful.fields.RGBColorField(default='1183db'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
