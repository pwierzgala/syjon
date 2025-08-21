# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merovingian', '0001_initial'),
        ('trinity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='education_areas',
            field=models.ManyToManyField(to='trinity.EducationArea', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='education_disciplines',
            field=models.ManyToManyField(to='trinity.EducationDiscipline', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='education_fields',
            field=models.ManyToManyField(to='trinity.EducationField', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='knowledge_areas',
            field=models.ManyToManyField(to='trinity.KnowledgeArea', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='level',
            field=models.ForeignKey(verbose_name='Education level', to='merovingian.CourseLevel'),
        ),
        migrations.AddField(
            model_name='course',
            name='profile',
            field=models.ForeignKey(null=True, to='merovingian.CourseProfile', blank=True, verbose_name='Education profile'),
        ),
        migrations.AddField(
            model_name='course',
            name='type',
            field=models.ForeignKey(verbose_name='Typ', to='merovingian.CourseType'),
        ),
        migrations.AlterUniqueTogether(
            name='moduleproperties',
            unique_together=set([('semester', 'module', 'type')]),
        ),
    ]
