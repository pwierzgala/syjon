from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation
from tqdm import tqdm

import syjon
from apps.merovingian.models import Course


class Command(BaseCommand):
    help = 'Refresh course assignment to didactic offers'

    def handle(self, *args, **options):
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))

        courses = Course.objects.active()
        for course in tqdm(courses, desc='Courses', unit='course'):
            self.force_save_course(course)

    def force_save_course(self, course):
        """
        Goes through all course descendants (subjects, modules) and saves them to update didactic
        offer.
        """
        course.save()
        for sgroup in tqdm(
                course.sgroups.all(), desc=f'{course}', leave=False):
            sgroup.save()
            for module in tqdm(sgroup.modules.all(), desc=f'{sgroup.name}', leave=False):
                module.save()
                for subject in tqdm(module.subjects.all(), desc=f'{module.name}', leave=False):
                    subject.save()
