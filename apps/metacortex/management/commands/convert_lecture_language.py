# -*- coding: utf-8 -*-
'''
Created on 27-08-2012

@author: pwierzgala
'''

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import termcolors

from apps.metacortex.models import LectureLanguage, SyllabusModule

green = termcolors.make_style(fg='green')
yellow = termcolors.make_style(fg='yellow')
cyan = termcolors.make_style(fg='cyan')
red = termcolors.make_style(fg='red', opts=('bold',))
bold = termcolors.make_style(opts=('bold',))

class Command(BaseCommand):
    help = u'Konwertuje pole język wykładowy z typu foreing key do many to many.'

    @transaction.atomic()
    def handle(self, *args, **options):
        syllabusses = SyllabusModule.objects.all()
        for s in syllabusses:
            if s.lecture_language:
                ll = LectureLanguage.objects.get(id = s.lecture_language.id)
                s.lecture_languages.add(ll)
                self.stdout.write('Dodano język: %s do sylabusa: %s\n' % (str(ll.name).encode('utf-8'), str(s.id).encode('utf-8')))
                