"""
Created on 27-08-2012

@author: pwierzgala
"""

import sys
from xml.dom import minidom

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import translation

import syjon
from apps.merovingian.models import Course, Module, SGroup
from apps.trinity.models import (
    CourseLearningOutcome, EducationArea, EducationDiscipline, EducationField,
    KnowledgeArea, ModuleLearningOutcome, TrinityProfile)

style = "<style>"+\
        ".indent_1 {margin-left: 15px; display: block;}"+\
        ".indent_2 {margin-left: 30px; display: block;}"+\
        ".indent_3 {margin-left: 45px; display: block;}"+\
        ".indent_4 {margin-left: 60px; display: block;}"+\
        ".indent_5 {margin-left: 75px; display: block;}"+\
        ".indent_6 {margin-left: 90px; display: block;}"+\
        "p {margin: 0 0 5px 0;}"+\
        "</style>"

h1 = lambda x: "<h1>"+x+"</h1>"
h2 = lambda x: "<h2>"+x+"</h2>"
h3 = lambda x: "<h3>"+x+"</h3>"

red = lambda x: "<p style='color: red'>"+x+"</p>"
green = lambda x: "<p style='color: green'>"+x+"</p>"
cyan = lambda x: "<p style='color: #206cff'>"+x+"</p>"
yellow = lambda x: "<p style='color: #ec7000'>"+x+"</p>"
bold = lambda x: "<p><b>"+x+"</b></p>"

i1 = lambda x: "<span class='indent_1'>"+x+"</span>"
i2 = lambda x: "<span class='indent_2'>"+x+"</span>"
i3 = lambda x: "<span class='indent_3'>"+x+"</span>"
i4 = lambda x: "<span class='indent_4'>"+x+"</span>"
i5 = lambda x: "<span class='indent_5'>"+x+"</span>"
i6 = lambda x: "<span class='indent_6'>"+x+"</span>"

class Command(BaseCommand):
    args = u'<course_id year_from>'
    help = u'Copies learning outcomes from all courses and all modules from year_from to all courses and all modules from year_to'

    def add_arguments(self, parser):
        parser.add_argument(
            'course_id',
            type=int,
            help='ID of the target course')
        parser.add_argument(
            'year_from',
            type=int,
            help='Year from which learning outcomes will be copied')

    def copy_education_areas(self, course_year_from, course_year_to):
        """
        Copyies educations adreas from course_year_to to course_year_from.
        """
        
        if course_year_to.is_level_phd(): # Course is at PhD level
            # Getting references to education areas from course_year_from
            knowledge_areas = KnowledgeArea.objects.filter(course = course_year_from)
            education_fields = EducationField.objects.filter(course = course_year_from)
            education_disciplines = EducationDiscipline.objects.filter(course = course_year_from)
            
            # Removing references to education areas from course_year_to
            course_year_to.knowledge_areas.clear()
            course_year_to.education_fields.clear()
            course_year_to.education_disciplines.clear()
            
            # Adding references to education areas to course_year_to
            for knowledge_area in knowledge_areas:
                course_year_to.knowledge_areas.add(knowledge_area)
                print(i2(cyan("Copied knowledge area: %s (id: %s)" % (str(knowledge_area).encode('utf-8'), knowledge_area.id))))
            
            for education_field in education_fields:
                course_year_to.educationfields.add(education_field)
                print(i2(cyan("Copied education field: %s (id: %s)" % (str(education_field).encode('utf-8'), education_field.id))))
            
            for education_discipline in education_disciplines:
                course_year_to.education_disciplines.add(education_discipline)
                print(i2(cyan("Copied education discipline: %s (id: %s)" % (str(education_discipline).encode('utf-8'), education_discipline.id))))
                 
        else: # Course is not at PhD level
            education_areas = EducationArea.objects.filter(course = course_year_from)
            course_year_to.education_areas.clear()
            for education_area in education_areas:
                course_year_to.education_areas.add(education_area)
                print(i2(cyan("Copied education area: %s (id: %s)" % (str(education_area).encode('utf-8'), education_area.id))))
                
    def copy_course_learning_oucomes(self, course_year_from, course_year_to):
        """
        Copies course learning outcomes from course_year_from to course_year_to.
        
        Note: We do not copy area learning outcomes. If area learning outcomes change there will be need to create a mechanisms to keep the old ones
        for old course learning outcomes and add new ones for new course learning outcomes.
        """
        
        # Removing course learning outcomes from course_year_to
        clos_year_to = CourseLearningOutcome.objects.filter(course = course_year_to)
        clos_year_to.delete()
        print(i2(bold("Course learning outcomes for course: %s (id: %s) has been removed" % (str(course_year_to).encode('utf-8'), course_year_to.id))))
        
        # Copying course learning outcomes from course_year_from to course_year_to
        clos_year_from = CourseLearningOutcome.objects.filter(course = course_year_from)
        for clo in clos_year_from:
            
            # Saving references to area learning outcomes
            alos_list = [alo for alo in clo.alos.all()]
            
            # Copying course learning outcome
            clo.pk = None
            clo.course = course_year_to
            clo.save()
            print(i2(cyan("Course learning outcome has been added: %s (id: %s)" % (str(clo.symbol).encode('utf-8'), clo.id))))
            
            # Copying references to area learning outcomes
            for alo in alos_list:
                clo.alos.add(alo)
                print(i3(yellow("Reference to area learning outcome has been added: %s (id: %s)" % (str(alo.symbol).encode('utf-8'), alo.id))))
                
    def copy_module_learning_outcomes(self, course_year_from, course_year_to):
        """
        Copies module learning outcomes from course_year_from to course_year_to.
        
        Note: We do not directly iterate over modules because module_year_from and module_year_to are compared by name 
        and there may be to modules with the same name in different sgroups.
        """
        
        sgroups_year_to = SGroup.objects.filter(course = course_year_to)
        sgroups_year_from = SGroup.objects.filter(course = course_year_from)
        
        # Iterating over sgroups from course_year_to
        for sgroup_year_to in sgroups_year_to:
            # Getting corresponding sgroup from course_year_from
            try:
                sgroup_year_from = sgroups_year_from.get(name = sgroup_year_to.name)
            except SGroup.DoesNotExist:
                print(i2(red("SGroup does not exist: %s (id: %s)" % (str(sgroup_year_to.name).encode('utf-8'), sgroup_year_to.id))))
                continue
            except SGroup.MultipleObjectsReturned:
                print(i2(red("Multiple sgroups returned: %s (id: %s)" % (str(sgroup_year_to.name).encode('utf-8'), sgroup_year_to.id))))
                continue
            
            print(i2(bold("Copying sgroup: %s (id: %s --> %s)" % (str(sgroup_year_from.name).encode('utf-8'), sgroup_year_from.id, sgroup_year_to.id))))

            modules_year_to = sgroup_year_to.modules.all()
            modules_year_from = sgroup_year_from.modules.all()

            # Iterating over modules from sgroup_year_to
            for module_year_to in modules_year_to:
                # Gettin corresponding module from sgroup_year_from
                try:
                    module_year_from = modules_year_from.get(name = module_year_to.name)
                except Module.DoesNotExist:
                    print(i3(red("Module does not exist: %s (id: %s)" % (str(module_year_to.name).encode('utf-8'), module_year_to.id))))
                    continue
                except Module.MultipleObjectsReturned:
                    print(i3(red("Multiple modules returned: %s (id: %s)" % (str(module_year_to.name).encode('utf-8'), module_year_to.id))))
                    continue
                
                print(i3(bold("Copying module: %s (id: %s --> %s)" % (str(module_year_from.name).encode('utf-8'), module_year_from.id, module_year_to.id))))
        
                # Removing module learning outcomes from module_year_to
                mlos_year_to = ModuleLearningOutcome.objects.filter(module = module_year_to)
                mlos_year_to.delete()
                print(i4(green("Module learning outcomes for module: %s (id: %s) has been removed" % (str(module_year_to).encode('utf-8'), module_year_to.id))))
                
                # Copying module learning outcomes from module_year_from to module_year_to
                mlos_year_from = ModuleLearningOutcome.objects.filter(module = module_year_from)
                for mlo in mlos_year_from:
                    
                    # Saving references to course learning outcomes
                    clos_module_from = [clo for clo in mlo.clos.all()]
                    
                    # Copying module learning outcome
                    mlo.pk = None
                    mlo.module = module_year_to
                    mlo.save()
                    print(i5(cyan("Module learning outcome has been copied: %s (id: %s)" % (str(mlo.symbol).encode('utf-8'), mlo.id))))
                    
                    # Copying references to course learning outcomes
                    for clo_module_from in clos_module_from:
                        # Getting course learning outcome defined for course_year_to with the same symbol as in module_year_from
                        try:
                            clo_module_to = CourseLearningOutcome.objects.get(course=course_year_to, symbol=clo_module_from.symbol)
                        except CourseLearningOutcome.DoesNotExist:
                            print(i6(red("Course learning outcome does not exist: %s (id: %s)" % (str(clo_module_from.symbol).encode('utf-8'), clo_module_from.id))))
                            continue
                        except CourseLearningOutcome.MultipleObjectsReturned:
                            print(i6(red("Multiple course learning outcome returned: %s (id: %s)" % (str(clo_module_from.symbol).encode('utf-8'), clo_module_from.id))))
                            continue
                        
                        mlo.clos.add(clo_module_to)
                        print(i6(yellow("Reference to course learning outcome has been added: %s (id: %s)" % (str(clo_module_to.symbol).encode('utf-8'), clo_module_to.id))))

    @transaction.atomic()
    def copy_los_for_course(self, course_year_to, year_from):
        """
        Copies areas of education, course learning outcomes and module_learning_outcomes from course started in year_from to course_year_to.
        """
        
        # Getting course from which learning outcomes will be copied
        try:
            course_year_from = Course.objects.get(start_date__year = year_from, name = course_year_to.name, level = course_year_to.level, profile = course_year_to.profile, type = course_year_to.type, department = course_year_to.department)
            print(h1(green("Copying learning outcomes from course: %s" % str(course_year_from).encode('utf-8'))))
        except:
            print(h1(red("Course from which learning outcomes should be copied does not exist: %s" % str(course_year_to).encode('utf-8'))))
            return
        
        print(i1(h2("Copying education areas")))
        self.copy_education_areas(course_year_from, course_year_to)
        print(i1(h2("Copying course learning outcomes")))
        self.copy_course_learning_oucomes(course_year_from, course_year_to)
        print(i1(h2("Copying module learning outcomes")))
        self.copy_module_learning_outcomes(course_year_from, course_year_to)
    
    def handle(self, *args, **options):
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))

        course_id = options['course_id']
        year_from = options['year_from']

        # Getting course to which learning outcomes will be copied
        try:
            course_year_to = Course.objects.get(pk = course_id)
        except Course.DoesNotExist:
            print(red("Course to which learning outcomes should be copied does not exist: %s (ID)" % course_id))
            return 
        
        self.copy_los_for_course(course_year_to, year_from)
