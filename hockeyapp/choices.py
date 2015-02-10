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

CONTRACT_TYPE = (
    ('', ''),
    (b'Двусторонний КХЛ/МХЛ', _('Two-sided KHL/MHL')),
    (b'Двусторонний КХЛ/ВХЛ', _('Two-sided KHL/VHL')),
    (b'Односторонний КХЛ', _('One-sided KHL')),
)

FIVER_VALUES = (
    DEFAULT_STATUS,
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
)

CHALLENGE_TYPE = (
    DEFAULT_STATUS,
    (1, _('Championship')),
    (2, _('Playoff')),
    (3, _('Hopeful cup')),
    (4, _('Junior World Cup')),
    (5, _('Challenge Cup')),
    (6, _('MHL playout')),
    (7, _('MHL qualifying tournament')),
    (8, _('MHL-2 Generation Cup'))
)