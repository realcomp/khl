#coding: utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


DEFAULT_STATUS = (0, _('unknown'))

PLAYER_ROLE = (
    DEFAULT_STATUS,
    (1, _('Goalkeeper')),
    (2, _('Defender')),
    (3, _('Offender')),
)

MATCH_HISTORY_ACTIONS = (
    DEFAULT_STATUS,
    (1, _('Goals')),
    (2, _('Penalty')),
)

PARITY_VALUES = (
    DEFAULT_STATUS,
    (1, _('EV')),
    (2, _('POWER PLAYS')),
    (3, _('EVEN STRENGTH')),
    (4, _('BULLET')),
)