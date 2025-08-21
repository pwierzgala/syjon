# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import translation

import syjon
from apps.merovingian.models import Course


class Command(BaseCommand):
    args = '<course_id>'
    help = "Refresh course assignation to didactic offer"
    
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
        
        if len(args) != 1:
            raise CommandError('Wrong number of parameters. Expected: ' + self.args)
        
        course = Course.objects.get(pk=int(args[0]))
        verbosity = options.get('verbosity',1)
        
        with transaction.atomic():
            if verbosity > 1:
                print(str(course))
            self.force_save_course(course)
        
        
        
        

