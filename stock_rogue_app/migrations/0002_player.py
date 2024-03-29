# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-29 10:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock_rogue_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.FloatField()),
                ('last_played_company1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='1+', to='stock_rogue_app.Spolka')),
                ('last_played_company2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='2+', to='stock_rogue_app.Spolka')),
                ('last_played_company3', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='3+', to='stock_rogue_app.Spolka')),
                ('last_played_company4', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='4+', to='stock_rogue_app.Spolka')),
                ('last_played_company5', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='5+', to='stock_rogue_app.Spolka')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
