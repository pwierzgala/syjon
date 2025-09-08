# -*- coding: utf-8 -*-
'''
Created on 27-08-2012

@author: pwierzgala
'''

from django.core.management.base import BaseCommand, CommandError
from django.utils import termcolors

from apps.metacortex.html_parsers import HTMLParserWYSIWYG
from apps.metacortex.models import (
    SyllabusModule, SyllabusPractice, SyllabusSubject)

green = termcolors.make_style(fg='green')
yellow = termcolors.make_style(fg='yellow')
cyan = termcolors.make_style(fg='cyan')
red = termcolors.make_style(fg='red', opts=('bold',))
bold = termcolors.make_style(opts=('bold',))

class Command(BaseCommand):
    help = u'Usuwa formatowanie z pól tekstowych sylabusów.'

    def handle(self, *args, **options):
        self.clear_module_syllabusses()
        self.clear_subject_syllabusses()
        self.clear_practice_syllabusses()
        
    def clear_module_syllabusses(self):
        self.stdout.write(bold("Oczyszczanie sylabusów modułów\n"))
        
        syllabusses = SyllabusModule.objects.all()
        i = 0
        n = syllabusses.count()
        for syllabus in syllabusses:
            syllabus.module_description = self.clear_text(syllabus.module_description)
            syllabus.module_description_pl = self.clear_text(syllabus.module_description_pl)
            syllabus.additional_information = self.clear_text(syllabus.additional_information)
            syllabus.additional_information_pl = self.clear_text(syllabus.additional_information_pl)
            syllabus.save()
            i += 1
            self.stdout.write("%s%% (%s)\n" % (round(float(i)/float(n)*100, 2), syllabus.module.pk))
    
    def clear_subject_syllabusses(self):
        self.stdout.write(bold("\n\nOczyszczanie sylabusów przedmiotów\n"))
        
        syllabusses = SyllabusSubject.objects.all()
        i = 0
        n = syllabusses.count()
        for syllabus in syllabusses:
            syllabus.initial_requirements = self.clear_text(syllabus.initial_requirements)
            syllabus.initial_requirements_pl = self.clear_text(syllabus.initial_requirements_pl)
            syllabus.literature = self.clear_text(syllabus.literature)
            syllabus.literature_pl = self.clear_text(syllabus.literature_pl)
            syllabus.subjects_scope = self.clear_text(syllabus.subjects_scope)
            syllabus.subjects_scope_pl = self.clear_text(syllabus.subjects_scope_pl)
            syllabus.education_effects = self.clear_text(syllabus.education_effects)
            syllabus.education_effects_pl = self.clear_text(syllabus.education_effects_pl)
            syllabus.additional_information = self.clear_text(syllabus.additional_information)
            syllabus.additional_information_pl = self.clear_text(syllabus.additional_information_pl)
            syllabus.save()
            i += 1
            self.stdout.write("%s%% (%s)\n" % (round(float(i)/float(n)*100, 2), syllabus.subject.pk))

    def clear_practice_syllabusses(self):
        self.stdout.write(bold("\n\nOczyszczanie sylabusów praktyk\n"))
        
        syllabusses = SyllabusPractice.objects.all()
        i = 0
        n = syllabusses.count()
        for syllabus in syllabusses:
            syllabus.description = self.clear_text(syllabus.description)
            syllabus.description_pl = self.clear_text(syllabus.description_pl)
            syllabus.education_effects = self.clear_text(syllabus.education_effects)
            syllabus.education_effects_pl = self.clear_text(syllabus.education_effects_pl)
            syllabus.additional_information = self.clear_text(syllabus.additional_information)
            syllabus.additional_information_pl = self.clear_text(syllabus.additional_information_pl)
            syllabus.save()
            i += 1
            self.stdout.write("%s%% (%s)\n" % (round(float(i)/float(n)*100, 2), syllabus.subject.pk))
        
    def clear_text(self, text):
        parser = HTMLParserWYSIWYG()
        return parser.parse(text)
       
    

        