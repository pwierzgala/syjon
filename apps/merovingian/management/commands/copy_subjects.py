# -*- coding: utf-8 -*-
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import translation

from apps.merovingian.models import Module, SGroup, Subject


class Command(BaseCommand):
    args = '<from_module_id> <to_module_id>'
    help = 'Copies subjects from module with ID=<from_module_id> to module with ID=<to_module_id>.\n'+\
           'If --from-semester is specified only semesters with given number are copied.\n'+\
           'If --to-semester is specified the seester number is overriden.\n'+\
           ' This parameter is available only if --from-semester is specified.'

    option_list = BaseCommand.option_list + (
        make_option('--from-semester',
            action='store',
            dest='from-semester',
            default=None,
            help='Semester from which subjects must be copied.'),
        make_option('--to-semester',
            action='store',
            dest='to-semester',
            default=None,
            help='Semester to which subjects must be copied.'),
    )

    def force_save_module(self, module):
        """
        Goes though all module subjects and saves them to update didactic offer.
        """
        module.name += ' '
        module.save()
        for subject in module.subjects.all():
            subject.name += ' '
            subject.save()

    def copy_subjects(self, old_module, new_module, from_semester=None, to_semester=None):
        """
        Goes though all module subjects with given semester number and copies them to new module.
        """
            
        for subject in old_module.subjects.all():

            if from_semester is not None and subject.semester != from_semester:
                continue

            check_semester = to_semester if to_semester is not None else subject.semester

            existing_subjects = new_module.subjects.filter(name__iexact=subject.name,
                                                              type=subject.type,
                                                              semester=check_semester)

            if len(existing_subjects) > 0:
                continue

            old_subject_pk = subject.pk

            subject.pk = None
            subject.save()
            new_subject = subject

            if to_semester is not None:
                new_subject.semester = to_semester

            new_subject.module = new_module
            new_subject.save()
            
            old_subject = Subject.objects.get(pk=old_subject_pk)
            for subject_teacher in old_subject.subjecttoteacher_set.all():
                subject_teacher.pk = None
                subject_teacher.subject = new_subject
                subject_teacher.save()

        print('Copied module {0}'.format(new_module))
            
    def handle(self, *args, **options):
        
        translation.activate(getattr(settings, 'LANGUAGE_CODE', settings.LANGUAGE_CODE))
        
        if len(args) != 2:
            raise CommandError('Wrong number of parameters. Expected 2: ' + self.args)

        from_semester = int(options['from-semester'])
        to_semester = int(options['to-semester'])

        if to_semester is not None and from_semester is None:
            raise CommandError('Parameter --from-semester is required when --to-semester is given.')

        from_module_id = int(args[0])
        to_module_id = int(args[1])
        
        from_module = Module.objects.get(pk=from_module_id)
        to_module = Module.objects.get(pk=to_module_id)

        with transaction.atomic():
            self.copy_subjects(from_module, to_module,
                               from_semester=from_semester, to_semester=to_semester)
            self.force_save_module(to_module)
