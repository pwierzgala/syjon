# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import translation

import syjon
from apps.merovingian.models import Course


class Command(BaseCommand):
    args = ''
    help = "Refresh courses' assignation to didactic offers"
    
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

    def handle(self, *args, **options):
        
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))
        
        verbosity = options.get('verbosity', 1)
        
        courses = Course.objects.active()
        for m in courses:
            with transaction.atomic():
                if verbosity > 1:
                    print(str(m))
                self.force_save_course(m)