# -*- coding: utf-8 -*-
'''
Created on 26-08-2016

@author: pwierzgala
'''

import sys

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import translation

import syjon
from apps.merovingian.models import Course
from apps.metacortex.models import (
    ECTS, SyllabusModule, SyllabusPractice, SyllabusSubject, SyllabusToECTS)
from apps.syjon.lib.pdf import create_pdf


class Command(BaseCommand):
    args = u'<id_course silent>'
    help = u'Przegląda moduły i przedmioty kierunku w celu zaktualizowania sekcji ECTS sylabusów.'

    silent = 0

    @transaction.atomic()
    def handle(self, *args, **options):
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))

        course_id = args[0]
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise CommandError('Nie znaleziono kierunku.\n')

        template_path = 'metacortex/syllabus_my/syllabus_module_print.html'
        for sgroup in course.sgroups.all():
            for module in sgroup.modules.all():
                print(module)

                syllabus = module.syllabus
                file_name = '{code} - {name}.pdf'.format(
                    code=syllabus.module.internal_code,
                    name=syllabus.module.name
                )
                output_path = '{file_path}/{file_name}'.format(
                    file_path='.',
                    file_name=file_name
                )
                template_context = {'syllabus': syllabus}
                create_pdf(template_path=template_path, template_context=template_context, output_path=output_path)
