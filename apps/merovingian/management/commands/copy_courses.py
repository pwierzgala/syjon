from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import translation

import syjon
from apps.merovingian.management.commands.copy_course import \
    Command as CopyCommand
from apps.merovingian.models import Course


class Command(BaseCommand):
    help = 'Copies all courses from one year to another'

    def add_arguments(self, parser):
        parser.add_argument('year_from', type=int, help='Year to copy courses from')
        parser.add_argument('year_to', type=int, help='Year to copy courses to')

    def handle(self, *args, **options):
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))

        old_year = options['year_from']
        new_year = options['year_to']

        if old_year == new_year:
            raise CommandError('Years must be different.')

        date_from = datetime(year=old_year, month=1, day=1)
        date_to = datetime(year=old_year+1, month=1, day=1)
        
        courses = Course.objects.active().filter(start_date__lt=date_to, start_date__gte=date_from).all()
        
        cp = CopyCommand()
        
        for m in courses:
            cp.copy_course(m, new_year)
