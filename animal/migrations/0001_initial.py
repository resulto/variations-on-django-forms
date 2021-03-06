# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-17 00:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('activities', models.ManyToManyField(blank=True, related_name='animals', to='animal.Activity')),
                ('favorite_activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favored_by_animals', to='animal.Activity')),
                ('internal_notes', models.TextField(blank=True, default="")),
            ],
        ),
        migrations.CreateModel(
            name='AnimalType',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='animal',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='animals', to='animal.AnimalType'),
        ),
        migrations.AddField(
            model_name='activity',
            name='animal_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='animal.AnimalType'),
        ),
    ]
