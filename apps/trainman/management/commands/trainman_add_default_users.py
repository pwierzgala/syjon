# -*- coding: utf-8 -*-
'''
Created on 11-04-2013

@author: pwierzgala
'''

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import termcolors, translation

import syjon
from apps.trainman.models import Teacher, TeacherDegree, TeacherPosition

green = termcolors.make_style(fg='green')
yellow = termcolors.make_style(fg='yellow')
cyan = termcolors.make_style(fg='cyan')
red = termcolors.make_style(fg='red', opts=('bold',))
bold = termcolors.make_style(opts=('bold',))

default_users = [
                 {'username':'gagik_makaryan', 'first_name': 'Gagik', 'last_name': 'Makaryan', 'password': 'dns73', 'email': 'makaryan@employers.am', 'is_staff': False, 'is_superuser': True, 'teacher': {'degree': 1, 'position': 1}},
                 {'username':'msmolira', 'first_name': 'Marcin', 'last_name': 'Smolira', 'password': 'xxx', 'email': 'marcin.smolira@gmail.com', 'is_staff': True, 'is_superuser': True, 'teacher': {'degree': 2, 'position': 2}},
                 {'username':'test_01', 'first_name': 'Test', 'last_name': '01', 'password': 'test_01', 'email': 'test_01@gmail.com', 'is_staff': True, 'is_superuser': True, 'teacher': {'degree': 1, 'position': 1}},
                 {'username':'test_02', 'first_name': 'Test', 'last_name': '02', 'password': 'test_02', 'email': 'test_02@gmail.com', 'is_staff': True, 'is_superuser': True, 'teacher': {'degree': 1, 'position': 1}},
                 {'username':'test_03', 'first_name': 'Test', 'last_name': '03', 'password': 'test_03', 'email': 'test_03@gmail.com', 'is_staff': True, 'is_superuser': True, 'teacher': {'degree': 1, 'position': 1}},
                 {'username':'test_04', 'first_name': 'Test', 'last_name': '04', 'password': 'test_04', 'email': 'test_04@gmail.com', 'is_staff': True, 'is_superuser': True, 'teacher': {'degree': 1, 'position': 1}},
                 {'username':'test_05', 'first_name': 'Test', 'last_name': '05', 'password': 'test_05', 'email': 'test_05@gmail.com', 'is_staff': True, 'is_superuser': True, 'teacher': {'degree': 1, 'position': 1}},
                 {'username':'test_06', 'first_name': 'Test', 'last_name': '06', 'password': 'test_06', 'email': 'test_06@gmail.com', 'is_staff': True, 'is_superuser': True, 'teacher': {'degree': 1, 'position': 1}},
                 {'username':'test_07', 'first_name': 'Test', 'last_name': '07', 'password': 'test_07', 'email': 'test_07@gmail.com', 'is_staff': True, 'is_superuser': True, 'teacher': {'degree': 1, 'position': 1}},
                 {'username':'test_08', 'first_name': 'Test', 'last_name': '08', 'password': 'test_08', 'email': 'test_08@gmail.com', 'is_staff': True, 'is_superuser': True, 'teacher': {'degree': 1, 'position': 1}},
                 {'username':'test_09', 'first_name': 'Test', 'last_name': '09', 'password': 'test_09', 'email': 'test_09@gmail.com', 'is_staff': True, 'is_superuser': True, 'teacher': {'degree': 1, 'position': 1}},
                 {'username':'test_10', 'first_name': 'Test', 'last_name': '10', 'password': 'test_10', 'email': 'test_10@gmail.com', 'is_staff': True, 'is_superuser': True, 'teacher': {'degree': 1, 'position': 1}},
                 ]


class Command(BaseCommand):
    help = u'Dodaje domyślnych użytkowników aplikacji.'

    @transaction.atomic()
    def handle(self, *args, **options):
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))
        
        for default_user in default_users:           
            (u, created) = User.objects.get_or_create(username = default_user['username'])
            if created:
                self.stdout.write('%s\n' % bold('CREATED'))
            else:
                self.stdout.write('%s\n' % bold('GET'))
            u.username = default_user['username']
            u.email = default_user['email']
            u.first_name = default_user['first_name']
            u.last_name = default_user['last_name']
            u.set_password(default_user['password'])
            u.is_staff = default_user['is_staff']
            u.is_superuser = default_user['is_superuser']
            u.save()
            
            self.stdout.write('Username: %s\n' % bold(str(default_user['username'])).encode('utf-8'))
            self.stdout.write('First name: %s\n' % str(default_user['first_name']).encode('utf-8'))
            self.stdout.write('Last_name: %s\n' % str(default_user['last_name']).encode('utf-8'))
            self.stdout.write(u'Email: %s\n' % default_user['email'])
            self.stdout.write(u'Password: %s\n' % default_user['password'])
            self.stdout.write(u'Is staff: %s\n' % default_user['is_staff'])
            self.stdout.write(u'Is superuser: %s\n' % default_user['is_superuser'])
            
            if 'teacher' in default_user:
                degree = TeacherDegree.objects.get(pk = default_user['teacher']['degree'])
                position = TeacherPosition.objects.get(pk = default_user['teacher']['position'])
                created = False
                try:
                    t = Teacher.objects.get(user_profile = u.userprofile)
                except Teacher.DoesNotExists:
                    t = Teacher()
                    t.degree = degree
                    t.position = position
                    t.saver()
                    created = True
                
                self.stdout.write('Teacher (%s)\n' % bold('CREATED' if created else 'GET'))
                self.stdout.write('Position: %s\n' % str(position).encode('utf-8'))
                self.stdout.write('Degree: %s\n' % str(degree).encode('utf-8'))
