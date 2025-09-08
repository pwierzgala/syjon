# -*- coding: utf-8 -*-
'''
Created on 27-08-2012

@author: pwierzgala
'''

from django.core.management.base import BaseCommand, CommandError

from apps.merovingian.models import Course
from apps.metacortex.models import (
    SyllabusModule, SyllabusPractice, SyllabusSubject)


class Command(BaseCommand):
    args = u'<id_course>'
    help = u'Wyświetla informacje o sylabusach wprowadzonych dla danego kierunku.'

    def handle(self, *args, **options):
        id_course = args[0]
        
        # Pobranie kierunków
        try:
            course = Course.objects.get(id = id_course)
            self.stdout.write('Kierunek: %s\n' % str(course).encode('utf-8'))
        except Course.DoesNotExist:
            raise CommandError('Nie znaleziono kierunk\n')
        
        self.stdout.write('\n')
        
        # Sylabusy modułu
        module_syllabusses = SyllabusModule.objects.filter(module__sgroup__course = course)
        if module_syllabusses:
            for module_syllabus in module_syllabusses.all():
                self.stdout.write('Sylabus modułu: %s, koordynator: %s\n', (str(module_syllabus.module).encode('utf-8'), str(module_syllabus.coordinator.user_profile.user.get_full_name()).encode('utf-8')))
        else:
            self.stdout.write('Nie znaleziono żadnego sylabusa modułu\n')
        self.stdout.write('\n')
        
        # Sylabusy przedmiotu
        subject_syllabusses = SyllabusSubject.objects.filter(subject__module__sgroup__course = course)
        if subject_syllabusses:
            for subject_syllabus in subject_syllabusses.all():
                self.stdout.write('\t Sylabus przedmiotu: %s, prowadzący: %s\n' % (str(subject_syllabus.subject).encode('utf-8'), str(subject_syllabus.teacher.user_profile.user.get_full_name()).encode('utf-8')))
        else:
            self.stdout.write('Nie znaleziono żadnego sylabusa przedmiotu\n')
        self.stdout.write('\n')
        
        # Sylabusy prakatyk
        practice_syllabusses = SyllabusPractice.objects.filter(subject__module__sgroup__course = course)
        if practice_syllabusses:
            for practice_syllabus in practice_syllabusses.all():
                self.stdout.write('\t Sylabus przedmiotu: %s, prowadzący: %s\n' % (str(practice_syllabus.subject).encode('utf-8'), str(practice_syllabus.teacher.user_profile.user.get_full_name()).encode('utf-8')))
        else:
            self.stdout.write('Nie znaleziono żadnego sylabusa praktyk\n')
        self.stdout.write('\n')