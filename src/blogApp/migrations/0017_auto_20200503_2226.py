# Generated by Django 3.0.5 on 2020-05-03 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0016_auto_20200503_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_on_view',
            field=models.ImageField(upload_to='public/articles/images/%m/%d'),
        ),
    ]
