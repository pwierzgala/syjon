from django.db import models
from django.db.models import F, Min, Prefetch, Q

from apps.metacortex.settings import MODULE_TYPE_GENERAL_ID

# -------------------------------------------------------
# --- MIXINS
# -------------------------------------------------------

class VisibleMixin:
    def visible(self):
        return self.filter(is_visible=True)


class ActiveMixin(object):
    def active(self):
        return self.filter(is_active=True)


class PublishedMixin(object):
    def published(self):
        return self.filter(is_published=True)


# -------------------------------------------------------
# --- SYLLABUS MODULE
# -------------------------------------------------------

class SyllabusModuleQuerySet(ActiveMixin, PublishedMixin, models.QuerySet):

    def search(self):
        return self.select_related(
            'module__sgroup__course',
            'module__sgroup__course__department',
            'module__sgroup__course__profile',
            'module__sgroup__course__type',
            'module__sgroup__course__level',
            'coordinator__user_profile__user',
            'coordinator__degree',
        )

    def details(self):
        return self.active().published().select_related(
            'unit_source',
            'unit_target',
            'module__sgroup__course',
            'module__sgroup__course__department',
            'module__sgroup__course__profile',
            'module__sgroup__course__type',
            'module__sgroup__course__level',
            'coordinator__user_profile__user',
            'coordinator__degree',
        ).prefetch_related(
            'lecture_languages',
            'module__subjects',
            'module__mlos',
        )

    def list(self, coordinator, year, semester):
        """
        Returns queryset of syllabuses.
        :param coordinator: Teacher object.
        :param year: Starting year of a course.
        :param semester: Semester of a subject.
        :return: Queryset of syllabuses.
        """

        query = Q(coordinator=coordinator)

        years = range(year, 2011, -1)
        semesters = range(semester, 11, 2)

        dates_queries = Q()
        for year, semester in zip(years, semesters):
            date_query = Q(module__sgroup__course__start_date__year=year) & \
                         Q(module__subjects__semester=semester) & \
                         Q(module__subjects__semester=F('first_semester_of_module'))
            dates_queries |= date_query

        query &= dates_queries

        return self.active().annotate(
            first_semester_of_module=Min('module__subjects__semester')
        ).filter(
            query
        ).select_related(
            'module',
            'module__type',
            'module__sgroup',
            'module__sgroup__course',
            'module__sgroup__course__level',
            'module__sgroup__course__type',
            'module__sgroup__course__profile',
            'module__sgroup__course__department',
        ).order_by(
            '-module__sgroup__course__start_date'
        )


SyllabusModuleManager = SyllabusModuleQuerySet.as_manager()


# -------------------------------------------------------
# --- SYLLABUS SUBJECT
# -------------------------------------------------------

class SyllabusSubjectQuerySet(ActiveMixin, PublishedMixin, models.QuerySet):

    def general(self):
        return self.filter(subject__module__type__pk=MODULE_TYPE_GENERAL_ID)

    def search(self):
        return self.select_related(
            'subject__module__sgroup__course',
            'subject__module__sgroup__course__department',
            'subject__module__sgroup__course__profile',
            'subject__module__sgroup__course__type',
            'subject__module__sgroup__course__level',
            'subject__type',
            'teacher__user_profile__user',
            'teacher__degree',
        )

    def details(self, syllabus_id):
        from apps.metacortex.models import SyllabusToECTS
        return self.active().published().select_related(
            'subject__module__sgroup__course',
            'subject__module__sgroup__course__department',
            'subject__module__sgroup__course__profile',
            'subject__module__sgroup__course__type',
            'subject__module__sgroup__course__level',
            'subject__type',
            'subject__assessment',
            'teacher__user_profile__user',
            'teacher__degree',
        ).prefetch_related(
            Prefetch(
                'syllabus_to_ects',
                queryset=SyllabusToECTS.objects.filter(syllabus=syllabus_id).select_related('ects'),
                to_attr='equivalents'
            ),
            'assessment_forms',
            'didactic_methods',
            'module_learning_outcomes',
        )

    def list(self, teacher, year, semester):
        """
        Returns queryset of syllabuses.
        :param teacher: Teacher object.
        :param year: Starting year of a course.
        :param semester: Semester of a subject.
        :return: Queryset of syllabuses.
        """

        query = Q(teacher=teacher)

        years = range(year, 2011, -1)
        semesters = range(semester, 11, 2)

        dates_queries = Q()
        for year, semester in zip(years, semesters):
            date_query = Q(subject__module__sgroup__course__start_date__year=year) & \
                         Q(subject__semester=semester)
            dates_queries |= date_query

        query &= dates_queries

        return self.active().filter(
                query
            ).select_related(
                'subject',
                'subject__type',
                'subject__module',
                'subject__module__sgroup',
                'subject__module__sgroup__course'
            ).order_by(
                'subject__semester',
                'subject__name'
            ).distinct()


SyllabusSubjectManager = SyllabusSubjectQuerySet.as_manager()


# -------------------------------------------------------
# --- SYLLABUS PRACTICE
# -------------------------------------------------------

class SyllabusPracticeQuerySet(ActiveMixin, PublishedMixin, models.QuerySet):

    def search(self):
        return self.select_related(
            'subject__module__sgroup__course',
            'subject__module__sgroup__course__department',
            'subject__module__sgroup__course__profile',
            'subject__module__sgroup__course__type',
            'subject__module__sgroup__course__level',
            'subject__type',
            'teacher__user_profile__user',
            'teacher__degree',
        )

    def details(self):
        return self.active().published().select_related(
            'subject__module__sgroup__course',
            'subject__module__sgroup__course__department',
            'subject__module__sgroup__course__profile',
            'subject__module__sgroup__course__type',
            'subject__module__sgroup__course__level',
            'subject__type',
            'subject__assessment',
            'teacher__user_profile__user',
            'teacher__degree',
        )

    def list(self, teacher, year, semester):
        """
        Returns queryset of syllabuses.
        :param teacher: Teacher object.
        :param year: Starting year of a course.
        :param semester: Semester of a subject.
        :return: Queryset of syllabuses.
        """

        query = Q(teacher=teacher)

        years = range(year, 2011, -1)
        semesters = range(semester, 11, 2)

        dates_queries = Q()
        for year, semester in zip(years, semesters):
            date_query = Q(subject__module__sgroup__course__start_date__year=year) & \
                         Q(subject__semester=semester)
            dates_queries |= date_query

        query &= dates_queries

        return self.active().filter(
                query
            ).select_related(
                'subject',
                'subject__type',
                'subject__module',
                'subject__module__sgroup',
                'subject__module__sgroup__course'
            ).order_by(
                'subject__semester',
                'subject__name'
            ).distinct()


SyllabusPracticeManager = SyllabusPracticeQuerySet.as_manager()


# -------------------------------------------------------
# --- DIDACTIC METHOD
# -------------------------------------------------------

class DidacticMethodQuerySet(VisibleMixin, models.QuerySet):
    pass


DidacticMethodManager = DidacticMethodQuerySet.as_manager()
