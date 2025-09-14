"""
Created on 24-11-2020

@author: pwierzgala
"""

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import termcolors, translation

import syjon
from apps.merovingian.models import Course, Module, SGroup, Subject
from apps.trinity.models import (
    CourseLearningOutcome, ModuleLearningOutcome,
    SubjectToModuleLearningOutcome)

green = termcolors.make_style(fg='green')
yellow = termcolors.make_style(fg='yellow')
cyan = termcolors.make_style(fg='cyan')
red = termcolors.make_style(fg='red', opts=('bold',))
bold = termcolors.make_style(opts=('bold',))


class Command(BaseCommand):
    help = u'Copies course learning outcomes from one course to other'

    def add_arguments(self, parser):
        parser.add_argument('course_from', type=int, help='ID of the source course')
        parser.add_argument('course_to', type=int, help='ID of the target course')


    @transaction.atomic()
    def handle(self, *args, **options):
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))

        id_course_from = options['course_from']
        id_course_to = options['course_to']

        course_from = self.get_course(id_course_from)
        course_to = self.get_course(id_course_to)

        self.copy_cols(course_from=course_from, course_to=course_to)
        self.copy_mlos(course_from=course_from, course_to=course_to)

        print('')

    @staticmethod
    def get_course(course_id):
        try:
            course = Course.objects.get(id=course_id)
            print('ID course from: {} ({})'.format(course, course.id))
        except Course.DoesNotExist:
            raise CommandError("Course does not exist: {}".format(course_id))
        else:
            return course

    @staticmethod
    def copy_cols(course_from, course_to):
        # Removing course learning outcomes from course_to
        clos_to = CourseLearningOutcome.objects.filter(course=course_to)
        clos_to.delete()
        print('Learning outcomes for course: {} (id: {}) have been removed'.format(
            course_to,
            course_to.id
        ))

        # Copying course learning outcomes from course_from to course_to
        clos_from = CourseLearningOutcome.objects.filter(course=course_from)
        for clo in clos_from:
            locs_from = clo.locs

            clo.pk = None
            clo.course = course_to
            clo.save()
            print("Course learning outcome: {} (id: {}) has been copied".format(
                clo.symbol,
                clo.id
            ))

            # Copying area learning outcomes
            for loc in locs_from.all():
                clo.locs.add(loc)
                print("Learning Outcome Characteristic has been copied '{}' (id: {})".
                    format(loc.symbol, loc.id))
            print('')

    @staticmethod
    def copy_mlos(course_from, course_to):
        sgroups_to = SGroup.objects.filter(course=course_to)
        sgroups_from = SGroup.objects.filter(course=course_from)
        for sgroup_to in sgroups_to:
            try:
                sgroup_from = sgroups_from.get(name=sgroup_to.name)
            except SGroup.DoesNotExist:
                print("SGroup does not exist: {} (id: {})".format(sgroup_to.name, sgroup_to.id))
                continue
            except SGroup.MultipleObjectsReturned:
                print("Multiple sgroups returned: {} (id: {})".format(sgroup_to.name, sgroup_to.id))
                continue
            print("Copying sgroup: {} (id: {} --> {})".format(sgroup_from.name, sgroup_from.id, sgroup_to.id))

            modules_to = sgroup_to.modules.all()
            modules_from = sgroup_from.modules.all()
            for module_to in modules_to:
                try:
                    module_from = modules_from.get(name=module_to.name)
                except Module.DoesNotExist:
                    print("Module does not exist: {} (id: {})".format(module_to.name, module_to.id))
                    continue
                except Module.MultipleObjectsReturned:
                    print("Multiple modules returned: {} (id: {})".format(module_to.name, module_to.id))
                    continue
                print("Copying module: {} (id: {} --> {})".format(module_from.name, module_from.id, module_to.id))

                # Removing module learning outcomes from module_year_to
                mlos_year_to = ModuleLearningOutcome.objects.filter(module=module_to)
                mlos_year_to.delete()
                print("Module learning outcomes for module: {} (id: {}) has been removed".format(module_to, module_to.id))

                # Copying module learning outcomes from module_from to module_to
                mlos_from = ModuleLearningOutcome.objects.filter(module=module_from)
                for mlo in mlos_from:
                    clos_from = mlo.clos
                    slos_from = mlo.module_to_slos.all()

                    mlo.pk = None
                    mlo.module = module_to
                    mlo.save()
                    print('Skopiowano Modułowy Efekt Kształcenia: {} (id: {})'.format(mlo.symbol, mlo.id))

                    for clo_from in clos_from.all():
                        try:
                            clo_to = CourseLearningOutcome.objects.get(course=course_to, symbol=clo_from.symbol)
                        except CourseLearningOutcome.DoesNotExist:
                            print("Course learning outcome does not exist: {} (id: {})".format(clo_from.symbol, clo_from.id))
                            continue
                        except CourseLearningOutcome.MultipleObjectsReturned:
                            print("Multiple course learning outcome returned: {} (id: {})".format(clo_from.symbol, clo_from.id))
                            continue

                        mlo.clos.add(clo_to)
                        print("Reference to course learning outcome has been added: {} (id: {})".format(clo_to.symbol, clo_to.id))

                    for slo_from in slos_from:
                        subject_from = slo_from.subject

                        try:
                            subject_to = Subject.objects.get(
                                module=module_to,
                                name=subject_from.name,
                                internal_code=subject_from.internal_code,
                                semester=subject_from.semester,
                                type=subject_from.type
                            )
                        except Subject.DoesNotExist:
                            print(
                             "\tSubject does not exist: {} (id: {})".format(subject_from.name, subject_from.id))
                            continue
                        except Subject.MultipleObjectsReturned:
                            print("\tMultiple subjects returned: {} (id: {})".format(subject_from.name, subject_from.id))
                            continue

                        print("\tCopying subject: {} (id: {} --> {})".format(subject_from.name, subject_from.id, subject_to.id))

                        SubjectToModuleLearningOutcome.objects.filter(
                            subject=subject_to,
                            mlo=mlo
                        ).delete()
                        SubjectToModuleLearningOutcome.objects.create(
                            subject=subject_to,
                            mlo=mlo
                        )
