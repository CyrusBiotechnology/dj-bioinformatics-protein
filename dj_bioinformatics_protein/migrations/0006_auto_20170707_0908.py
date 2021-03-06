# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-07 09:08
from __future__ import unicode_literals

import dj_bioinformatics_protein.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_bioinformatics_protein', '0005_auto_20170627_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alignment',
            name='modified_query_aln_seq',
            field=dj_bioinformatics_protein.fields.AminoAcidAlignmentTextField(max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='alignment',
            name='modified_target_aln_seq',
            field=dj_bioinformatics_protein.fields.AminoAcidAlignmentTextField(max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='alignment',
            name='query_aln_seq',
            field=dj_bioinformatics_protein.fields.AminoAcidAlignmentTextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='alignment',
            name='target_aln_seq',
            field=dj_bioinformatics_protein.fields.AminoAcidAlignmentTextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='alignment',
            name='target_description',
            field=models.TextField(max_length=1000, null=True),
        ),
    ]
