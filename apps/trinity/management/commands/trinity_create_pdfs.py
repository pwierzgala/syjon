"""
Created on 27-08-2012

@author: pwierzgala
"""

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

import syjon
from apps.merovingian.models import Course
from apps.syjon.lib.pdf import create_pdf
from apps.trinity.models import CourseLearningOutcome, ModuleLearningOutcome


class Command(BaseCommand):
    help = u'Zapisuje wszystkie efekty kształcenia do pliku.'

    def handle(self, *args, **options):    
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))

        courses = Course.objects.all()
        for course in courses:
            #self.create_clos_pdfs(course)
            self.create_mlos_pdfs(course)

    def create_clos_pdfs(self, course):
        clos = CourseLearningOutcome.objects.filter(course=course)
        template_path = 'trinity/clo/print.html'
        file_name = u'%s.pdf' % (str(course))
        template_context = {'course': course, 'clos': clos}
        output_path=u'/tmp/trinity/clos/'
        create_pdf(template_path, template_context, template_path)
        self.stdout.write('%s\n' % file_name)

    def create_mlos_pdfs(self, course):
        template_path = 'trinity/mlo/print.html'
        for sgroup in course.sgroups.all():
            for module in sgroup.modules.all():
                file_name = u'%s.pdf' % (str(module))
                mlos = ModuleLearningOutcome.objects.filter(module=module)
                template_context = {'course': course, 'sgroup': sgroup, 'module': module, 'mlos': mlos}
                output_path=u'/tmp/trinity/mlos/%s/%s' % (str(sgroup), str(course))

                create_pdf(template_path, template_context, template_path)
                self.stdout.write('%s\n' % file_name)
