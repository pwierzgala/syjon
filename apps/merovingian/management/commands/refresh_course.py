from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import translation

import syjon
from apps.merovingian.models import Course


class Command(BaseCommand):
    help = 'Refresh course assignation to didactic offer'

    def add_arguments(self, parser):
        parser.add_argument('course_id', type=int)

    def handle(self, *args, **options):
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))
        course_id = options['course_id']
        course = Course.objects.get(pk=course_id)
        verbosity = options.get('verbosity', 1)

        with transaction.atomic():
            if verbosity > 1:
                print(str(course))
            self.force_save_course(course)
    
    def force_save_course(self, course):
        """
        Goes though all course descendants (subjects, modules) and saves them to update didactic offer.
        """
        course.save()
        for sgroup in course.sgroups.all():
            sgroup.save()
            for module in sgroup.modules.all():
                module.save()
                for subject in module.subjects.all():
                    subject.save()
