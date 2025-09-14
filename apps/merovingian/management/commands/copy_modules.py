from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import translation

import syjon
from apps.merovingian.management.commands import copy_module
from apps.merovingian.models import Module, SGroup


class Command(BaseCommand):
    help = (
        'Copies modules (and its subjects) from specialty with ID=<from_sgroup_id> to specialty'
        'with ID=<to_sgroup_id>. If specialty already have module with this name, only subjects '
        'are copied. If subject with given name, semester and type exists, it is ommited.')

    def add_arguments(self, parser):
        parser.add_argument(
            'from_sgroup_id',
            type=int,
            help='ID of the specialty (SGroup) to copy from')
        parser.add_argument(
            'to_sgroup_id',
            type=int,
            help='ID of the specialty (SGroup) to copy to')

    def handle(self, *args, **options):
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))

        from_sgroup_id = options['from_sgroup_id']
        to_sgroup_id = options['to_sgroup_id']

        from_sgroup = SGroup.objects.get(pk=from_sgroup_id)
        to_sgroup = SGroup.objects.get(pk=to_sgroup_id)
        
        copy_module_command = copy_module.Command()
        
        for m in from_sgroup.modules.all():
            copy_module_command.copy_module(m, to_sgroup)
