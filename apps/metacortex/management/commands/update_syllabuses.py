# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from apps.merovingian.models import Module, Subject, SubjectToTeacher
from apps.metacortex.models import (SyllabusModule, SyllabusPractice,
                                    SyllabusSubject)
from apps.trainman.models import Department, Teacher


class Command(BaseCommand):

    def handle(self, *args, **options):
        # self.update_workload()
        self.update_syllabuses()

    def update_workload(self):
        # Pobierz wszystkie wydziału
        departments = Department.objects.filter(type=1).exclude(id=25)

        # Aktualizacja obsady zajęć na podstawie sylabusów.
        for department in departments:
            for child in department.children():
                for user_profile in child.userprofile_set.all():
                    try:
                        teacher = user_profile.teacher
                    except Teacher.DoesNotExist:
                        continue

                    module_syllabuses = SyllabusModule.objects.filter(coordinator=teacher, is_active=True)
                    for module_syllabus in module_syllabuses:
                        module = module_syllabus.module
                        module.coordinator = teacher
                        module.save()

                    subject_syllabuses = SyllabusSubject.objects.filter(teacher=teacher, is_active=True)
                    for subject_syllabus in subject_syllabuses:
                        subject = subject_syllabus.subject
                        try:
                            SubjectToTeacher.objects.get(subject=subject, teacher=teacher)
                        except SubjectToTeacher.DoesNotExist:
                            SubjectToTeacher.objects.create(subject=subject, teacher=teacher, hours=0, groups=0)
                            print("Created: ", subject.name, teacher)
                        except SubjectToTeacher.MultipleObjectsReturned:
                            pass

                    practice_syllabuses = SyllabusPractice.objects.filter(teacher=teacher, is_active=True)
                    for practice_syllabus in practice_syllabuses:
                        subject = practice_syllabus.subject
                        try:
                            SubjectToTeacher.objects.get(subject=subject, teacher=teacher)
                        except SubjectToTeacher.DoesNotExist:
                            SubjectToTeacher.objects.create(subject=subject, teacher=teacher, hours=0, groups=0)
                            print("Created: ", subject.name, teacher)
                        except SubjectToTeacher.MultipleObjectsReturned:
                            pass

    def update_syllabuses(self):
        # Aktualizacja sylabusów na podstawie obsady zajęć (Wydział Artystyczny).
        department = Department.objects.get(id=25)
        for child in department.children():
            for course in child.course_set.all():
                for sgroup in course.sgroups.all():
                    for module in sgroup.modules.all():

                        if module.coordinator:
                            _, created = SyllabusModule.objects.update_or_create(
                                module=module, coordinator=module.coordinator, defaults={'is_active': True}
                            )
                            if created:
                                print("-- Created: ", module.name, module.coordinator)
                            SyllabusModule.objects.filter(coordinator=module.coordinator).exclude(module__coordinator=module.coordinator).update(is_active=False)

                        for subject in module.subjects.all():
                            for teacher in subject.teachers.all():
                                if subject.type.is_practice():
                                    _, created = SyllabusPractice.objects.update_or_create(
                                        subject=subject, teacher=teacher, defaults={'is_active': True}
                                    )
                                else:
                                    _, created = SyllabusSubject.objects.update_or_create(
                                        subject=subject, teacher=teacher, defaults={'is_active': True}
                                    )
                                if created:
                                    print("-- Created: ", subject.name, teacher)

                                SyllabusSubject.objects.filter(teacher=teacher).exclude(subject__teachers=teacher).update(is_active=False)
                                SyllabusPractice.objects.filter(teacher=teacher).exclude(subject__teachers=teacher).update(is_active=False)
