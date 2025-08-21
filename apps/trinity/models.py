# -*- coding: utf-8 -*-

from django.core.cache import cache
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from apps.merovingian.models import Course, CourseProfile, Module, Subject
from apps.syjon.lib.validators import validate_white_space
from apps.trainman.models import UserProfile


class TrinityProfile(models.Model):
    class Meta:
        verbose_name = _(u'Administrator')
        verbose_name_plural = _(u'Administrators')

    user_profile = models.OneToOneField(UserProfile, verbose_name=_(u'User'))
    courses = models.ManyToManyField(Course, blank=True)
    
    def __str__(self):
        return self.user_profile.user.username
    
    @staticmethod
    def get_courses(user):
        if user.is_superuser:
            return Course.objects.active()
        else:
            return TrinityProfile.objects.get(user_profile=user.userprofile).courses.filter(is_active=True)


# ---------------------------------------------------
# --- EDUCATION AREAS
# ---------------------------------------------------

class EducationArea(models.Model):
    class Meta:
        verbose_name = _(u'Area of education')
        verbose_name_plural = _(u'Areas of education')
        ordering = ('name', )
        
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class KnowledgeArea(models.Model):
    class Meta:
        verbose_name = _(u'Area of knowledge')
        verbose_name_plural = _(u'Areas of knowledge')
        ordering = ('name', )
        
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name   


class EducationField(models.Model):
    class Meta:
        verbose_name = _(u'Field of science')
        verbose_name_plural = _(u'Fields of science')
        ordering = ('name', )
        
    name = models.CharField(max_length=255)
    knowledge_area = models.ForeignKey('KnowledgeArea')

    def __str__(self):
        return self.name


class EducationDiscipline(models.Model):
    class Meta:
        verbose_name = _(u'Discipline of science')
        verbose_name_plural = _(u'Disciplines of science')
        ordering = ('name', )
        
    name = models.CharField(max_length=255)
    education_field = models.ForeignKey(EducationField, null=True, blank=True)

    def __str__(self):
        return self.name


class LeadingDiscipline(models.Model):
    class Meta:
        verbose_name = "Dyscyplina wiodąca"
        verbose_name_plural = "Dyscypliny wiodące"
        ordering = ('name',)

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# ---------------------------------------------------
# --- CHARACTERISTIC
# ---------------------------------------------------

class LearningOutcomeAspect(models.Model):
    class Meta:
        verbose_name = _('Aspekt charakterystyki')
        verbose_name_plural = _('Aspekty charakterystyk')

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class LearningOutcomeCharacteristic(models.Model):
    class Meta:
        verbose_name = _('Charakterystyka efektu uczenia się')
        verbose_name_plural = _('Charakterystyki efektów uczenia się')
        ordering = ('symbol', )

    symbol = models.CharField(max_length=16, validators=[validate_white_space])
    description = models.TextField(validators=[validate_white_space])
    level = models.IntegerField()
    education_category = models.ForeignKey('EducationCategory')
    aspect = models.ForeignKey('LearningOutcomeAspect', null=True)

    @classmethod
    def get_for_course_level(cls, educational_level):
        edu_level_to_loc_level = {
            8: 6,  # I stopień
            9: 7,  # II stopień
            11: 7  # jednolite magisterskie
        }
        locs = LearningOutcomeCharacteristic.objects.filter(
            level=edu_level_to_loc_level[educational_level.id]
        )
        return locs

    def __str__(self):
        return self.symbol


# ---------------------------------------------------
# --- AREA LEARNING OUTCOME
# ---------------------------------------------------

class AreaLearningOutcome(models.Model):
    class Meta:
        verbose_name = _(u'Area learning outcome')
        verbose_name_plural = _(u'Area learning outcomes')
        ordering = ('symbol', )

    symbol = models.CharField(max_length=16, validators=[validate_white_space])
    description = models.TextField(validators=[validate_white_space])
    education_area = models.ForeignKey('EducationArea')
    education_level = models.ForeignKey('merovingian.CourseLevel')
    education_profile = models.ForeignKey(CourseProfile)
    education_category = models.ForeignKey('EducationCategory')

    def __str__(self):
        return self.symbol


# ---------------------------------------------------
# --- COURSE LEARNING OUTCOMES
# ---------------------------------------------------

class EducationCategory(models.Model):
    class Meta:
        verbose_name = _(u'Education category')
        verbose_name_plural = _(u'Education categories')
        ordering = ('-name', )

    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class CourseLearningOutcome(models.Model):
    class Meta:
        verbose_name = _(u'Course learning outcome')
        verbose_name_plural = _(u'Course learning outcomes')
        ordering = ('symbol', )

    course = models.ForeignKey(Course, related_name='clos')
    education_category = models.ForeignKey('EducationCategory')
    symbol = models.CharField(max_length=16, validators=[validate_white_space])
    description = models.TextField(validators=[validate_white_space])
    alos = models.ManyToManyField('AreaLearningOutcome', related_name='clos')
    locs = models.ManyToManyField('LearningOutcomeCharacteristic', related_name='locs')
    
    def __str__(self):
        return self.symbol
    
    def get_related_modules(self):
        """
        Zwraca zbiór modułów powiązanych z kierunkowym efektem kształcenia.
        """
        related_modules = Module.objects.filter(mlos__clos=self).only(
            'id', 'name', 'sgroup'
        ).distinct().select_related('sgroup').annotate(intensity=Count('mlos'))

        return related_modules


# ---------------------------------------------------
# --- MODULE LEARNING OUTCOMES
# ---------------------------------------------------

class ModuleLearningOutcome(models.Model):
    class Meta:
        verbose_name = _(u'Module learning outcome')
        verbose_name_plural = _(u'Module learning outcomes')
        ordering = ('symbol', )

    module = models.ForeignKey(Module, related_name='mlos')
    symbol = models.CharField(max_length=16, validators=[validate_white_space])
    description = models.TextField(validators=[validate_white_space])
    clos = models.ManyToManyField('CourseLearningOutcome', related_name='mlos')
    
    def get_related_alos(self):
        """
        Zwraca zbiór obszarowych efketów kształcenia powiązanych z modułowym efektem kształcenia.
        """
        return AreaLearningOutcome.objects.filter(clos__mlos=self).distinct()

    def get_related_locs(self):
        return LearningOutcomeCharacteristic.objects.filter(locs__mlos=self).distinct()

    def __str__(self):
        return self.symbol


# ---------------------------------------------------
# --- SUBJECT LEARNING OUTCOMES
# ---------------------------------------------------


class LearningOutcomesEvaluation(models.Model):
    class Meta:
        verbose_name = "Sposób weryfikacji i oceny efektów uczenia się"
        verbose_name_plural = "Sposoby weryfikacji i oceny efektów uczenia się"
        ordering = ('name',)

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class SubjectToModuleLearningOutcome(models.Model):
    class Meta:
        verbose_name = "Przedmiotowy efekt uczenia się"
        verbose_name_plural = "Przedmiotowe efekty uczenia się"
        ordering = ('mlo__symbol',)

    subject = models.ForeignKey(Subject, related_name='subject_to_slos')
    mlo = models.ForeignKey(ModuleLearningOutcome, related_name='module_to_slos')
    loes = models.ManyToManyField(LearningOutcomesEvaluation)
