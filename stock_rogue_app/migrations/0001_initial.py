# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-15 20:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dane',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('kurs_otwarcia', models.FloatField()),
                ('kurs_max', models.FloatField()),
                ('kurs_min', models.FloatField()),
                ('kurs_biezacy', models.FloatField()),
                ('obrot', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Spolka',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skrot', models.CharField(max_length=50, unique=True)),
                ('typ', models.CharField(choices=[('SP', 'Spółka'), ('IN', 'Indeks'), ('OT', 'Inne')], default='OT', max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='dane',
            name='spolka',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_rogue_app.Spolka'),
        ),
        migrations.AlterUniqueTogether(
            name='dane',
            unique_together=set([('spolka', 'data')]),
        ),
    ]
