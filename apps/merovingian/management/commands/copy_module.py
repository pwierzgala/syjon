# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import translation

import syjon
from apps.merovingian.models import Module, SGroup, Subject


class Command(BaseCommand):
    args = '<module_id> <sgroup_id>'
    help = 'Copies module (and its subjects) with ID=<module_id> to specialty with ID=<sgroup_id>.\n'+\
            'If specialty already have module with this name, only subjects are copied.\n'+\
            'If subject with given name, semester and type exists, it is ommited.'

    def force_save_module(self, module):
        """
        Goes though all module subjects and saves them to update didactic offer.
        """
        module.name += ' '
        module.save()
        for subject in module.subjects.all():
            subject.name += ' '
            subject.save()

    def copy_subjects(self, old_module, new_module):
        """
        Goes though all course descendants (subjects, modules) and saves them to duplicate them.
        """
            
        for subject in old_module.subjects.all():

            existing_subjects = new_module.subjects.filter(name__iexact = subject.name,
                                                              type = subject.type,
                                                              semester = subject.semester)

            if len(existing_subjects) > 0:
                continue

            old_subject_pk = subject.pk

            subject.pk = None
            subject.save()
            new_subject = subject
            
            new_subject.module = new_module
            new_subject.save()
            
            old_subject = Subject.objects.get(pk=old_subject_pk)
            for subject_teacher in old_subject.subjecttoteacher_set.all():
                subject_teacher.pk = None
                subject_teacher.subject = new_subject
                subject_teacher.save()
            
    @transaction.atomic()
    def copy_module(self, module, sgroup):
        
        existing_modules = sgroup.modules.filter(name__iexact=module.name)
        if len(existing_modules) == 0:
            
            old_module_pk = module.pk
            
            module.pk = None 
            module.save()
            sgroup.modules.add(module)
            
            old_module = Module.objects.get(pk=old_module_pk)
            new_module = module
            
            for properties in old_module.moduleproperties_set.all():
                properties.pk = None
                properties.module = new_module
                properties.save()
        else:
            new_module = existing_modules[0] 

        self.copy_subjects(old_module, new_module)
        self.force_save_module(new_module)
        
        print('Copied module {0}'.format(new_module))
            
    def handle(self, *args, **options):
        
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))
        
        if len(args) != 2:
            raise CommandError('Wrong number of parameters. Expected 2: ' + self.args)
        
        module_id = int(args[0])
        sgroup_id = int(args[1])
        
        module = Module.objects.get(pk=module_id)
        sgroup = SGroup.objects.get(pk=sgroup_id)
        
        self.copy_module(module, sgroup)
