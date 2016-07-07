# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-06 14:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0008_auto_20160706_0848'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sample',
            options={'ordering': ['-tmstp']},
        ),
        migrations.AlterField(
            model_name='sample',
            name='image_path',
            field=models.FilePathField(null=True, verbose_name='/home/l-brognoli/djangodev/fruitoscopy/frutopy/static/images'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='ml_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tables.ML_Model'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sp_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tables.SP_Model'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='sample',
            order_with_respect_to=None,
        ),
    ]