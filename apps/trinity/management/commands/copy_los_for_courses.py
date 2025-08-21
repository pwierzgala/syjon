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
from django.utils import translation

import syjon
from apps.merovingian.models import Course, Module
from apps.trinity.management.commands.copy_los_for_course import \
    Command as CopyCommand
from apps.trinity.models import TrinityProfile

style = "<style>"+\
        ".indent_1 {margin-left: 15px; display: block;}"+\
        ".indent_2 {margin-left: 30px; display: block;}"+\
        ".indent_3 {margin-left: 45px; display: block;}"+\
        ".indent_4 {margin-left: 60px; display: block;}"+\
        ".indent_5 {margin-left: 75px; display: block;}"+\
        ".indent_6 {margin-left: 90px; display: block;}"+\
        "p {margin: 0 0 5px 0;}"+\
        "</style>"
        
head = "<!DOCTYPE html>" +\
        "<html lang='pl'>" +\
        "<head>" +\
        "<meta http-equiv='Content-Type' content='text/html; charset=UTF-8' />"+\
        style +\
        "</head>"+\
        "<body>"
        
foot = "</body></html>"

h1 = lambda x: "<h1>"+x+"</h1>"
h2 = lambda x: "<h2>"+x+"</h2>"
h3 = lambda x: "<h3>"+x+"</h3>"

red = lambda x: "<p style='color: red'>"+x+"</p>"
green = lambda x: "<p style='color: green'>"+x+"</p>"
cyan = lambda x: "<p style='color: #206cff'>"+x+"</p>"
yellow = lambda x: "<p style='color: #ec7000'>"+x+"</p>"
bold = lambda x: "<b>"+x+"</b>"

i1 = lambda x: "<span class='indent_1'>"+x+"</span>"
i2 = lambda x: "<span class='indent_2'>"+x+"</span>"
i3 = lambda x: "<span class='indent_3'>"+x+"</span>"
i4 = lambda x: "<span class='indent_4'>"+x+"</span>"
i5 = lambda x: "<span class='indent_5'>"+x+"</span>"
i6 = lambda x: "<span class='indent_6'>"+x+"</span>"

class Command(BaseCommand):
    args = u'<year_from year_to>'
    help = u'Copies learning outcomes from all courses and all modules from year_from to all courses and all modules from year_to'

    def copy_trinity_profiles(self, year_from, year_to):
        """
        Copies administrators' permissions to courses from year_from to courses from year_to
        """
        print(h1(bold("Copying administrators' profiles")))
        trinity_profiles = TrinityProfile.objects.all()       
        for trinity_profile in trinity_profiles:
            print(i1(h2("Processing profile: %s (id: %s)" % (str(trinity_profile).encode('utf-8'), trinity_profile.id))))
            for course in trinity_profile.courses.all():
                if course.start_date != None:
                    if course.start_date.year == int(year_from):
                        try:
                            course_year_to = Course.objects.get(start_date__year = year_to, name = course.name, level = course.level, profile = course.profile, type = course.type, department = course.department)
                            trinity_profile.courses.remove(course)
                            print(i2(red("Course %s (id: %s) has been removed" % (str(course).encode('utf-8'), course.id))))
                            trinity_profile.courses.add(course_year_to)
                            print(i2(green("Course %s (id: %s) has been added" % (str(course_year_to).encode('utf-8'), course_year_to.id))))
                        except:
                            print(i2(red("Course does not exits: %s (id: %s)" % (str(course).encode('utf-8'), course.id))))
                            continue
                    
                    elif course.start_date.year == int(year_to):
                         # If the command is executed several times this will prevent from removing existing courses_year_to
                         pass
                    else:
                        # Sometimes it happens that user has added course started more than one year age.
                        # Such course should be removed because users can only edit learning outcomes in courses started no more than one year ago.  
                        trinity_profile.courses.remove(course)
                        print(i2(red("Course %s (id: %s) has been removed because of too old start_date" % (str(course).encode('utf-8'), course.id))))
                else:
                    # Processed course does not have defined start_date.
                    trinity_profile.courses.remove(course)
                    print(i2(red("Course does not have defined start_date: %s (id: %s)" % (str(course).encode('utf-8'), course.id))))

    @transaction.atomic()
    def handle(self, *args, **options):
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))
        
        print(head)
        
        try:    
            year_from = args[0]
            year_to = args[1]
            print(green("Year from: %s" % str(year_from).encode('utf-8')))
            print(green("Year to: %s" % str(year_to).encode('utf-8')))
        except:
            print(red("Nie podano argumentów"))
            return
        
        courses_year_to = Course.objects.filter(start_date__year = year_to)
        cp = CopyCommand()
        
        i = 0.0;
        n = courses_year_to.count()
        for course_year_to in courses_year_to:
            cp.copy_los_for_course(course_year_to, year_from)
            i += 1
            p = i/n*100
            print(cyan("%.2f%%\n" % p))
            
        # Copying learning outcomes admins from course_year_from to course_year_to
        self.copy_trinity_profiles(year_from, year_to)
        
        print(foot)