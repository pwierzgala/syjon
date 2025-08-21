# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import apps.syjon.lib.validators


class Migration(migrations.Migration):

    dependencies = [
        ('merovingian', '0001_initial'),
        ('trainman', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaLearningOutcome',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('symbol', models.CharField(validators=[apps.syjon.lib.validators.validate_white_space], max_length=16)),
                ('symbol_pl', models.CharField(null=True, validators=[apps.syjon.lib.validators.validate_white_space], max_length=16)),
                ('symbol_en', models.CharField(null=True, validators=[apps.syjon.lib.validators.validate_white_space], max_length=16)),
                ('symbol_ua', models.CharField(null=True, validators=[apps.syjon.lib.validators.validate_white_space], max_length=16)),
                ('symbol_ru', models.CharField(null=True, validators=[apps.syjon.lib.validators.validate_white_space], max_length=16)),
                ('description', models.TextField(validators=[apps.syjon.lib.validators.validate_white_space])),
                ('description_pl', models.TextField(null=True, validators=[apps.syjon.lib.validators.validate_white_space])),
                ('description_en', models.TextField(null=True, validators=[apps.syjon.lib.validators.validate_white_space])),
                ('description_ua', models.TextField(null=True, validators=[apps.syjon.lib.validators.validate_white_space])),
                ('description_ru', models.TextField(null=True, validators=[apps.syjon.lib.validators.validate_white_space])),
            ],
            options={
                'ordering': ('symbol',),
                'verbose_name': 'Area learning outcome',
                'verbose_name_plural': 'Area learning outcomes',
            },
        ),
        migrations.CreateModel(
            name='CourseLearningOutcome',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('symbol', models.CharField(validators=[apps.syjon.lib.validators.validate_white_space], max_length=16)),
                ('symbol_pl', models.CharField(null=True, validators=[apps.syjon.lib.validators.validate_white_space], max_length=16)),
                ('symbol_en', models.CharField(null=True, validators=[apps.syjon.lib.validators.validate_white_space], max_length=16)),
                ('symbol_ua', models.CharField(null=True, validators=[apps.syjon.lib.validators.validate_white_space], max_length=16)),
                ('symbol_ru', models.CharField(null=True, validators=[apps.syjon.lib.validators.validate_white_space], max_length=16)),
                ('description', models.TextField(validators=[apps.syjon.lib.validators.validate_white_space])),
                ('description_pl', models.TextField(null=True, validators=[apps.syjon.lib.validators.validate_white_space])),
                ('description_en', models.TextField(null=True, validators=[apps.syjon.lib.validators.validate_white_space])),
                ('description_ua', models.TextField(null=True, validators=[apps.syjon.lib.validators.validate_white_space])),
                ('description_ru', models.TextField(null=True, validators=[apps.syjon.lib.validators.validate_white_space])),
                ('alos', models.ManyToManyField(related_name='clos', to='trinity.AreaLearningOutcome')),
                ('course', models.ForeignKey(related_name='clos', to='merovingian.Course')),
            ],
            options={
                'ordering': ('symbol',),
                'verbose_name': 'Course learning outcome',
                'verbose_name_plural': 'Course learning outcomes',
            },
        ),
        migrations.CreateModel(
            name='EducationArea',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('name_pl', models.CharField(null=True, max_length=255)),
                ('name_en', models.CharField(null=True, max_length=255)),
                ('name_ua', models.CharField(null=True, max_length=255)),
                ('name_ru', models.CharField(null=True, max_length=255)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Area of education',
                'verbose_name_plural': 'Areas of education',
            },
        ),
        migrations.CreateModel(
            name='EducationCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('name_pl', models.CharField(null=True, max_length=255)),
                ('name_en', models.CharField(null=True, max_length=255)),
                ('name_ua', models.CharField(null=True, max_length=255)),
                ('name_ru', models.CharField(null=True, max_length=255)),
            ],
            options={
                'ordering': ('-name',),
                'verbose_name': 'Education category',
                'verbose_name_plural': 'Education categories',
            },
        ),
        migrations.CreateModel(
            name='EducationDiscipline',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('name_pl', models.CharField(null=True, max_length=255)),
                ('name_en', models.CharField(null=True, max_length=255)),
                ('name_ua', models.CharField(null=True, max_length=255)),
                ('name_ru', models.CharField(null=True, max_length=255)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Discipline of science',
                'verbose_name_plural': 'Disciplines of science',
            },
        ),
        migrations.CreateModel(
            name='EducationField',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('name_pl', models.CharField(null=True, max_length=255)),
                ('name_en', models.CharField(null=True, max_length=255)),
                ('name_ua', models.CharField(null=True, max_length=255)),
                ('name_ru', models.CharField(null=True, max_length=255)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Field of science',
                'verbose_name_plural': 'Fields of science',
            },
        ),
        migrations.CreateModel(
            name='KnowledgeArea',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('name_pl', models.CharField(null=True, max_length=255)),
                ('name_en', models.CharField(null=True, max_length=255)),
                ('name_ua', models.CharField(null=True, max_length=255)),
                ('name_ru', models.CharField(null=True, max_length=255)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Area of knowledge',
                'verbose_name_plural': 'Areas of knowledge',
            },
        ),
        migrations.CreateModel(
            name='ModuleLearningOutcome',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('symbol', models.CharField(validators=[apps.syjon.lib.validators.validate_white_space], max_length=16)),
                ('symbol_pl', models.CharField(null=True, validators=[apps.syjon.lib.validators.validate_white_space], max_length=16)),
                ('symbol_en', models.CharField(null=True, validators=[apps.syjon.lib.validators.validate_white_space], max_length=16)),
                ('symbol_ua', models.CharField(null=True, validators=[apps.syjon.lib.validators.validate_white_space], max_length=16)),
                ('symbol_ru', models.CharField(null=True, validators=[apps.syjon.lib.validators.validate_white_space], max_length=16)),
                ('description', models.TextField(validators=[apps.syjon.lib.validators.validate_white_space])),
                ('description_pl', models.TextField(null=True, validators=[apps.syjon.lib.validators.validate_white_space])),
                ('description_en', models.TextField(null=True, validators=[apps.syjon.lib.validators.validate_white_space])),
                ('description_ua', models.TextField(null=True, validators=[apps.syjon.lib.validators.validate_white_space])),
                ('description_ru', models.TextField(null=True, validators=[apps.syjon.lib.validators.validate_white_space])),
                ('clos', models.ManyToManyField(related_name='mlos', to='trinity.CourseLearningOutcome')),
                ('module', models.ForeignKey(related_name='mlos', to='merovingian.Module')),
            ],
            options={
                'ordering': ('symbol',),
                'verbose_name': 'Module learning outcome',
                'verbose_name_plural': 'Module learning outcomes',
            },
        ),
        migrations.CreateModel(
            name='TrinityProfile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('courses', models.ManyToManyField(to='merovingian.Course', blank=True)),
                ('user_profile', models.OneToOneField(to='trainman.UserProfile', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Administrator',
                'verbose_name_plural': 'Administrators',
            },
        ),
        migrations.AddField(
            model_name='educationfield',
            name='knowledge_area',
            field=models.ForeignKey(to='trinity.KnowledgeArea'),
        ),
        migrations.AddField(
            model_name='educationdiscipline',
            name='education_field',
            field=models.ForeignKey(null=True, to='trinity.EducationField', blank=True),
        ),
        migrations.AddField(
            model_name='courselearningoutcome',
            name='education_category',
            field=models.ForeignKey(to='trinity.EducationCategory'),
        ),
        migrations.AddField(
            model_name='arealearningoutcome',
            name='education_area',
            field=models.ForeignKey(to='trinity.EducationArea'),
        ),
        migrations.AddField(
            model_name='arealearningoutcome',
            name='education_category',
            field=models.ForeignKey(to='trinity.EducationCategory'),
        ),
        migrations.AddField(
            model_name='arealearningoutcome',
            name='education_level',
            field=models.ForeignKey(to='merovingian.CourseLevel'),
        ),
        migrations.AddField(
            model_name='arealearningoutcome',
            name='education_profile',
            field=models.ForeignKey(to='merovingian.CourseProfile'),
        ),
    ]
