# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError


def validate_white_space(value):
    if not str(value).strip():
        raise ValidationError('To pole jest wymagane.')
