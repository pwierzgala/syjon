# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models

import apps.syjon.lib.validators


class Migration(migrations.Migration):

    dependencies = [
        ('trainman', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_pl', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_en', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_ua', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_ru', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('semesters', models.IntegerField(null=True, blank=True, verbose_name='Number of semesters')),
                ('years', models.IntegerField(null=True, blank=True, verbose_name='Number of years')),
                ('start_date', models.DateField(null=True, blank=True, verbose_name='Start date')),
                ('end_date', models.DateField(null=True, blank=True, verbose_name='End date')),
                ('is_first', models.NullBooleanField(default=None, verbose_name='First')),
                ('is_last', models.NullBooleanField(default=None, verbose_name='Last')),
                ('department', models.ForeignKey(null=True, to='trainman.Department', blank=True, verbose_name='Unit')),
            ],
            options={
                'ordering': ('-is_active', 'name', '-level__name', '-type__name', 'profile__name', 'start_date'),
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
                'permissions': (('assign_education_area_course', 'Can assign education area'),),
            },
        ),
        migrations.CreateModel(
            name='CourseLevel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], unique=True, max_length=256, verbose_name='name')),
                ('name_pl', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_en', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_ua', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_ru', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
            ],
            options={
                'verbose_name': 'Education level',
                'verbose_name_plural': 'Education levels',
            },
        ),
        migrations.CreateModel(
            name='CourseProfile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], unique=True, max_length=256, verbose_name='name')),
                ('name_pl', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_en', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_ua', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_ru', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
            ],
            options={
                'verbose_name': 'Education profile',
                'verbose_name_plural': 'Education profiles',
            },
        ),
        migrations.CreateModel(
            name='CourseType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], unique=True, max_length=256, verbose_name='name')),
                ('name_pl', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_en', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_ua', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_ru', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
            ],
            options={
                'verbose_name': 'Course type',
                'verbose_name_plural': 'Course types',
            },
        ),
        migrations.CreateModel(
            name='DidacticOffer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_pl', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_en', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_ua', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_ru', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('start_date', models.DateField(verbose_name='start date')),
                ('end_date', models.DateField(verbose_name='end date')),
            ],
            options={
                'verbose_name': 'Teaching offer',
                'verbose_name_plural': 'Teaching offers',
            },
        ),
        migrations.CreateModel(
            name='MerovingianAdmin',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('temporary_privileged_access', models.BooleanField(default=False, verbose_name='Temporary Privileged Access')),
                ('courses', models.ManyToManyField(to='merovingian.Course', blank=True, verbose_name='Managed courses')),
                ('user_profile', models.OneToOneField(to='trainman.UserProfile', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Merowing Administrator',
                'verbose_name_plural': 'Merowing Administrator',
            },
        ),
        migrations.CreateModel(
            name='MerovingianSettings',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('key', models.CharField(unique=True, max_length=32, verbose_name='key')),
                ('value', models.CharField(max_length=128, verbose_name='value')),
                ('value_pl', models.CharField(null=True, max_length=128, verbose_name='value')),
                ('value_en', models.CharField(null=True, max_length=128, verbose_name='value')),
                ('value_ua', models.CharField(null=True, max_length=128, verbose_name='value')),
                ('value_ru', models.CharField(null=True, max_length=128, verbose_name='value')),
            ],
            options={
                'verbose_name': 'Merowing Settings',
                'verbose_name_plural': 'Merowing Settings',
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_pl', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_en', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_ua', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_ru', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('ects', models.FloatField(null=True, blank=True, verbose_name='ECTS points')),
                ('internal_code', models.CharField(max_length=128, blank=True)),
                ('erasmus_code', models.CharField(max_length=128, blank=True)),
                ('isced_code', models.CharField(max_length=128, blank=True)),
                ('coordinator', models.ForeignKey(null=True, to='trainman.Teacher', blank=True, verbose_name='Teacher')),
                ('didactic_offer', models.ForeignKey(null=True, to='merovingian.DidacticOffer', blank=True, verbose_name='Teaching offer')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Module',
                'verbose_name_plural': 'Modules',
            },
        ),
        migrations.CreateModel(
            name='ModuleProperties',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('semester', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Semester/Year')),
                ('hours', models.FloatField(null=True, blank=True, verbose_name='Number of hours')),
                ('ects', models.FloatField(verbose_name='ECTS points')),
                ('module', models.ForeignKey(verbose_name='Module', to='merovingian.Module')),
            ],
            options={
                'ordering': ('semester',),
                'verbose_name': 'Module attributes',
                'verbose_name_plural': 'Module attributes',
            },
        ),
        migrations.CreateModel(
            name='ModuleType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], unique=True, max_length=256, verbose_name='name')),
                ('name_pl', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_en', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_ua', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_ru', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Module type',
                'verbose_name_plural': 'Module types',
            },
        ),
        migrations.CreateModel(
            name='SGroup',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_pl', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_en', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_ua', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_ru', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('start_semester', models.IntegerField(default=1, verbose_name='First semester/year')),
                ('course', models.ForeignKey(to='merovingian.Course', verbose_name='Course', related_name='sgroups')),
                ('didactic_offer', models.ForeignKey(null=True, to='merovingian.DidacticOffer', blank=True, verbose_name='Teaching offer')),
                ('sgroup', models.ForeignKey(null=True, to='merovingian.SGroup', blank=True, verbose_name='Parent subjects group', related_name='+')),
            ],
            options={
                'ordering': ('-is_active', '-type', 'name'),
                'verbose_name': 'Subjects group',
                'verbose_name_plural': 'Subjects groups',
            },
        ),
        migrations.CreateModel(
            name='SGroupType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], unique=True, max_length=256, verbose_name='name')),
                ('name_pl', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_en', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_ua', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_ru', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
            ],
            options={
                'verbose_name': 'Type of subjects group',
                'verbose_name_plural': 'Types of subjects group',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_pl', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_en', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_ua', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('name_ru', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('hours', models.FloatField(verbose_name='Number of hours')),
                ('semester', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Semester/Year')),
                ('ects', models.FloatField(null=True, blank=True, verbose_name='ECTS points')),
                ('internal_code', models.CharField(max_length=128, blank=True)),
            ],
            options={
                'ordering': ('semester', 'name', '-type', 'assessment'),
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
            },
        ),
        migrations.CreateModel(
            name='SubjectAssessment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], unique=True, max_length=256, verbose_name='name')),
                ('name_pl', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_en', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_ua', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_ru', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Type of pass',
                'verbose_name_plural': 'Types of pass',
            },
        ),
        migrations.CreateModel(
            name='SubjectToTeacher',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('groups', models.IntegerField(verbose_name='Number of groups')),
                ('hours', models.FloatField(max_length=3, verbose_name='Number of hours')),
                ('description', models.CharField(null=True, max_length=512, blank=True, verbose_name='Description')),
                ('subject', models.ForeignKey(verbose_name='Subject', to='merovingian.Subject')),
                ('teacher', models.ForeignKey(verbose_name='Teacher', to='trainman.Teacher')),
            ],
            options={
                'verbose_name': 'Subject - Teacher',
                'verbose_name_plural': 'Subjects - Teachers',
            },
        ),
        migrations.CreateModel(
            name='SubjectType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], unique=True, max_length=256, verbose_name='name')),
                ('name_pl', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_en', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_ua', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
                ('name_ru', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='name', unique=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Type of classes',
                'verbose_name_plural': 'Types of classes',
            },
        ),
        migrations.AddField(
            model_name='subject',
            name='assessment',
            field=models.ForeignKey(verbose_name='Type of pass', to='merovingian.SubjectAssessment'),
        ),
        migrations.AddField(
            model_name='subject',
            name='didactic_offer',
            field=models.ForeignKey(null=True, to='merovingian.DidacticOffer', blank=True, verbose_name='Teaching offer'),
        ),
        migrations.AddField(
            model_name='subject',
            name='module',
            field=models.ForeignKey(to='merovingian.Module', verbose_name='Module', related_name='subjects'),
        ),
        migrations.AddField(
            model_name='subject',
            name='teachers',
            field=models.ManyToManyField(to='trainman.Teacher', through='merovingian.SubjectToTeacher', blank=True, verbose_name='Teachers'),
        ),
        migrations.AddField(
            model_name='subject',
            name='type',
            field=models.ForeignKey(verbose_name='Type of classes', to='merovingian.SubjectType'),
        ),
        migrations.AddField(
            model_name='sgroup',
            name='type',
            field=models.ForeignKey(verbose_name='Type', to='merovingian.SGroupType'),
        ),
        migrations.AddField(
            model_name='moduleproperties',
            name='type',
            field=models.ForeignKey(null=True, to='merovingian.SubjectType', blank=True, verbose_name='Type of classes'),
        ),
        migrations.AddField(
            model_name='module',
            name='sgroup',
            field=models.ForeignKey(null=True, to='merovingian.SGroup', related_name='modules'),
        ),
        migrations.AddField(
            model_name='module',
            name='type',
            field=models.ForeignKey(null=True, to='merovingian.ModuleType', blank=True, verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='course',
            name='didactic_offer',
            field=models.ForeignKey(null=True, to='merovingian.DidacticOffer', blank=True, verbose_name='Teaching offer'),
        ),
    ]
