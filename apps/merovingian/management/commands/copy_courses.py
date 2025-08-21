# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import translation
from django.utils.datetime_safe import datetime

import syjon
from apps.merovingian.management.commands.copy_course import \
    Command as CopyCommand
from apps.merovingian.models import Course


class Command(BaseCommand):
    args = '<year_from> <year_to>'
    help = 'Copies all courses from one year to another'

    def handle(self, *args, **options):
        
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))
        
        if len(args) != 2:
            raise CommandError('Wrong number of parameters. Expected 2: ' + self.args)
        
        old_year = int(args[0])
        new_year = int(args[1])

        if old_year == new_year:
            raise CommandError('Years must be different.')

        date_from = datetime(year=old_year, month=1, day=1)
        date_to = datetime(year=old_year+1, month=1, day=1)
        
        courses = Course.objects.active().filter(start_date__lt=date_to, start_date__gte=date_from).all()
        
        cp = CopyCommand()
        
        for m in courses:
            cp.copy_course(m, new_year)
        
        
        
        

