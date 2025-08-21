'''
Created on 13-05-2013

@author: Damian Rusinek <damian.rusinek@gmail.com>
'''
import csv
import os
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import translation

import syjon
from apps.merovingian.models import Subject, SubjectToTeacher
from apps.trainman.models import Teacher


class Command(BaseCommand):
    
    args = '<file_path> [--override]'
    
    help = """Loads workload for teachers. File should be CSV file constructed as following:
order number, module id, teacher id (model: teacher), number of groups, numer of hours.
First should contain headers and is ommited.
"""
    
    option_list = BaseCommand.option_list + (
                    make_option('--override',
                        action = 'store_true',
                        dest = 'override',
                        default = False,
                        help = 'Override numbers of groups and hours if teacher is already assigned to subject'
                    ),
                )
    
    def _load_workload(self, csvfile, override=False, check_only=True):
        
        already_exist = 0
        already_exist_with_different_data = 0
        newly_added = 0
        different_module_ids = 0
        teachers_not_found = 0
        subjects_not_found = 0
        
        first_row = True
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for r in reader:
            
            if first_row:
                first_row = False
                continue
            
            module_id = int(r[1])
            subject_id = int(r[2])
            teacher_id = int(r[3])
            groups = int(r[4])
            hours = int(r[5])
            
            try:
                subject = Subject.objects.get(pk=subject_id)
            except Subject.DoesNotExist:
                subjects_not_found += 1
                continue 
            
            if subject.module.id != module_id:
                print("Subject %s is in module %d (system), not %d (csv)." % (subject.name, subject.module.id, module_id))
                different_module_ids += 1
                continue
            
            try: 
                teacher = Teacher.objects.get(pk=teacher_id)
            except Teacher.DoesNotExist:
                teachers_not_found += 1
                continue
            
            assignations = SubjectToTeacher.objects.filter(subject=subject, teacher=teacher).all()
            if len(assignations) > 0:
                already_exist += 1
                assignation = assignations[0]
                if assignation.groups != groups or assignation.hours != hours:
                    already_exist_with_different_data += 1
                
                    if not check_only and override:
                        assignation.groups = groups
                        assignation.hours = hours
                        assignation.save()
                    
            else:
                newly_added += 1
                if not check_only:
                    assignation = SubjectToTeacher()
                    assignation.teacher = teacher
                    assignation.subject = subject
                    assignation.groups = groups
                    assignation.hours = hours
                    assignation.save()
                
        if check_only:
            print("Changes to be commited:")
        else:
            print("Commited changes:")
                    
        print("Already existing workload: %d.                      \tOmmited" % already_exist)
        print("Teachers not found: %d.                                \tOmmited" % teachers_not_found)
        print("Subjects not found: %d.                                \tOmmited" % subjects_not_found)
        print("Subjects with different modules: %d.                   \tOmmited" % different_module_ids)
        if override:
            print("Already existing workload with different data: %d.    \tOverriden" % already_exist_with_different_data)
        else:
            print("Already existing workload with different data: %d.    \tOmmited" % already_exist_with_different_data)
        print("ADDED: %d.                                            \tAdded" % newly_added)
    
    def handle(self, *args, **kwargs):
        
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))
    
        if len(args) != 1:
            print("Wrong number of parameters!")
            print("Use --help to check.")
            return
        
        if not os.path.isfile(args[0]):
            print("File " + args[0] + " does not exist!")
            return
        
        override = kwargs['override']

        csvfile = open(args[0], 'rb')
        self._load_workload(csvfile, override, check_only=True)
        
        confirm = input('Continue? [yY]')
        if confirm.lower() == 'y':
            with transaction.atomic():
                csvfile = open(args[0], 'rb')
                self._load_workload(csvfile, override, check_only=False)
                        