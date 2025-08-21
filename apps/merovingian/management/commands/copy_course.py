# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import translation
from django.utils.datetime_safe import datetime

import syjon
from apps.merovingian.functions import default_sgroup_name
from apps.merovingian.models import Course, Module, SGroup, Subject


class Command(BaseCommand):
    args = '<course_id> <year>'
    help = 'Copies course from one year to another'

    def force_save_course(self, course):
        """
        Goes though all course descendants (subjects, modules) and saves them to update didactic offer.
        """
        course.name += ' '
        course.save()
        for sgroup in course.sgroups.all():
            sgroup.name += ' '
            sgroup.save()
            for module in sgroup.modules.all():
                module.name += ' '
                module.save()
                for subject in module.subjects.all():
                    subject.name += ' '
                    subject.save()

    def copy_course_descendants(self, old, new):
        """
        Goes though all course descendants (subjects, modules) and saves them to duplicate them.
        """
        for sgroup in old.sgroups.all():

            old_sgroup_pk = sgroup.pk
                        
            if sgroup.name == default_sgroup_name():
                new_sgroup = new.sgroups.all()[0]
            else:
                sgroup.pk = None
                sgroup.save()
                new_sgroup = sgroup
                
            old_sgroup = SGroup.objects.get(pk=old_sgroup_pk)
                
            new_modules = []
            
            for module in old_sgroup.modules.all():

                old_module_pk = module.pk

                module.pk = None
                module.save()
                new_module = module
                
                old_module = Module.objects.get(pk=old_module_pk)
            
                for subject in old_module.subjects.all():

                    old_subject_pk = subject.pk

                    subject.pk = None
                    subject.save()
                    new_subject = subject
                    
                    new_subject.module = new_module
                    new_subject.save()
                    
                    old_subject = Subject.objects.get(pk=old_subject_pk)
                    for subject_teacher in old_subject.subjecttoteacher_set.all():
                        subject_teacher.pk = None
                        subject_teacher.subject = new_subject
                        subject_teacher.save()
                        
                for properties in old_module.moduleproperties_set.all():
                    properties.pk = None
                    properties.module = new_module
                    properties.save()
                    
                new_modules.append(new_module)

            for m in new_modules:
                new_sgroup.modules.add(m)
                
            new_sgroup.course = new
            new_sgroup.save()
            
    @transaction.atomic()
    def copy_course(self, course, new_year):
        
        other_courses = course.get_courses()
        for m in other_courses:
            if m.start_date and m.start_date.year == new_year:
                print('Course {0} has already its didactic offer for year {1}'.format(course, str(new_year)))
                return
            
        old_pk = course.pk
        
        new_date = datetime(year=new_year, month=course.start_date.month, day=course.start_date.day)
        course.start_date = new_date.date()
        course.pk = None
        
        course.save()
        new = course
        old = Course.objects.get(pk=old_pk)

        # Copy admins
        for admin in old.merovingianadmin_set.all():
            if new not in admin.courses.all():
                admin.courses.add(new)
                admin.save() 

        self.copy_course_descendants(old, new)
        self.force_save_course(new)
        self.force_save_course(old)
        print('Copied course {0}'.format(old))
            
    def handle(self, *args, **options):
        
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))
        
        if len(args) != 2:
            raise CommandError('Wrong number of parameters. Expected 2: ' + self.args)
        
        new_year = int(args[1])
        course_id = int(args[0])
        
        course = Course.objects.get(pk=course_id)
        
        if not course.start_date:
            raise CommandError('Course does not have start_date filled in')

        if course.start_date.year == new_year:
            raise CommandError('Course is already on this year')
        
        self.copy_course(course, new_year)
