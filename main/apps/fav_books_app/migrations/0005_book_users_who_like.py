# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-06-23 04:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fav_books_app', '0004_auto_20190622_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='users_who_like',
            field=models.ManyToManyField(related_name='liked_books', to='fav_books_app.User'),
        ),
    ]