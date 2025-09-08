# -*- coding: utf-8 -*-

from datetime import date

from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.urls import reverse
from django.utils.translation import gettext as __
from django.utils.translation import gettext_lazy as _

from apps.merovingian.models import Module, Subject, SubjectToTeacher
from apps.metacortex.managers import (
    DidacticMethodManager, SyllabusModuleManager, SyllabusPracticeManager,
    SyllabusSubjectManager)
from apps.metacortex.settings import (
    SYLLABUS_TYPE_MODULE_ID, SYLLABUS_TYPE_PRACTICE_ID,
    SYLLABUS_TYPE_SUBJECT_ID)
from apps.trainman.models import Department, Teacher
from apps.trinity.models import (
    LearningOutcomesEvaluation, ModuleLearningOutcome)

# ---------------------------------------------------
# --- SYLLABUS
# ---------------------------------------------------

class Syllabus(models.Model):
    class Meta:
        verbose_name = _(u'Syllabus')
        verbose_name_plural = _(u'Syllabuses')

    is_published = models.BooleanField(
        default=False,
        verbose_name=_(u'Published'))
    is_active = models.BooleanField(
        default=True,
        verbose_name=_(u'Active'))
    ectss = models.ManyToManyField(
        to='ECTS',
        blank=True,
        through='SyllabusToECTS')

    def get_show_url(self):
        raise NotImplementedError


# ---------------------------------------------------
# --- ECTS
# ---------------------------------------------------

class SyllabusToECTS(models.Model):
    class Meta:
        ordering = ('-ects__is_default', 'ects__order', 'ects__name',)
        
    syllabus = models.ForeignKey(
        to='Syllabus',
        related_name='syllabus_to_ects',
        on_delete=models.CASCADE)
    ects = models.ForeignKey(
        to='ECTS',
        on_delete=models.CASCADE)
    hours = models.FloatField(null=True, blank=True)

    # This field is used since 2019 reform. It holds number of points assigned to
    # related ECTS activity.
    value = models.IntegerField(null=True, blank=True)
    
    def get_delete_url(self):
        return reverse(
            'metacortex:my:delete_ects',
            kwargs={'id_syllabus': self.syllabus.id, 'id_ects': self.ects.id})

    def __str__(self):
        return "{} - {}, {} ECTS, {}h".format(
            self.syllabus,
            self.ects.name,
            self.value,
            self.hours
        )


class ECTS(models.Model):
    class Meta:
        verbose_name = _(u'ECTS equivalent in hours')
        verbose_name_plural = _(u'ECTS equivalents in hours')
        ordering = ('is_default', 'name')
        
    name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    order = models.IntegerField(null=True, blank=True)
    flag = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return str(self.name[:100]+"...")


# ---------------------------------------------------
# --- SYLLABUS MODULE
# ---------------------------------------------------

class SyllabusModule(Syllabus):
    class Meta:
        verbose_name = _(u'Module syllabus')
        verbose_name_plural = _(u'Module syllabuses')
        ordering = ['module__name']
        
    module = models.OneToOneField(
        to=Module,
        related_name='syllabus',
        on_delete=models.CASCADE)
    module_description = models.TextField(
        blank=True,
        verbose_name=_(u'Module description'))
    lecture_languages = models.ManyToManyField(
        to='LectureLanguage',
        blank=True,
        verbose_name=_(u'Languages'),
        related_name='lecturelanguages')
    unit_source = models.ForeignKey(
        to=Department,
        null=True,
        blank=True,
        related_name='unit_source',
        verbose_name=_(u'Source unit (the one that the module is offered by)'),
        on_delete=models.SET_NULL)
    unit_target = models.ForeignKey(
        to=Department,
        null=True,
        blank=True,
        related_name='unit_target',
        verbose_name=_(u'Target unit (the one that the module is offered for)'),
        on_delete=models.SET_NULL)
    coordinator = models.ForeignKey(
        to=Teacher,
        null=True,
        blank=True,
        related_name='module_coordinator',
        verbose_name=_(u'Coordinator'),
        on_delete=models.SET_NULL)
    additional_information = models.TextField(
        blank=True,
        verbose_name=_(u'Additional remarks'))
    loes = models.ManyToManyField(
        to=LearningOutcomesEvaluation,
        blank=True,
        verbose_name='Sposoby weryfikacji i oceny efektów uczenia się')

    objects = SyllabusModuleManager

    def get_show_url(self):
        return reverse(
            'metacortex:search:show',
            kwargs={'syllabus_type': 0, 'syllabus_id': self.pk})

    @property
    def syllabus_type(self):
        return SYLLABUS_TYPE_MODULE_ID
    
    def __str__(self):
        return self.module.name


# ---------------------------------------------------
# --- SYLLABUS SUBJECT
# ---------------------------------------------------

class AbstractSyllabusSubject(models.Model):
    class Meta:
        abstract = True
        
    subject = models.ForeignKey(
        to=Subject,
        on_delete=models.CASCADE)
    learning_outcomes_verification = models.TextField(
        blank=True,
        verbose_name=_(u'Sposób weryfikacji efektów kształcenia'))
    
    def get_hours(self):
        return self.subject.hours
        
    def get_ects(self):
        """Zwraca liczbę punktów ECTS przedmiotu sylabusa."""
        return self.subject.ects

    def get_hours_equivalent_of_ects(self):
        """Zwraca godzinowy ekwiwalnet puntków ECTS przedmiotu sylabusa."""
        return self.get_ects()*30

    def display_ects_section(self):
        """
        Zwraca wartość True jeżeli dla sylabusa powinna zostać wyświetlona sekcja ECTS.
        Sekcja ECTS dla sylabusa zostanie wyświetlona jeżeli przedmiot sylabusa ma okresloną liczbę
        puntków ECTS.
        """
        if self.subject.ects:
            return True
        return False


class SyllabusSubject(Syllabus, AbstractSyllabusSubject):
    class Meta:
        verbose_name = _(u'Subject syllabus')
        verbose_name_plural = _(u'Subject syllabuses')
        ordering = ['subject__name']

    additional_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(u'Title of course or additional information regarding the course name')
    )
    initial_requirements = models.TextField(
        blank=True,
        verbose_name=_(u'Prerequisities'))
    literature = models.TextField(
        blank=True,
        verbose_name=_(u'Reading list'))
    subjects_scope = models.TextField(
        blank=True,
        verbose_name=_(u'List of topics'))
    assessment_conditions = models.TextField(
        null=True,
        blank=True,
        verbose_name=_(u'Assessment conditions'))
    additional_information = models.TextField(
        blank=True,
        verbose_name=_(u'Additional remarks'))
    education_effects = models.TextField(
        blank=True,
        verbose_name=_(u'Additional learning outcomes'))
    module_learning_outcomes = models.ManyToManyField(
        ModuleLearningOutcome,
        blank=True,
        verbose_name=_(u'Module learning outcomes'))
    didactic_methods = models.ManyToManyField(
        to='DidacticMethod',
        blank=True,
        verbose_name=_(u'Teaching methods'))
    assessment_forms = models.ManyToManyField(
        to='AssessmentForm',
        blank=True,
        verbose_name=_(u'Evaluation form'))
    teacher = models.ForeignKey(
        to=Teacher,
        on_delete=models.CASCADE)

    objects = SyllabusSubjectManager

    def get_show_url(self):
        return reverse(
            'metacortex:search:show',
            kwargs={'syllabus_type': 1, 'syllabus_id': self.pk}
        )

    @property
    def syllabus_type(self):
        return SYLLABUS_TYPE_SUBJECT_ID
    
    def get_name(self):
        name = self.subject.name
        if self.additional_name:
            name += ' - %s' % self.additional_name
        return name                    
    
    def __str__(self):
        syllabus_name = self.get_name()
        syllabus_name += ", %s %s" % (self.subject.hours, __(u"h"))
        syllabus_name += ", %s" % self.subject.type.name
        syllabus_name += " (%s)" % str(self.teacher)
        return syllabus_name


# ---------------------------------------------------
# --- SYLLABUS PRACTICE
# ---------------------------------------------------    

class SyllabusPractice(Syllabus, AbstractSyllabusSubject):
    class Meta:
        verbose_name = _(u'Practice syllabus')
        verbose_name_plural = _(u'Practice syllabuses')
        ordering = ['subject__name']
        
    teacher = models.ForeignKey(
        to=Teacher,
        on_delete=models.CASCADE)
    type = models.ForeignKey(
        to='PracticeType',
        null=True,
        blank=True,
        verbose_name=_(u'Type'),
        on_delete=models.SET_NULL)
    description = models.TextField(
        blank=True,
        verbose_name=_(u'Description'))
    education_effects = models.TextField(
        blank=True,
        verbose_name=_(u'Additional learning outcomes'))
    additional_information = models.TextField(
        blank=True,
        verbose_name=_(u'Additional remarks'))

    objects = SyllabusPracticeManager

    def get_show_url(self):
        return reverse(
            'metacortex:search:show',
            kwargs={'syllabus_type': 2, 'id_syllabus': self.pk})

    @property
    def syllabus_type(self):
        return SYLLABUS_TYPE_PRACTICE_ID
    
    def __str__(self):
        syllabus_name = self.subject.name
        syllabus_name += ", %s %s" % (self.subject.hours, __(u"h"))
        syllabus_name += ", %s" % self.subject.type.name
        syllabus_name += " (%s)" % str(self.teacher)
        return syllabus_name


# ---------------------------------------------------
# --- PRACTICE TYPE
# ---------------------------------------------------  

class PracticeType(models.Model):
    class Meta:
        verbose_name = _(u'Type of practice')
        verbose_name_plural = _(u'Types of practices')
    
    name = models.CharField(max_length=64)
    
    def __str__(self):
        return str(self.name)
    
# ---------------------------------------------------
# --- LECTURE LANGUAGE
# ---------------------------------------------------      


class LectureLanguage(models.Model):
    class Meta:
        verbose_name = _(u'Language')
        verbose_name_plural = _(u'Languages')
      
    name = models.CharField(max_length=64)
    
    def __str__(self):
        return str(self.name)
    

# ---------------------------------------------------
# --- DIDACTIC METHOD
# ---------------------------------------------------

class DidacticMethod(models.Model):
    class Meta:
        verbose_name = 'Metoda dydaktyczna'
        verbose_name_plural = 'Metody dydaktyczne'
        ordering = ['order', 'name']
    
    name = models.CharField(max_length=128)
    order = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    objects = DidacticMethodManager
    
    def __str__(self):
        return str(self.name)

# ---------------------------------------------------
# --- ASSESSMENT FORM
# ---------------------------------------------------  


class AssessmentForm(models.Model):
    class Meta:
        verbose_name = _(u'Evaluation form')
        verbose_name_plural = _(u'Evaluation forms')
        ordering = ['order', 'name']
    
    name = models.CharField(max_length=128)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.name)


# ---------------------------------------------------
# --- YEARS
# ---------------------------------------------------

class SyllabusYear(models.Model):
    class Meta:
        verbose_name = _(u'Syllabus year')
        verbose_name_plural = _(u'Syllabuses years')
        ordering = ['-date', ]
        
    date = models.DateField()
    read_only = models.BooleanField(default=False)
    
    def get_previous(self):
        previous_year = self.date.year-1
        try:
            return SyllabusYear.objects.get(date__year=previous_year)
        except:
            return None
    
    def __str__(self):
        return str(self.date.year)

    def get_name_with_current_year(self):
        years_delta = relativedelta(date.today(), self.date).years+1
        return u'{0} (obecnie rok studiów: {1})'.format(str(self.date.year), years_delta)


# ---------------------------------------------------
# --- SIGNALS
# ---------------------------------------------------


def module_post_save(instance, created, **kwargs):
    coordinator = instance.coordinator
    if not created:
        try:
            defaults = {'is_active': True, 'coordinator': coordinator}
            if coordinator is None:
                defaults = {'is_active': False, 'coordinator': None}
            SyllabusModule.objects.update_or_create(module=instance, defaults=defaults)
        except SyllabusModule.MultipleObjectsReturned:
            pass


post_save.connect(receiver=module_post_save, sender=Module)


def subject_to_teacher_post_save(instance, created, **kwargs):
    if created:
        teacher = instance.teacher
        subject = instance.subject
        if subject.type.is_practice():
            SyllabusPractice.objects.update_or_create(
                subject=subject, teacher=teacher, defaults={'is_active': True})
        else:
            syllabus, _ = SyllabusSubject.objects.update_or_create(
                subject=subject,
                teacher=teacher,
                defaults={'is_active': True})


def subject_to_teacher_pre_delete(instance, **kwargs):
    teacher = instance.teacher
    subject = instance.subject

    if subject.type.is_practice():
        SyllabusPractice.objects.filter(subject=subject, teacher=teacher).update(is_active=False)
    else:
        SyllabusSubject.objects.filter(subject=subject, teacher=teacher).update(is_active=False)


post_save.connect(receiver=subject_to_teacher_post_save, sender=SubjectToTeacher)
pre_delete.connect(receiver=subject_to_teacher_pre_delete, sender=SubjectToTeacher)
