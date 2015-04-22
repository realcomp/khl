# -*- coding: utf-8 -*-
import re

from django.core.exceptions import ValidationError


def rgb_validator(value):
    if not re.match(r"(\d+),\s*(\d+),\s*(\d+)", value):
        raise ValidationError('Incorrect format. Expected `#,#,#`.')


def hex_validator(value):
    if not re.match(r'#[0-9a-fA-F]{6}', value):
        raise ValidationError('Incorrect format. Expected hex.')
