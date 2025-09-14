from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import translation

from apps.merovingian.models import Course


class Command(BaseCommand):
    help = 'Moves course from one year to another'

    def add_arguments(self, parser):
        parser.add_argument('course_id', type=int, help='ID of the course to move')
        parser.add_argument('year', type=int, help='New year to move the course to')


    @transaction.atomic()
    def handle(self, *args, **options):
        translation.activate('pl')

        course_id = options['course_id']
        new_year = options['year']

        course = Course.objects.get(pk=course_id)

        if not course.start_date:
            raise CommandError('Course does not have start_date filled in')

        if course.start_date.year != new_year:
            new_date = datetime(year=new_year, month=course.start_date.month,
                                day=course.start_date.day)
            course.start_date = new_date.date()
            course.save()
            self.force_save_course(course)

    def force_save_course(self, course):
        """
        Goes though all course descendants (subjects, modules) and saves them to update didactic
        offer.
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
