# -*- coding: utf-8 -*-
'''
Created on 27-08-2012

@author: pwierzgala
'''

import sys
from xml.dom import minidom

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import termcolors, translation

import syjon
from apps.merovingian.models import Course, Module
from apps.trinity.models import CourseLearningOutcome, ModuleLearningOutcome

green = termcolors.make_style(fg='green')
yellow = termcolors.make_style(fg='yellow')
cyan = termcolors.make_style(fg='cyan')
red = termcolors.make_style(fg='red', opts=('bold',))
bold = termcolors.make_style(opts=('bold',))

class Command(BaseCommand):
    args = u'<path>'
    help = u'path - Path to a XML file with Module Learning Outcomes'

    @transaction.atomic()
    def handle(self, *args, **options):
        """
        Loads module learning outcomes from XML file. Sample XML:
        <course id="course_id">
            <module id="module_id">
                <learning_outcomes>
                   <learning_outcome>
                       <symbol>symbol</symbol>
                       <description>description</description>
                       <course_learning_outcomes>
                           <course_learning_outcome>symbol</course_learning_outcome>
                       </course_learning_outcomes>
                   </learning_outcome>
                </learning_outcomes>
            </module>
        </course>
        """
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))
            
        try:    
            path = args[0]
        except:
            print(red("Insufficient number of arguments"))
            return
        
        dom = minidom.parse(path)
        xml_course = dom.getElementsByTagName('course')[0]
        
        # Getting course object
        course_id = xml_course.getAttribute('id')
        course = Course.objects.get(id = course_id)
        self.stdout.write(green("Course: %s\n" % str(course).encode('utf-8')))
        
        for xml_module in xml_course.getElementsByTagName('module'):
            # Pobranie obiektu modułu
            module_id = xml_module.getAttribute('id')
            module = Module.objects.get(id = module_id)
            self.stdout.write(green("Module: %s\n" % str(module).encode('utf-8')))
            
            # Removing existing module learning outcomes
            mlos = ModuleLearningOutcome.objects.filter(module = module)
            mlos.delete()
            
            # Adding new module learning outcomes
            xml_learning_outcomes = xml_module.getElementsByTagName('learning_outcomes')[0]
            for xml_learning_outcome in xml_learning_outcomes.getElementsByTagName('learning_outcome'):
                 symbol = xml_learning_outcome.getElementsByTagName('symbol')[0].firstChild.nodeValue
                 descritpion = xml_learning_outcome.getElementsByTagName('description')[0].firstChild.nodeValue
                 
                 # Saving module learning outcome
                 mlo = ModuleLearningOutcome()
                 mlo.module = module
                 mlo.symbol = symbol
                 mlo.description = descritpion
                 mlo.save()
                 self.stdout.write(cyan("\tMLO symbol: %s\n" % str(symbol).encode('utf-8')))
                 
                 # Adding references to course learning outcomes
                 xml_course_learning_outcomes = xml_learning_outcome.getElementsByTagName('course_learning_outcomes')[0]
                 for xml_course_learning_outcome in xml_course_learning_outcomes.getElementsByTagName('course_learning_outcome'):
                     course_learning_outcome_symbol = xml_course_learning_outcome.firstChild.nodeValue
                     clo = CourseLearningOutcome.objects.get(course = course, symbol = course_learning_outcome_symbol)
                     mlo.clos.add(clo)
                     self.stdout.write(yellow("\t\tCLO Symbol: %s\n" % str(clo.symbol).encode('utf-8')))
                 
                 
                 
                 
                 