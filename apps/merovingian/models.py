# -*- coding: utf-8 -*-

import math

from django.core.validators import (
    MaxValueValidator, MinLengthValidator, MinValueValidator)
from django.db import models
from django.utils.translation import gettext_lazy as _

import syjon
from apps.merovingian.functions import default_sgroup_name
from apps.merovingian.managers import (
    CourseManager, ModuleManager, SGroupManager, SubjectManager)
from apps.syjon.lib.functions import to_roman
from apps.syjon.lib.validators import validate_white_space
from syjon import settings


def semesters_list():
    """Returns the list with numbers of all possible semesters."""
    return range(1, 11)
semester_minimal = semesters_list()[0]
semester_maximal = semesters_list()[len(semesters_list())-1]


# -------------------------------------------------------
# --- ABSTRACT UNIQUE NAME
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
        verbose_name=_(u'name'),
        validators=[MinLengthValidator(2), validate_white_space])

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super(AbstractUniqueName, self).save(*args, **kwargs)


# -------------------------------------------------------
# --- ABSTRACT NAME
# -------------------------------------------------------

class AbstractName(models.Model):
    class Meta:
        abstract = True
        ordering = ('name',)
        verbose_name = _(u'Name')
        verbose_name_plural = _(u'Names')

    name = models.CharField(
        max_length=256,
        verbose_name=_(u'name'),
        validators=[MinLengthValidator(2), validate_white_space])

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super(AbstractName, self).save(*args, **kwargs)


# -------------------------------------------------------
# --- ABSTRACT ACTIVE
# -------------------------------------------------------

class AbstractActive(AbstractName):
    class Meta:
        abstract = True
        ordering = ('-is_active', 'name')
        verbose_name = _(u'Name, active')
        verbose_name_plural = _(u'Names, active')
        
    is_active = models.BooleanField(default=True, verbose_name=_(u'Active'))

    def __str__(self):
        return '%s, %s' % (str(self.name), str(self.is_active))

    def set_active(self, active):
        self.is_active = active
        self.save()


# -------------------------------------------------------
# --- ABSTRACT DIDACTIC OFFER
# -------------------------------------------------------

class AbstractDidacticOffer(AbstractActive):
    class Meta:
        abstract = True
        ordering = ('-is_active', 'name')
        verbose_name = _(u'Teaching offer record')
        verbose_name_plural = _(u'Teaching offer records')

    didactic_offer = models.ForeignKey(
        to='DidacticOffer',
        null=True,
        blank=True,
        verbose_name=_(u'Teaching offer'),
        on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)

    def get_start_date(self):
        raise NotImplementedError

    def get_end_date(self):
        raise NotImplementedError

    def get_prev(self):
        raise NotImplementedError

    def get_next(self):
        raise NotImplementedError

    def is_course_first(self):
        raise NotImplementedError

    def is_course_last(self):
        raise NotImplementedError

    def _find_offer_for_date(self, offers, date):
        for offer in offers:
            if offer.start_date <= date <= offer.end_date:
                return offer
        return None

    def date(self, date, sem=0, begin=True):
        """
        Returns the date of current didactic offer after sem semesters.
        It will be the beginning or ending date of current didactic offer but with replaced year.
        
        It is used to calculate i.e. the start and end date of course.
        """
        
        def find_active_offer(offers):
            for offer in offers:
                if offer.is_active:
                    return offer
            return None
        
        if not date:
            return None
        
        if sem < 0:
            sem = 0
        
        didactic_offers = DidacticOffer.objects.order_by('start_date')
        i = 0
        offers_cnt = len(didactic_offers)
        while i < offers_cnt:
            offer = didactic_offers[i]
            if offer.start_date <= date <= offer.end_date:
                break
            i += 1

        i += sem

        if i >= offers_cnt:
            return None

        offer = didactic_offers[i]
        if begin:
            return offer.start_date
        else:
            return offer.end_date

    def diff(self, date0, date1):
        """
        Return the number of semesters between dates date0 and date1.
        """
        offers = DidacticOffer.objects.order_by('start_date')

        offer0 = self._find_offer_for_date(offers, date0)
        offer1 = self._find_offer_for_date(offers, date1)
        
        if not offer0 or not offer1:
            return None
        
        if date0 < date1:
            start_offer = offer0
            end_offer = offer1
        else:
            start_offer = offer1
            end_offer = offer0
        
        semester = 0
        for offer in offers:
            if offer == end_offer:
                break
            elif offer == start_offer:
                semester = 1
            elif semester > 0:
                semester += 1
        return semester 


# -------------------------------------------------------
# --- SETTINGS
# -------------------------------------------------------

class MerovingianSettings(models.Model):
    class Meta:
        verbose_name = _(u'Merowing Settings')
        verbose_name_plural = _(u'Merowing Settings')

    key = models.CharField(max_length=32, unique=True, verbose_name=_(u'key'))
    value = models.CharField(max_length=128, verbose_name=_(u'value'))

    def __str__(self):
        return '%s: %s' % (str(self.key), str(self.value))


# -------------------------------------------------------
# --- MEROVINGIAN ADMIN
# -------------------------------------------------------

class MerovingianAdmin(models.Model):
    class Meta:
        verbose_name = _(u'Merowing Administrator')
        verbose_name_plural = _(u'Merowing Administrator')

    user_profile = models.OneToOneField(
        to='trainman.UserProfile',
        verbose_name=_(u'User'),
        on_delete=models.CASCADE)
    temporary_privileged_access = models.BooleanField(
        default=False,
        verbose_name=_(u'Temporary Privileged Access'))
    courses = models.ManyToManyField(
        to='Course',
        blank=True,
        verbose_name=_(u'Managed courses'))

    def __str__(self):
        return str(self.user_profile)


# -------------------------------------------------------
# --- DIDACTIC OFFER
# -------------------------------------------------------

class DidacticOffer(AbstractActive):
    class Meta:
        verbose_name = _(u'Teaching offer')
        verbose_name_plural = _(u'Teaching offers')

    start_date = models.DateField(verbose_name=_(u'start date'))
    end_date = models.DateField(verbose_name=_(u'end date'))

    def __str__(self):
        return '%s, %s, %s - %s' % (
            str(self.name), str(self.is_active), str(self.start_date), str(self.end_date)
        )

    def save(self, *args, **kwargs):
        if self.is_active:
            for d in DidacticOffer.objects.filter(is_active=True):
                d.set_active(False)
        super(DidacticOffer, self).save(*args, **kwargs)


# -------------------------------------------------------
# --- COURSE
# -------------------------------------------------------

LEVEL_BA = 8
LEVEL_MSC = 9
LEVEL_PHD = 10
LEVEL_U_MSC = 11
LEVEL_ENG = 12
LEVEL_PG_Q = 13  # Q - Qualifying
LEVEL_PG_FL = 14  # FL - Final learning


class CourseLevel(AbstractUniqueName):
    class Meta:
        verbose_name = _(u'Education level')
        verbose_name_plural = _(u'Education levels')


class CourseType(AbstractUniqueName):
    class Meta:
        verbose_name = _(u'Course type')
        verbose_name_plural = _(u'Course types')


class CourseProfile(AbstractUniqueName):
    class Meta:
        verbose_name = _(u'Education profile')
        verbose_name_plural = _(u'Education profiles')


class Course(AbstractDidacticOffer):
    class Meta:
        ordering = ('-is_active', 'name', '-level__name', '-type__name', 'profile__name', 'start_date', )
        verbose_name = _(u'Course')
        verbose_name_plural = _(u'Courses')
        permissions = (('assign_education_area_course', 'Can assign education area'), )

    semesters = models.IntegerField(null=True, blank=True, verbose_name=_(u'Number of semesters'))
    years = models.IntegerField(null=True, blank=True, verbose_name=_(u'Number of years'))
    start_date = models.DateField(null=True, blank=True, verbose_name=_(u'Start date'))
    end_date = models.DateField(null=True, blank=True, verbose_name=_(u'End date'))
    level = models.ForeignKey(
        to='CourseLevel',
        verbose_name=_(u'Education level'),
        on_delete=models.CASCADE)
    type = models.ForeignKey(
        to='CourseType',
        verbose_name=_(u'Typ'),
        on_delete=models.CASCADE)
    profile = models.ForeignKey(
        to='CourseProfile',
        null=True,
        blank=True,
        verbose_name=_(u'Education profile'),
        on_delete=models.SET_NULL)
    department = models.ForeignKey(
        to='trainman.Department',
        null=True,
        blank=True,
        verbose_name=_(u'Unit'),
        on_delete=models.SET_NULL)
    is_first = models.BooleanField(null=True, blank=True, verbose_name=_(u'First'))
    is_last = models.BooleanField(null=True, blank=True, verbose_name=_(u'Last'))
    education_areas = models.ManyToManyField(to='trinity.EducationArea', blank=True)
    knowledge_areas = models.ManyToManyField(to='trinity.KnowledgeArea', blank=True)
    education_fields = models.ManyToManyField(to='trinity.EducationField', blank=True)
    education_disciplines = models.ManyToManyField(to='trinity.EducationDiscipline', blank=True)
    leading_discipline = models.ManyToManyField(to='trinity.LeadingDiscipline', blank=True)

    objects = CourseManager

    def __str__(self):
        if self.years:
            sem_desc = "[%s %s]" % (str(self.years), _(u'years'))
        else:
            sem_desc = "[%s %s]" % (str(self.semesters), _(u'sems'))
        s = u'%s, %s %s, %s' % (str(self.name), str(self.level), sem_desc, str(self.type))

        if self.type.id not in (LEVEL_PG_Q, LEVEL_PG_FL) and self.profile is not None:
            s += u', %s' % str(self.profile)

        if self.start_date is None:
            return s
        return s + u', rozpoczęty w: %s' % self.start_date.year

    def __lt__(self, other):
        return self.start_date < other.start_date

    def __gt__(self, other):
        return self.start_date > other.start_date

    def save(self, *args, **kwargs):
        self.is_first = self.get_prev() is None
        self.is_last = self.get_next() is None
        
        if self.semesters:
            self.end_date = self.date(self.start_date, self.semesters-1, begin=False)
        elif self.years:
            self.end_date = self.date(self.start_date, self.years*2-1, begin=False)
        
        super(Course, self).save(*args, **kwargs)

    def get_leading_discipline(self):
        return self.coursetoleadingdiscipline_set.first()

    def get_start_date(self):
        return self.date(self.start_date, begin=True)

    def get_end_date(self):
        return self.date(self.end_date, begin=False)

    def reform_2019(self):
        """
        Returns True if the course should be displayed and processed in accordance
        to changes introduced in education system reform from 2019, otherwise returns
        False.
        """
        return True if self.start_date.year >= 2019 else False

    def get_prev(self):
        if not self.start_date:
            return None
        courses = self.get_courses().exclude(
            id__exact=self.id
        ).filter(start_date__lt=self.start_date).order_by('-start_date')
        return courses[0] if len(courses) > 0 else None

    def get_next(self):
        if not self.start_date:
            return None
        courses = self.get_courses().exclude(
            id__exact=self.id
        ).filter(start_date__gt=self.start_date).order_by('start_date')
        return courses[0] if len(courses) > 0 else None

    def is_course_first(self):
        return self.is_first

    def is_course_last(self):
        return self.is_last

    def get_courses(self):
        lang = getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE)
        f = {'name_%s' % lang: getattr(self, 'name_%s' % lang, '')}
        return Course.objects.active().filter(**f).filter(
            semesters__exact=self.semesters,
            years__exact=self.years,
            level__exact=self.level,
            type__exact=self.type,
            profile__exact=self.profile,
            department__exact=self.department
        )
        
    def get_current_semesters(self):
        semester = self.get_current_semester()
        if not semester:
            return []
        if semester % 2 == 0:
            return [semester - 1, semester]
        else:
            return [semester, semester + 1]
    
    def get_current_semester(self):
        """
        Returns current semester of this course.
        """
        if not self.didactic_offer or not self.didactic_offer.is_active:
            return None
        diff = self.diff(self.didactic_offer.start_date, self.start_date)
        if diff is None:
            return None
        return diff+1
    
    def get_current_year(self):
        semester = self.get_current_semester()
        if not semester:
            return None
        return int(math.ceil(semester / 2.0))
    
    def is_in_active_offer(self):
        """
        Returns True if course is in active didactic offer.
        """
        return self.didactic_offer and self.didactic_offer.is_active
    
    # Metody sprawdzające poziom nauczania
    def is_level_ba(self):
        return True if self.level.id == LEVEL_BA else False
    
    def is_level_msc(self):
        return True if self.level.id == LEVEL_MSC else False
    
    def is_level_phd(self):
        return True if self.level.id == LEVEL_PHD else False
    
    def is_level_u_msc(self):
        return True if self.level.id == LEVEL_U_MSC else False
    
    def is_level_eng(self):
        return True if self.level.id == LEVEL_ENG else False
    
    def is_level_pg_q(self):
        return True if self.level.id == LEVEL_PG_Q else False
    
    def is_level_pg_fl(self):
        return True if self.level.id == LEVEL_PG_FL else False

    def get_name_with_current_year(self):
        return u"%s, %s, %s, %s, rocznik: %s (rok studiów: %s)" % (
            self.name, self.level, self.type, self.profile, self.start_date.year,
            self.get_current_year())


class CourseToLeadingDiscipline(models.Model):
    class Meta:
        verbose_name = "Kierunek - Dyscyplina wiodąca"
        verbose_name_plural = "Kierunki - Dyscypliny wiodące"

    implementation = models.IntegerField(verbose_name="Realizacja [%]")
    course = models.ForeignKey(
        to='Course',
        verbose_name='Kierunek',
        on_delete=models.CASCADE)
    leading_discipline = models.ForeignKey(
        to='trinity.LeadingDiscipline',
        verbose_name='Dyscyplina wiodąca',
        on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}%'.format(self.leading_discipline.name, self.implementation)

    def __repr__(self):
        return '%s - %s' % (str(self.course), str(self.leading_discipline))


# -------------------------------------------------------
# --- SGROUP TYPE
# -------------------------------------------------------

class SGroupType(AbstractUniqueName):
    class Meta:
        verbose_name = _(u'Type of subjects group')
        verbose_name_plural = _(u'Types of subjects group')


# -------------------------------------------------------
# --- SGROUP
# -------------------------------------------------------

class SGroup(AbstractDidacticOffer):
    class Meta:
        ordering = ('-is_active', '-type', 'name',)
        verbose_name = _(u'Subjects group')
        verbose_name_plural = _(u'Subjects groups')

    start_semester = models.IntegerField(default=1, verbose_name=_(u'First semester/year'))
    sgroup = models.ForeignKey(
        to='self',
        related_name='+',
        null=True,
        blank=True,
        verbose_name=_(u'Parent subjects group'),
        on_delete=models.SET_NULL)
    course = models.ForeignKey(
        to='Course',
        verbose_name=_(u'Course'),
        related_name='sgroups',
        on_delete=models.CASCADE)
    type = models.ForeignKey(
        to='SGroupType',
        verbose_name=_(u'Type'),
        on_delete=models.CASCADE)

    objects = SGroupManager

    def __str__(self):
        from apps.merovingian.functions import default_sgroup_name
        if self.name == default_sgroup_name():
            return str(self.course)
        else:
            return '%s - %s' % (str(self.course), str(self.name))

    def save(self, *args, **kwargs):
        from apps.merovingian.functions import default_sgroup_name
        try:
            dsg_name = default_sgroup_name()
            if self.type.name != dsg_name:
                self.sgroup = SGroup.objects.get(
                    course=self.course,
                    type=SGroupType.objects.get(name=dsg_name)
                )
        except:
            pass
        finally:
            super(SGroup, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for m in self.modules.all():
            m.delete()
        super(SGroup, self).delete(*args, **kwargs)

    def get_start_date(self):
        if self.course.semesters:
            return self.date(self.course.start_date, self.start_semester - 1, begin=True)
        elif self.course.years:
            return self.date(self.course.start_date, (self.start_semester - 1)*2, begin=True)
        else:
            return None

    def get_end_date(self):
        return self.course.get_end_date()

    def get_prev(self):
        try:
            return self.course.get_prev().sgroups.get(
                name__iexact=self.name,
                start_semester__exact=self.start_semester,
                type__exact=self.type
            )
        except:
            return None

    def get_next(self):
        try:
            return self.course.get_next().sgroups.get(
                name__iexact=self.name,
                start_semester__exact=self.start_semester,
                type__exact=self.type
            )
        except:
            return None

    def is_course_first(self):
        return self.course.is_course_first()

    def is_course_last(self):
        return self.course.is_course_last()

    def is_default(self):
        return self.name == default_sgroup_name()


# -------------------------------------------------------
# --- MODULE TYPE
# -------------------------------------------------------

class ModuleType(AbstractUniqueName):
    class Meta:
        ordering = ('name',)
        verbose_name = _(u'Module type')
        verbose_name_plural = _(u'Module types')


# -------------------------------------------------------
# --- MODULE
# -------------------------------------------------------

class Module(AbstractDidacticOffer):
    class Meta:
        verbose_name = _(u'Module')
        verbose_name_plural = _(u'Modules')
        ordering = ('name', )

    ects = models.FloatField(null=True, blank=True, verbose_name=_(u'ECTS points'))
    type = models.ForeignKey(
        to='ModuleType',
        null=True,
        blank=True,
        verbose_name=_(u'Type'),
        on_delete=models.CASCADE)
    internal_code = models.CharField(max_length=128, blank=True)
    erasmus_code = models.CharField(max_length=128, blank=True)
    isced_code = models.CharField(max_length=128, blank=True)
    coordinator = models.ForeignKey(
        to='trainman.Teacher',
        verbose_name=_(u'Teacher'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    sgroup = models.ForeignKey(
        to='SGroup',
        related_name='modules',
        on_delete=models.CASCADE)

    objects = ModuleManager

    def get_start_date(self):
        if not self.pk:
            return None

        course = self.sgroup.course
        if course.semesters:
            semesters = self.get_semesters()
            semesters.append(course.semesters)
            return (self.date(course.start_date, min(semesters) - 1, begin=True)
                if self.id is not None
                else None)
        elif course.years: # years
            years = self.get_semesters()
            years.append(course.years)
            return (self.date(course.start_date, (min(years) - 1)*2, begin=True)
                if self.id is not None
                else None)
        else:
            return None

    def get_end_date(self):
        if not self.pk:
            return None

        course = self.sgroup.course

        if course.semesters:
            semesters = self.get_semesters()
            if len(semesters) > 0:
                semester = max(semesters)
            else:
                semester = 0
            return (self.date(course.start_date, min([semester, course.semesters])-1, begin=False)
                if self.id is not None
                else None)
        elif course.years:  # years
            years = self.get_semesters()
            if len(years) > 0:
                year = max(years)
            else:
                year = 0
            return (self.date(course.start_date, min([year, course.years])*2-1, begin=False)
                if self.id is not None
                else None)
        else:
            return None

    def get_prev(self):
        try:
            return self.sgroup.get_prev().modules.get(
                name__iexact=self.name,
                ects__exact=self.ects,
                type__exact=self.type
            )
        except:
            return None

    def get_next(self):
        try:
            return self.sgroup.get_next().modules.get(
                name__iexact=self.name,
                ects__exact=self.ects,
                type__exact=self.type
            )
        except:
            return None
    
    def is_annual(self):
        return True if self.sgroup.course.years else False

    def is_course_first(self):
        try:
            return self.sgroup.is_course_first()
        except:
            return False

    def is_course_last(self):
        try:
            return self.sgroup.is_course_last()
        except:
            return False

    def get_course(self):
        return self.sgroup.course

    def get_department(self):
        return self.sgroup.course.department

    def get_teachers(self):
        from apps.trainman.models import Teacher
        return Teacher.objects.filter(
            subject__in=Subject.objects.filter(
                module__exact=self)
        ).distinct()

    def get_lecture_teachers(self):
        from apps.merovingian.functions import lecture_name
        from apps.trainman.models import Teacher
        return Teacher.objects.filter(
            subject__in=Subject.objects.filter(
                module__exact=self,
                type__name__exact=lecture_name()
            )
        ).distinct()

    def get_semesters(self):
        """Returns semesters/years list of its subjects."""
        return [s.semester for s in Subject.objects.filter(module__exact=self)]

    def subjects_have_defined_ects(self):
        from django.db.models import Q
        s_all = Subject.objects.filter(module__exact=self).count()
        s_ects = Subject.objects.filter(module__exact=self).exclude(
            Q(ects__exact=0) | Q(ects__exact=None)).count()
        return True if s_all == s_ects else False

    def get_related_slos(self):
        slos = set()
        for subject in self.subjects.all():
            for slo in subject.slos.all():
                slos.add(slo)
        return slos

    def get_hours(self):
        return sum([s.hours for s in Subject.objects.filter(module__exact=self)])

    def get_hours_individual(self):
        return sum([s.hours_individual for s in Subject.objects.filter(module__exact=self)])

    def get_ects_classes(self):
        return sum([s.ects_classes for s in Subject.objects.filter(module__exact=self)])

    def get_ects_individual(self):
        return sum([s.ects_individual for s in Subject.objects.filter(module__exact=self)])

# -------------------------------------------------------
# --- MODULE PROPERTIES
# -------------------------------------------------------

class ModuleProperties(models.Model):
    class Meta:
        unique_together = ('semester', 'module', 'type')
        ordering = ('semester',)
        verbose_name = _(u'Module attributes')
        verbose_name_plural = _(u'Module attributes')

    semester = models.IntegerField(
        validators=[MinValueValidator(semester_minimal), MaxValueValidator(semester_maximal)],
        verbose_name=_(u'Semester/Year'),
    )
    hours = models.FloatField(verbose_name=_(u'Number of hours'))
    ects = models.FloatField(verbose_name=_(u'ECTS points'))
    type = models.ForeignKey(
        to='SubjectType',
        verbose_name=_(u'Type of classes'),
        on_delete=models.CASCADE)
    module = models.ForeignKey(
        to='Module',
        verbose_name=_(u'Module'),
        on_delete=models.CASCADE)

    def __str__(self):
        return '%s, %s' % (str(self.module), self.semester)


# -------------------------------------------------------
# --- SUBJECT TYPE
# -------------------------------------------------------

class SubjectType(AbstractUniqueName):
    class Meta:
        ordering = ('name',)
        verbose_name = _(u'Type of classes')
        verbose_name_plural = _(u'Types of classes')

    def short_name(self):
        return {
            9: u'WY',
            10: u'LB',
            11: u'KW',
            12: u'ĆW',
            13: u'SM',
            14: u'PR',
            15: u'CT',
            16: u'LT',
            17: u'KS'
        }[self.id]

    def is_practice(self):
        return self.id == 14


# -------------------------------------------------------
# --- SUBJECT ASSESSMENT
# -------------------------------------------------------

class SubjectAssessment(AbstractUniqueName):
    class Meta:
        ordering = ('name',)
        verbose_name = _(u'Type of pass')
        verbose_name_plural = _(u'Types of pass')


# -------------------------------------------------------
# --- SUBJECT DIFFICULTY
# -------------------------------------------------------

class SubjectDifficulty(models.Model):
    class Meta:
        verbose_name = _(u'Class level')
        verbose_name_plural = _(u'Class levels')
        ordering = ['order', 'name']

    name = models.CharField(max_length=128)
    order = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)


# -------------------------------------------------------
# --- SUBJECT
# -------------------------------------------------------

class Subject(AbstractDidacticOffer):
    class Meta:
        ordering = ('semester', 'name', '-type', 'assessment')
        verbose_name = _(u'Subject')
        verbose_name_plural = _(u'Subjects')

    hours = models.FloatField(verbose_name=_(u'Number of hours'))
    hours_individual = models.FloatField(
        default=0,
        verbose_name='Liczba godzin praca samodzielna')
    semester = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name=_(u'Semester/Year'))
    ects = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_(u'ECTS points'))
    ects_classes = models.FloatField(
        default=0,
        verbose_name='ECTS zajęcia')
    ects_individual = models.FloatField(
        default=0,
        verbose_name='ECTS praca samodzielna')
    type = models.ForeignKey(
        to='SubjectType',
        verbose_name=_(u'Type of classes'),
        on_delete=models.CASCADE)
    assessment = models.ForeignKey(
        to='SubjectAssessment',
        verbose_name=_(u'Type of pass'),
        on_delete=models.CASCADE)
    difficulty = models.ForeignKey(
        to='SubjectDifficulty',
        null=True,
        blank=True,
        verbose_name=_(u'Class level'),
        on_delete=models.CASCADE)
    module = models.ForeignKey(
        to='Module',
        verbose_name=_(u'Module'),
        related_name='subjects',
        on_delete=models.CASCADE)
    teachers = models.ManyToManyField(
        to='trainman.Teacher',
        through='SubjectToTeacher',
        blank=True,
        verbose_name=_(u'Teachers'))
    internal_code = models.CharField(max_length=128, blank=True)

    slos = models.ManyToManyField(
        to='trinity.ModuleLearningOutcome',
        through='trinity.SubjectToModuleLearningOutcome',
        blank=True,
        verbose_name='Przedmiotowe efekty uczenia się')

    objects = SubjectManager

    def __str__(self):
        return '%s, %sh, %s' % (self.name, self.hours, self.type)
    
    def is_annual(self):
        return True if self.module.get_course().years else False

    def get_start_date(self):
        if not self.module or not self.module.sgroup:
            return None
        course = self.module.sgroup.course
        if course.semesters:
            return self.date(course.start_date, min(self.semester, course.semesters) - 1, begin=True)
        elif course.years:  # years
            return self.date(course.start_date, (min(self.semester, course.years)-1)*2, begin=True)
        else:
            return None

    def get_end_date(self):
        if not self.module or not self.module.sgroup:
            return None
        course = self.module.sgroup.course
        if course.semesters:
            return self.date(course.start_date, min(self.semester, course.semesters) - 1, begin=False)
        elif course.years:  # years
            return self.date(course.start_date, min(self.semester, course.years)*2-1, begin=False)
        else:
            return None

    def get_prev(self):
        try:
            return self.module.get_prev().subjects.get(
                name__iexact=self.name,
                hours__exact=self.hours,
                semester__exact=self.semester,
                ects__exact=self.ects,
                type__exact=self.type,
                assessment__exact=self.assessment
            )
        except:
            return None                              

    def get_next(self):
        try:
            return self.module.get_next().subjects.get(
                name__exact=self.name,
                hours__exact=self.hours,
                semester__exact=self.semester,
                ects__exact=self.ects,
                type__exact=self.type,
                assessment__exact=self.assessment
            )
        except:
            return None

    def is_course_first(self):
        return self.module.is_course_first()

    def is_course_last(self):
        return self.module.is_course_last()

    def get_year_semester(self):
        if not self.module or not self.module.sgroup:
            return None, None
        course = self.module.sgroup.course
        
        if course.semesters:
            return int(self.semester / 2.0 + 0.5), int((self.semester + 1) % 2 + 1)
        else:
            return self.semester, None

    def get_roman_year_semester(self):
        if self.is_annual():
            return '{0}/-'.format(self.semester)
        return '{0}/{1}'.format(to_roman(self.get_year_semester()[0]), self.semester)


# -------------------------------------------------------
# --- SUBJECT TO TEACHER
# -------------------------------------------------------

class SubjectToTeacher(models.Model):
    class Meta:
        verbose_name = _(u'Subject - Teacher')
        verbose_name_plural = _(u'Subjects - Teachers')
        
    groups = models.IntegerField(verbose_name=_(u'Number of groups'))
    hours = models.FloatField(max_length=3, verbose_name=_(u'Number of hours'))
    description = models.CharField(
        max_length=512, null=True, blank=True, verbose_name=_(u'Description'))
    teacher = models.ForeignKey(
        to='trainman.Teacher',
        verbose_name=_(u'Teacher'),
        on_delete=models.CASCADE)
    subject = models.ForeignKey(
        to='Subject',
        verbose_name=_(u'Subject'),
        on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (str(self.subject), str(self.teacher))


# -------------------------------------------------------
# --- SIGNALS
# -------------------------------------------------------

def set_didactic_offer(sender, **kwargs):
    """
    Signal sets the didactic offer for the sender depending on the start and end date.
    
    Tries to find the didactic offer for instance. 
    Algorithm:
        Get all didactic offers from newest to latest
        For each of them:
            Check if the period of instance overlaps the period of this didactif offer
            If yes:
                Set this didactic offer as instance's offer
            If active offer was checked:
                Do not set and omit other didactic offers
    """
    if kwargs.get('raw', True):
        return
    
    if 'instance' not in kwargs:
        return
    instance = kwargs.get('instance')
    if not instance:
        return
    
    instance.didactic_offer = None
    object_start_date = instance.get_start_date()
    object_end_date = instance.get_end_date()

    if object_start_date is None or object_end_date is None:
        return

    doffers = DidacticOffer.objects.order_by('-start_date')
    for doffer in doffers:
        doffer_start_date, doffer_end_date = doffer.start_date, doffer.end_date
        if object_start_date > doffer_end_date:
            break
    
        if object_start_date <= doffer_end_date and object_end_date >= doffer_start_date:
            instance.didactic_offer = doffer
            if doffer.is_active:
                break

models.signals.pre_save.connect(set_didactic_offer, sender=Course)
models.signals.pre_save.connect(set_didactic_offer, sender=SGroup)
models.signals.pre_save.connect(set_didactic_offer, sender=Module)
models.signals.pre_save.connect(set_didactic_offer, sender=Subject)


def set_default_sgroup(sender, **kwargs):
    """
    Signal adds default specialty that exists in every course. 
    It's name is configurable.
    """
    if not kwargs.get('created', True) or kwargs.get('raw', False):
        return
    from apps.merovingian.functions import default_sgroup_settings
    dsg_settings = default_sgroup_settings()
    
    kwargs_names_exprs = {}
    kwargs_names = {}
    for lang_code, lang_name in settings.LANGUAGES:
        kwargs_names_exprs['name_'+lang_code+'__exact'] = getattr(dsg_settings, 'value_'+lang_code)
        kwargs_names['name_'+lang_code] = getattr(dsg_settings, 'value_'+lang_code)
    
    default_sgroup_type, created = SGroupType.objects.get_or_create(**kwargs_names_exprs)
    
    SGroup.objects.create(
        is_active=True,
        course=kwargs.get('instance', Course.objects.none()),
        type=default_sgroup_type, **kwargs_names
    )

models.signals.post_save.connect(set_default_sgroup, sender=Course)
