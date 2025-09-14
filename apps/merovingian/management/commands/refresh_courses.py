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
        for course in (pbar := tqdm(courses)):
            pbar.set_description(f'{course}')
            self.force_save_course(course)

    def force_save_course(self, course):
        """
        Goes through all course descendants (subjects, modules) and saves them to update didactic
        offer.
        """
        course.save()
        for sgroup in (sgroup_pbar := tqdm(course.sgroups.all(), leave=False)):
            sgroup_pbar.set_description(f'{sgroup.name}')
            sgroup.save()
            for module in (module_pbar := tqdm(sgroup.modules.all(), leave=False)):
                module_pbar.set_description(f'{module.name}')
                module.save()
                for subject in (subject_pbar := tqdm(module.subjects.all(), leave=False)):
                    subject_pbar.set_description(f'{subject.name}')
                    subject.save()
