# -*- coding: utf-8 -*-
'''
Created on 27-08-2012

@author: pwierzgala
'''

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import termcolors, translation

import syjon
from apps.merovingian.models import Course, Module, SGroup
from apps.trinity.models import CourseLearningOutcome, ModuleLearningOutcome

green = termcolors.make_style(fg='green')
yellow = termcolors.make_style(fg='yellow')
cyan = termcolors.make_style(fg='cyan')
red = termcolors.make_style(fg='red', opts=('bold',))
bold = termcolors.make_style(opts=('bold',))


class Command(BaseCommand):
    args = u'<module_from module_to>'
    help = u'Copies module learning outcomes from specified module'

    @transaction.atomic()
    def handle(self, *args, **options):
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))
        
        id_module_from = args[0]
        id_module_to = args[1]

        module_to = Module.objects.get(id=id_module_to)
        module_from = Module.objects.get(id=id_module_from)

        course_to = module_to.get_course()
        course_from = module_from.get_course()

        # Removing module learning outcomes from module_year_to
        mlos_to = ModuleLearningOutcome.objects.filter(module=module_to)
        mlos_to.delete()
        print(green("Module learning outcomes for module: %s (id: %s) has been removed" % (str(module_to).encode('utf-8'), module_to.id)))

        # Copying module learning outcomes from module_from to module_to
        mlos_from = ModuleLearningOutcome.objects.filter(module=module_from)
        for mlo_from in mlos_from:

            # Saving references to course learning outcomes, before shallow copy!
            clos_from = mlo_from.clos

            # Shallow copy of module learning outcome
            mlo_from.pk = None
            mlo_from.module = module_to
            mlo_from.save()
            print(yellow('\tSkopiowano Modułowy Efekt Kształcenia: %s (id: %s)' % (str(mlo_from.symbol).encode('utf-8'), mlo_from.id)))

            # Copying references to courese learning outcomes
            for clo_from in clos_from.all():
                # Getting course learning outcome defined for course_year_to with the same symbol as in module_year_from
                try:
                    clo_to = CourseLearningOutcome.objects.get(course=course_to, symbol=clo_from.symbol)
                except CourseLearningOutcome.DoesNotExist:
                    print(red("\t\tCourse learning outcome does not exist: %s (id: %s)" % (str(clo_from.symbol).encode('utf-8'), clo_from.id)))
                    continue
                except CourseLearningOutcome.MultipleObjectsReturned:
                    print(red("\t\tMultiple course learning outcome returned: %s (id: %s)" % (str(clo_from.symbol).encode('utf-8'), clo_from.id)))
                    continue

                mlo_from.clos.add(clo_to)
                print(yellow("\t\tReference to course learning outcome has been added: %s (id: %s)" % (str(clo_to.symbol).encode('utf-8'), clo_to.id)))
