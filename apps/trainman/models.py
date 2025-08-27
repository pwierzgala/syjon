# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.syjon.lib.validators import validate_white_space

# -------------------------------------------------------
# --- ABSTRACT
# -------------------------------------------------------


class AbstractUniqueName(models.Model):
    class Meta:
        abstract = True
        ordering = ('name',)
        verbose_name = _(u'Name')
        verbose_name_plural = _(u'Names')

    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name=_(u'Name'),
        validators=[MinLengthValidator(2), validate_white_space])

    def __str__(self):
        return str(self.name)


class AbstractName(models.Model):
    class Meta:
        abstract = True
        ordering = ('name',)
        verbose_name = 'Name'
        verbose_name_plural = 'Names'

    name = models.CharField(
        max_length=256,
        verbose_name=_(u'Name'),
        validators=[MinLengthValidator(2), validate_white_space])

    def __str__(self):
        return str(self.name)


# -------------------------------------------------------
# --- USER PROFILE
# -------------------------------------------------------

class UserProfile(models.Model):
    class Meta:
        ordering = ('user__last_name', )
        verbose_name = _(u'User profile')
        verbose_name_plural = _(u"User profiles")
        
    user = models.OneToOneField(
        to=User,
        verbose_name='User',
        on_delete=models.CASCADE)
    second_name = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_(u'Middle name'))
    pesel = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        verbose_name='PESEL',
        validators=[MinLengthValidator(10)])
    department = models.ForeignKey(
        to='Department',
        null=True,
        blank=True,
        verbose_name=_(u'Unit'),
        on_delete=models.SET_NULL)

    def is_in_department(self, department):
        while self.department is not None:
            if self.department == department:
                return True
            else:
                self.department = self.department.department
        return False

    def __str__(self):
        return '%s, %s' % (str(self.user.last_name), str(self.user.first_name))


# -------------------------------------------------------
# --- IDENTITY DOCUMENT
# -------------------------------------------------------

class IdentityDocument(AbstractUniqueName):
    class Meta:
        verbose_name = _(u'ID document')
        verbose_name_plural = _(u'ID documents')


# -------------------------------------------------------
# --- DEPARTMENT
# -------------------------------------------------------


DEPARTMENT_TYPE_FACULTY = 1

class DepartmentType(AbstractUniqueName):
    class Meta:
        verbose_name = _(u'Unit type')
        verbose_name_plural = _(u'Unit types')


class Department(AbstractName):
    class Meta:
        ordering = ('name',)
        verbose_name = _(u'Unit')
        verbose_name_plural = _(u'Units')

    type = models.ForeignKey(
        to='DepartmentType',
        null=True,
        blank=True,
        verbose_name=_(u'Type'),
        on_delete=models.SET_NULL)
    department = models.ForeignKey(
        to='self',
        related_name='+',
        null=True,
        blank=True,
        verbose_name=_(u'Superior unit'),
        on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)
    
    def children(self):
        all = [self]
        step = Department.objects.filter(department_id__exact=self.id)
        while len(step) > 0:
            all += step
            step = Department.objects.filter(department_id__in=step)
        return all
    
    def children_id(self):
        c = []
        for child in self.children():
            c.append(child.id)
        return c
            

# -------------------------------------------------------
# --- TEACHER
# -------------------------------------------------------

class TeacherDegree(AbstractName):
    class Meta:
        verbose_name = _(u'Degree')
        verbose_name_plural = _(u'Deegrees')
        ordering = ('name',)


class TeacherPosition(AbstractName):
    class Meta:
        verbose_name = _(u'Position')
        verbose_name_plural = _(u'Positions')
        ordering = ('name',)


class Teacher(models.Model):
    class Meta:
        ordering = ('user_profile__user__last_name', )
        verbose_name = _(u'Teacher')
        verbose_name_plural = _(u'Teachers')

    user_profile = models.OneToOneField(
        to=UserProfile,
        verbose_name=_(u'User'),
        on_delete=models.CASCADE)
    degree = models.ForeignKey(
        to='TeacherDegree',
        verbose_name=_(u'Degree'),
        on_delete=models.CASCADE)
    position = models.ForeignKey(
        to='TeacherPosition',
        verbose_name=_(u'Position'),
        on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s, %s' % (str(self.user_profile.user.last_name), str(self.user_profile.user.first_name), str(self.degree))

    def get_full_name(self):
        return '%s %s %s' % (str(self.degree), str(self.user_profile.user.first_name), str(self.user_profile.user.last_name))

    def get_subjects(self, **kwargs):
        from apps.merovingian.models import Module
        if 'module' in kwargs:
            return self.subjects.filter(module__exact=kwargs.get('module', Module.objects.none()))
        else:
            return self.subjects.all().distinct()

    def get_modules(self):
        from apps.merovingian.models import Module
        return Module.objects.filter(id__in=[s.module.id for s in self.subjects.all().distinct()])


# -------------------------------------------------------
# --- OCCUPATION
# -------------------------------------------------------

class Occupation(models.Model):
    class Meta:
        verbose_name = _(u'Occupation')
        verbose_name_plural = _(u'Occupations')
        
    name = models.CharField(
        max_length=256,
        verbose_name=_(u'Name'))


class UserOccupation(models.Model):
    class Meta:
        verbose_name = _(u'User Position')
        verbose_name_plural = _(u'Users Positions')
        
    user_profile = models.ForeignKey(
        to=UserProfile,
        verbose_name=_(u'User'),
        on_delete=models.CASCADE)
    department = models.ForeignKey(
        to='Department',
        null=True,
        blank=True,
        verbose_name=_(u'Unit'),
        on_delete=models.SET_NULL)
    occupation = models.ForeignKey(
        to=Occupation,
        null=True,
        blank=True,
        verbose_name=_(u'Occupation'),
        on_delete=models.SET_NULL)
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_(u'start date'))
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_(u'end date'))


# -------------------------------------------------------
# --- SIGNALS
# -------------------------------------------------------

def create_user_profile(**kwargs):
    if kwargs.get('created', False) and not kwargs.get('raw', True):
        UserProfile.objects.create(user=kwargs.get('instance', User.objects.none()))
        
models.signals.post_save.connect(create_user_profile, sender=User)
