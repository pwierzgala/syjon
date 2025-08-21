# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.trainman.models import UserProfile


class SearchForm(forms.Form):
    query = forms.CharField(label = '', required=False)
    
    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop('queryset', None)
        super(SearchForm, self).__init__(*args, **kwargs)
        if self.queryset != None:
            self.fields['user'] = forms.ModelChoiceField(queryset = self.queryset, required = False, empty_label=_(u"Wszyscy"))
        else:
            self.fields['user'] = forms.ModelChoiceField(queryset = UserProfile.objects.none(), required = False)
    