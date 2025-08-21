# -*- coding: utf-8 -*-

import sys

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import translation
from django.utils.datetime_safe import datetime

from apps.merovingian.models import Course


class Command(BaseCommand):
    args = '<command> <course_id> <year>]'
    help = 'Moves course from one year to another'

    def force_save_course(self, course):
        """
        Goes though all course descendants (subjects, modules) and saves them to update didactic offer.
        """
        for sgroup in course.sgroups.all():
            sgroup.name += ' '
            sgroup.save()
            for module in sgroup.modules.all():
                module.name += ' '
                module.save()
                for subject in module.subjects.all():
                    subject.name += ' '
                    subject.save()

    @transaction.atomic()
    def handle(self, *args, **options):
        
        translation.activate('pl')
        
        if len(args) != 2:
            raise CommandError('Wrong number of parameters. Expected 2: ' + self.args)
        
        new_year = int(args[1])
        course_id = int(args[0])
        
        course = Course.objects.get(pk=course_id)
        
        if not course.start_date:
            raise CommandError('Course does not have start_date filled in')
        
        if course.start_date.year != new_year:
            
            new_date = datetime(year=new_year, month=course.start_date.month, day=course.start_date.day)
            course.start_date = new_date.date()
            course.save() 
            self.force_save_course(course)
        
        

