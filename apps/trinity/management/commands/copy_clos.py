"""
Created on 27-08-2012

@author: pwierzgala
"""

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import termcolors, translation

import syjon
from apps.merovingian.models import Course
from apps.trinity.models import CourseLearningOutcome

green = termcolors.make_style(fg='green')
yellow = termcolors.make_style(fg='yellow')
cyan = termcolors.make_style(fg='cyan')
red = termcolors.make_style(fg='red', opts=('bold',))
bold = termcolors.make_style(opts=('bold',))

class Command(BaseCommand):
    help = u'Copies course learning outcomes from one course to other'

    def add_arguments(self, parser):
        parser.add_argument('course_from', type=int, help='ID of the source course')
        parser.add_argument('course_to', type=int, help='ID of the target course')


    @transaction.atomic()
    def handle(self, *args, **options):
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))

        id_course_from = options['course_from']
        id_course_to = options['course_to']

        # Getting courses
        try:
            course_from = Course.objects.get(id = id_course_from)
            print('ID course from: %s (%s)' % (str(course_from).encode('utf-8'), str(course_from.id).encode('utf-8')))
        except Course.DoesNotExist:
            raise CommandError('Course does not exist: %s' % str(course_from).encode('utf-8'))
        
        try:
            course_to = Course.objects.get(id = id_course_to)
            print('ID course to: %s (%s)' % (str(course_to).encode('utf-8'), str(course_to.id).encode('utf-8')))
        except:
            raise CommandError('Course does not exist: %s\n' % str(course_to).encode('utf-8'))
        
        print('')

        # Removing course learning outcomes from course_to
        clos_to = CourseLearningOutcome.objects.filter(course = course_to)
        clos_to.delete()
        print(green('Learning outcomes for course: %s (id: %s) have been removed' % (str(course_to).encode('utf-8'), course_to.id)))
        
        # Copying course learning outcomes from courst_from to course_to
        clos_from = CourseLearningOutcome.objects.filter(course = course_from)
        for clo in clos_from:
            alos_from = clo.alos
            
            clo.pk = None
            clo.course = course_to
            clo.save()
            print(green('\tCourse learing outcome: %s (id: %s) has been copied' % (str(clo.symbol).encode('utf-8'), clo.id)))
            
            # Copying area learning outcomes
            for alo_from in alos_from.all():
                clo.alos.add(alo_from)
                print(yellow('\t\tArea learning outcomes has been copied "%s" (id: %s)' % (str(alo_from.symbol).encode('utf-8'), alo_from.id)))
            
            print('')
