from django.db import models

# -------------------------------------------------------
# --- MIXINS
# -------------------------------------------------------


class ActiveMixin(object):
    def active(self):
        return self.filter(is_active=True)


class DidacticOfferMixin(object):
    def didactic_offer(self):
        return self.filter(didactic_offer__is_active=True, is_active=True)


class DidacticOfferAndFutureMixin(object):
    def didactic_offer_and_future(self):
        from apps.merovingian.models import DidacticOffer
        offer = DidacticOffer.objects.get(is_active=True)
        return self.filter(didactic_offer__start_date__gte=offer.start_date, is_active=True)


class NewestMixin(object):
    def newest(self):
        return self.filter(is_last=True, is_active=True)


# -------------------------------------------------------
# --- COURSE
# -------------------------------------------------------

class CourseQuerySet(ActiveMixin, DidacticOfferMixin, DidacticOfferAndFutureMixin, NewestMixin, models.QuerySet):

    def future(self):
        from apps.merovingian.models import DidacticOffer
        offer = DidacticOffer.objects.get(is_active=True)
        return self.filter(didactic_offer__start_date__gt=offer.start_date, is_active=True)

    def active_between_dates(self, from_date, to_date):
        return self.active().filter(start_date__lte=to_date, end_date__gte=from_date)

CourseManager = CourseQuerySet.as_manager()


# -------------------------------------------------------
# --- SGROUP
# -------------------------------------------------------

class SGroupQuerySet(ActiveMixin, DidacticOfferMixin, DidacticOfferAndFutureMixin, NewestMixin, models.QuerySet):
    pass

SGroupManager = SGroupQuerySet.as_manager()


# -------------------------------------------------------
# --- MODULE
# -------------------------------------------------------

class ModuleQuerySet(ActiveMixin, DidacticOfferMixin, DidacticOfferAndFutureMixin, NewestMixin, models.QuerySet):

    def course(self, course):
        return self.filter(sgroup__course=course)

    def coordinator(self, coordinator):
        return self.filter(coordinator=coordinator)

    def course_start_year(self, year):
        return self.filter(sgroup__course__start_date__year=year)

ModuleManager = ModuleQuerySet.as_manager()


# -------------------------------------------------------
# --- SUBJECT
# -------------------------------------------------------

class SubjectQuerySet(ActiveMixin, DidacticOfferMixin, DidacticOfferAndFutureMixin, NewestMixin, models.QuerySet):
    pass

    def teacher(self, teacher):
        return self.filter(teachers=teacher)

    def course_start_year(self, year):
        return self.filter(module__sgroup__course__start_date__year=year)

SubjectManager = SubjectQuerySet.as_manager()
