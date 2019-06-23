# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-06-23 04:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fav_books_app', '0003_auto_20190622_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='uploaded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='fav_books_app.User'),
        ),
    ]
