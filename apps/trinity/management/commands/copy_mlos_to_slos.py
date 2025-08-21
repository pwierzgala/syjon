# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import termcolors, translation
from tqdm import tqdm

import syjon
from apps.merovingian.models import Course
from apps.trinity.models import SubjectToModuleLearningOutcome

green = termcolors.make_style(fg='green')
yellow = termcolors.make_style(fg='yellow')
cyan = termcolors.make_style(fg='cyan')
red = termcolors.make_style(fg='red', opts=('bold',))
bold = termcolors.make_style(opts=('bold',))


class Command(BaseCommand):
    args = u'<course_id>'
    help = u'Copies module learning outcomes to subject learning outcomes'

    @staticmethod
    def get_course(course_id):
        try:
            course = Course.objects.get(id=course_id)
            print('ID course from: {} ({})'.format(course, course.id))
        except Course.DoesNotExist:
            raise CommandError("Course does not exist: {}".format(course_id))
        else:
            return course

    @staticmethod
    def copy(course):
        for sgroup in tqdm(course.sgroups.all()):
            for module in tqdm(sgroup.modules.all(), leave=False):
                for subject in tqdm(module.subjects.all(), leave=False):
                    SubjectToModuleLearningOutcome.objects.filter(subject=subject).delete()
                    for mlo in tqdm(module.mlos.all(), leave=False):
                        SubjectToModuleLearningOutcome.objects.create(subject=subject, mlo=mlo)

    @transaction.atomic()
    def handle(self, *args, **options):
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))
        course_id = args[0]
        course = self.get_course(course_id)
        self.copy(course=course)
        print('')




