# Generated by Django 5.1.3 on 2024-11-25 11:54

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_site', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='types',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('144p', '144p'), ('360p', '360p'), ('480p', '480p'), ('720p', '720p'), ('1080p', '1080p')], max_length=16),
        ),
    ]
