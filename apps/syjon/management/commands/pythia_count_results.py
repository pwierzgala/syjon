# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

import syjon
from apps.merovingian.models import Course, Subject
from apps.pythia.models import (QUESTION_TYPE_CLOSEDEND_EVALUATION, Poll,
                                Question, ResultCourse, ResultTeacher,
                                ResultTeacherSubjectCourse, TokenAnswer)
from apps.trainman.models import Teacher


class Command(BaseCommand):

    args = u'<id_poll>'

    def result_table(self, poll_id, results):
        questions = Question.objects.filter(
            poll_id__exact=poll_id,
            type_id__exact=QUESTION_TYPE_CLOSEDEND_EVALUATION
        ).order_by('sequence')

        mark = 0.0
        weight = 0.0
        votes = 0
        for question in questions:
            answers = results.filter(question_id__exact=question.id)

            for answer in answers:
                mark += float(answer.answer.mark) * float(answer.answer.weight) * float(answer.question.weight)
                weight += float(answer.answer.weight) * float(answer.question.weight)
                votes += 1
        if weight != 0:
            mark /= weight
        endresults = (votes/len(questions), mark)
        return endresults

    def handle(self, *args, **options):
        translation.activate(getattr(settings, 'LANGUAGE_CODE', syjon.settings.LANGUAGE_CODE))

        id_poll = args[0]
        poll = Poll.objects.filter(id__exact=id_poll)[0]

        teachers = Teacher.objects.all()

        ResultTeacher.objects.filter(poll__exact=poll).delete()
        ResultTeacherSubjectCourse.objects.filter(poll__exact=poll).delete()

        for teacher in teachers:
            print(teacher)
            answers = TokenAnswer.objects.filter(teacher_id__exact=teacher.id)
            results = self.result_table(id_poll, answers);

            rt = ResultTeacher()
            rt.teacher = teacher
            rt.mark = results[1]
            rt.votes = results[0]
            rt.poll = poll
            rt.save()

            subjects_from_merv = Subject.objects.active().filter(
                semester__in=poll.token_set.values('semester').distinct(),
                teachers__in=[teacher]
            )
            subjects_from_pyth = Subject.objects.active().filter(
                id__in=TokenAnswer.objects.filter(
                    token__poll__id=poll.id,
                    teacher__in=[teacher]
                ).values('subject').distinct()
            )

            subjects = set(subjects_from_merv) | set(subjects_from_pyth)

            for subject in subjects:
                if subject.module.sgroup is None:
                    continue
                course = subject.module.sgroup.course
                if course.start_date.year+int((subject.semester-1)*.5) != poll.start_date.year-1:
                    continue

                #print('%s%s' % (('\t'+subject.name).ljust(50), ('\t'+str(course))))
                #print(type(subject))
                courses = Course.objects.filter(sgroups__modules__subjects=subject)
                if len(courses) > 0:
                    course = courses[0]
                else:
                    continue

                answers = TokenAnswer.objects.filter(teacher_id__exact=teacher.id, subject_id__exact=subject.id)
                results = self.result_table(id_poll, answers)

                rtsm = ResultTeacherSubjectCourse()
                rtsm.teacher = teacher
                rtsm.subject = subject
                rtsm.course = course
                rtsm.mark = results[1]
                rtsm.votes = results[0]
                rtsm.poll = poll
                rtsm.save()

        ResultCourse.objects.filter(poll__exact=poll).delete()
