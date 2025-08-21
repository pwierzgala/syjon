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
from apps.merovingian.models import Course
from apps.trinity.models import (AreaLearningOutcome, CourseLearningOutcome,
                                 EducationCategory)

green = termcolors.make_style(fg='green')
yellow = termcolors.make_style(fg='yellow')
cyan = termcolors.make_style(fg='cyan')
red = termcolors.make_style(fg='red', opts=('bold',))
bold = termcolors.make_style(opts=('bold',))

class Command(BaseCommand):
    args = u'<path>'
    help = u'path - Path to a XML file with Course Learning Outcomes'

    @transaction.atomic()
    def handle(self, *args, **options):
        """
        Loads module learning outcomes from XML file. Sample XML:
        <course id="course_id">
            <learning_outcomes category="category_id">
                <learning_outcome>
                    <symbol>Symbol</symbol>
                    <description>Description</description>
                    <area_learning_outcomes>
                        <area_learning_outcome id="area_learning_outcome_id"></area_learning_outcome>
                    </area_learning_outcomes>
                </learning_outcome>
            </learning_outcomes>
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
        
        for xml_learning_outcomes in xml_course.getElementsByTagName('learning_outcomes'):
            # Getting education category object
            education_category_id = xml_learning_outcomes.getAttribute('category')
            education_category = EducationCategory.objects.get(id = education_category_id)
            self.stdout.write(green("Education category: %s\n" % str(education_category).encode('utf-8')))
            
            # Removing existing course learning outcomes
            clos = CourseLearningOutcome.objects.filter(course = course, education_category = education_category)
            clos.delete()
            
            # Adding new course learning outcomes
            for xml_learning_outcome in xml_learning_outcomes.getElementsByTagName('learning_outcome'):
                 symbol = xml_learning_outcome.getElementsByTagName('symbol')[0].firstChild.nodeValue
                 descritpion = xml_learning_outcome.getElementsByTagName('description')[0].firstChild.nodeValue
                 
                 # Saving course learning outcome
                 clo = CourseLearningOutcome()
                 clo.course = course
                 clo.education_category = education_category
                 clo.symbol = symbol
                 clo.description = descritpion
                 clo.save()
                 self.stdout.write(cyan("\tCLO symbol: %s\n" % str(clo.symbol).encode('utf-8')))
                 
                 # Adding references to area learning outcomes
                 xml_area_learning_outcomes = xml_learning_outcome.getElementsByTagName('area_learning_outcomes')[0]
                 for xml_area_learning_outcome in xml_area_learning_outcomes.getElementsByTagName('area_learning_outcome'):
                     area_learning_outcome_id = xml_area_learning_outcome.getAttribute('id')
                     try:
                         alo = AreaLearningOutcome.objects.get(id = area_learning_outcome_id)
                         clo.alos.add(alo)
                         self.stdout.write(yellow("\t\tALO symbol: %s\n" % str(alo.symbol).encode('utf-8')))
                     except AreaLearningOutcome.DoesNotExist:
                         self.stdout.write(red("\t\tALO ID: %s\n" % str(area_learning_outcome_id).encode('utf-8')))
                 
                 
                 
                 
                 