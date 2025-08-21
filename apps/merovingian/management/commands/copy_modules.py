# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import translation

import syjon
from apps.merovingian.management.commands import copy_module
from apps.merovingian.models import Module, SGroup


class Command(BaseCommand):
    args = '<from_sgroup_id> <to_sgroup_id>'
    help = 'Copies modules (and its subjects) from specialty with ID=<from_sgroup_id> to specialty with ID=<to_sgroup_id>.\n'+\
            'If specialty already have module with this name, only subjects are copied.\n'+\
            'If subject with given name, semester and type exists, it is ommited.'

    def handle(self, *args, **options):
        
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))
        
        if len(args) != 2:
            raise CommandError('Wrong number of parameters. Expected 2: ' + self.args)
        
        from_sgroup_id = int(args[0])
        to_sgroup_id = int(args[1])
        
        from_sgroup = SGroup.objects.get(pk=from_sgroup_id)
        to_sgroup = SGroup.objects.get(pk=to_sgroup_id)
        
        copy_module_command = copy_module.Command()
        
        for m in from_sgroup.modules.all():
            copy_module_command.copy_module(m, to_sgroup)
