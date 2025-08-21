# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
from django.conf import settings
from django.db import migrations, models

import apps.syjon.lib.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name')),
                ('name_pl', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name')),
                ('name_en', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name')),
                ('name_ua', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name')),
                ('name_ru', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name')),
                ('department', models.ForeignKey(null=True, to='trainman.Department', blank=True, verbose_name='Superior unit', related_name='+')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Unit',
                'verbose_name_plural': 'Units',
            },
        ),
        migrations.CreateModel(
            name='DepartmentType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], unique=True, max_length=256, verbose_name='Name')),
                ('name_pl', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name', unique=True)),
                ('name_en', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name', unique=True)),
                ('name_ua', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name', unique=True)),
                ('name_ru', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name', unique=True)),
            ],
            options={
                'verbose_name': 'Unit type',
                'verbose_name_plural': 'Unit types',
            },
        ),
        migrations.CreateModel(
            name='IdentityDocument',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], unique=True, max_length=256, verbose_name='Name')),
                ('name_pl', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name', unique=True)),
                ('name_en', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name', unique=True)),
                ('name_ua', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name', unique=True)),
                ('name_ru', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name', unique=True)),
            ],
            options={
                'verbose_name': 'ID document',
                'verbose_name_plural': 'ID documents',
            },
        ),
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('name_pl', models.CharField(null=True, max_length=256, verbose_name='Name')),
                ('name_en', models.CharField(null=True, max_length=256, verbose_name='Name')),
                ('name_ua', models.CharField(null=True, max_length=256, verbose_name='Name')),
                ('name_ru', models.CharField(null=True, max_length=256, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Occupation',
                'verbose_name_plural': 'Occupations',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('registration_number', models.CharField(max_length=16, verbose_name='Registration number')),
                ('legitimation_number_phd', models.CharField(max_length=16, verbose_name='PhD legitimation number')),
            ],
            options={
                'ordering': ('user_profile__user__last_name',),
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
            ],
            options={
                'ordering': ('user_profile__user__last_name',),
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
            },
        ),
        migrations.CreateModel(
            name='TeacherDegree',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name')),
                ('name_pl', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name')),
                ('name_en', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name')),
                ('name_ua', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name')),
                ('name_ru', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Degree',
                'verbose_name_plural': 'Deegrees',
            },
        ),
        migrations.CreateModel(
            name='TeacherPosition',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name')),
                ('name_pl', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name')),
                ('name_en', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name')),
                ('name_ua', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name')),
                ('name_ru', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(2), apps.syjon.lib.validators.validate_white_space], max_length=256, verbose_name='Name')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Position',
                'verbose_name_plural': 'Positions',
            },
        ),
        migrations.CreateModel(
            name='UserOccupation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('start_date', models.DateField(null=True, blank=True, verbose_name='start date')),
                ('end_date', models.DateField(null=True, blank=True, verbose_name='end date')),
                ('department', models.ForeignKey(null=True, to='trainman.Department', blank=True, verbose_name='Unit')),
                ('occupation', models.ForeignKey(null=True, to='trainman.Occupation', blank=True, verbose_name='Occupation')),
            ],
            options={
                'verbose_name': 'User Position',
                'verbose_name_plural': 'Users Positions',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('second_name', models.CharField(null=True, max_length=128, blank=True, verbose_name='Middle name')),
                ('pesel', models.CharField(null=True, validators=[django.core.validators.MinLengthValidator(10)], max_length=11, blank=True, verbose_name='PESEL')),
                ('department', models.ForeignKey(null=True, to='trainman.Department', blank=True, verbose_name='Unit')),
                ('managed_departments', models.ManyToManyField(related_name='managed_departments', to='trainman.Department', blank=True, verbose_name='Zarządzane jednostki')),
                ('managed_users', models.ManyToManyField(related_name='_userprofile_managed_users_+', to='trainman.UserProfile', blank=True, verbose_name='Zarządzani użytkownicy')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ('user__last_name',),
                'verbose_name': 'User profile',
                'verbose_name_plural': 'User profiles',
            },
        ),
        migrations.AddField(
            model_name='useroccupation',
            name='user_profile',
            field=models.ForeignKey(verbose_name='User', to='trainman.UserProfile'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='degree',
            field=models.ForeignKey(verbose_name='Degree', to='trainman.TeacherDegree'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='position',
            field=models.ForeignKey(verbose_name='Position', to='trainman.TeacherPosition'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='user_profile',
            field=models.OneToOneField(to='trainman.UserProfile', verbose_name='User'),
        ),
        migrations.AddField(
            model_name='student',
            name='user_profile',
            field=models.OneToOneField(to='trainman.UserProfile', verbose_name='User'),
        ),
        migrations.AddField(
            model_name='department',
            name='type',
            field=models.ForeignKey(null=True, to='trainman.DepartmentType', blank=True, verbose_name='Type'),
        ),
    ]
