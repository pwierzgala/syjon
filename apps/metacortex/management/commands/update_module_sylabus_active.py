# -*- coding: utf-8 -*-


from django.core.management.base import BaseCommand

from apps.metacortex.models import SyllabusModule


class Command(BaseCommand):
    args = u'<id_course>'

    def handle(self, *args, **options):
        id_course = args[0]
        syllabuses = SyllabusModule.objects.filter(module__sgroup__course=id_course)
        for syllabus in syllabuses:
            print(syllabus)
            syllabus.is_active = True
            syllabus.save()
