# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sha256', models.CharField(max_length=255, unique=True, null=True, editable=False, blank=True)),
                ('alignment_method', models.CharField(max_length=100, choices=[(b'H', b'hhsearch'), (b'S', b'sparksX'), (b'U', b'user')])),
                ('rank', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('query_tag', models.CharField(max_length=255)),
                ('query_start', models.IntegerField()),
                ('query_aln_seq', models.TextField(max_length=5000)),
                ('modified_query_aln_seq', models.TextField(default=b'', max_length=5000)),
                ('target_tag', models.CharField(max_length=255)),
                ('target_pdb_code', models.CharField(max_length=4)),
                ('target_pdb_chain', models.CharField(max_length=1)),
                ('target_start', models.IntegerField()),
                ('target_aln_seq', models.TextField(max_length=5000)),
                ('modified_target_aln_seq', models.TextField(default=b'', max_length=5000)),
                ('p_correct', models.FloatField()),
                ('threaded_template', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FASTA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sha256', models.CharField(unique=True, max_length=255, editable=False, blank=True)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('comments', models.TextField(max_length=2000, null=True, blank=True)),
                ('sequence', models.TextField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='MultipleAlignments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('full_query_sequence', models.ForeignKey(to='dj_bioinformatics_protein.FASTA')),
            ],
        ),
        migrations.AddField(
            model_name='alignment',
            name='full_query_sequence',
            field=models.ForeignKey(to='dj_bioinformatics_protein.FASTA'),
        ),
        migrations.AddField(
            model_name='alignment',
            name='multiple_alignments',
            field=models.ForeignKey(to='dj_bioinformatics_protein.MultipleAlignments'),
        ),
    ]
