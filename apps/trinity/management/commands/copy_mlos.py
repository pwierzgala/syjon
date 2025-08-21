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
    args = u'<course_from course_to>'
    help = u'Copies module learning outcomes from one course to other'

    @transaction.atomic()
    def handle(self, *args, **options):
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))
        
        id_course_from = args[0]
        id_course_to = args[1]
        
        # Getting courses
        try:
            course_from = Course.objects.get(id = id_course_from)
            print('ID course from: %s (%s)' % (str(course_from).encode('utf-8'), str(course_from.id).encode('utf-8')))
        except Course.DoesNotExist:
            raise CommandError('Course does not exist: %s' % str(course_from).encode('utf-8'))
        
        try:
            course_to = Course.objects.get(id = id_course_to)
            print('ID course to: %s (%s)' % (str(course_to).encode('utf-8'), str(course_to.id).encode('utf-8')))
        except:
            raise CommandError('Course does not exist: %s\n' % str(course_to).encode('utf-8'))
        
        print('')
                
        # Iterating over sgroups from course_to
        sgroups_to = SGroup.objects.filter(course = course_to)
        sgroups_from = SGroup.objects.filter(course = course_from)
        for sgroup_to in sgroups_to:
            
            try:
                sgroup_from = sgroups_from.get(name = sgroup_to.name)
            except SGroup.DoesNotExist:
                print(red("\tSGroup does not exist: %s (id: %s)" % (str(sgroup_to.name).encode('utf-8'), sgroup_to.id)))
                continue
            except SGroup.MultipleObjectsReturned:
                print(red("\tMultiple sgroups returned: %s (id: %s)" % (str(sgroup_to.name).encode('utf-8'), sgroup_to.id)))
                continue
            print(bold("\tCopying sgroup: %s (id: %s --> %s)" % (str(sgroup_from.name).encode('utf-8'), sgroup_from.id, sgroup_to.id)))
            
            # Iterating over modules from sgroup_year_to
            modules_to = sgroup_to.modules.all()
            modules_from = sgroup_from.modules.all()
            for module_to in modules_to:
                
                # Gettin corresponding module from sgroup_from
                try:
                    module_from = modules_from.get(name = module_to.name)
                except Module.DoesNotExist:
                    print(red("\t\tModule does not exist: %s (id: %s)" % (str(module_to.name).encode('utf-8'), module_to.id)))
                    continue
                except Module.MultipleObjectsReturned:
                    print(red("\t\tMultiple modules returned: %s (id: %s)" % (str(module_to.name).encode('utf-8'), module_to.id)))
                    continue
                print(bold("\t\tCopying module: %s (id: %s --> %s)" % (str(module_from.name).encode('utf-8'), module_from.id, module_to.id)))
                
                # Removing module learning outcomes from module_year_to
                mlos_year_to = ModuleLearningOutcome.objects.filter(module = module_to)
                mlos_year_to.delete()
                print(green("\t\t\tModule learning outcomes for module: %s (id: %s) has been removed" % (str(module_to).encode('utf-8'), module_to.id)))
     
                # Copying module learning outcomes from module_from to module_to
                mlos_from = ModuleLearningOutcome.objects.filter(module = module_from)
                for mlo_from in mlos_from:                   
                    
                    # Saving references to course learning outcomes
                    clos_from = mlo_from.clos
                    
                    mlo_from.pk = None
                    mlo_from.module = module_to
                    mlo_from.save()
                    print(yellow('\t\t\t\tSkopiowano Modułowy Efekt Kształcenia: %s (id: %s)' % (str(mlo_from.symbol).encode('utf-8'), mlo_from.id)))
                    
                    for clo_from in clos_from.all():
                        # Getting course learning outcome defined for course_year_to with the same symbol as in module_year_from
                        try:
                            clo_to = CourseLearningOutcome.objects.get(course=course_to, symbol=clo_from.symbol)
                        except CourseLearningOutcome.DoesNotExist:
                            print(red("\t\t\t\t\tCourse learning outcome does not exist: %s (id: %s)" % (str(clo_from.symbol).encode('utf-8'), clo_from.id)))
                            continue
                        except CourseLearningOutcome.MultipleObjectsReturned:
                            print(red("\t\t\t\t\tMultiple course learning outcome returned: %s (id: %s)" % (str(clo_from.symbol).encode('utf-8'), clo_from.id)))
                            continue
                        
                        mlo_from.clos.add(clo_to)
                        print(yellow("\t\t\t\t\tReference to course learning outcome has been added: %s (id: %s)" % (str(clo_to.symbol).encode('utf-8'), clo_to.id)))
                
                print('')
            print('')