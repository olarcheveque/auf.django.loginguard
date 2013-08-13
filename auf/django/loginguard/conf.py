# -*- coding: utf-8 -*-

from django.conf import settings

LOGIN_GUARD_RETRY_POLICY_ON = getattr(
    settings,
    'LOGIN_GUARD_RETRY_POLICY_ON',
    False)

LOGIN_GUARD_RETRY_POLICY = (
    (60 * 10, 3),  # 3 times allowed in 10min
    (60 * 20, 4),  # 4 times allowed in 20min (+1 attempt wait 10 extra min)
    (60 * 40, 5),  # 5 times allowed in 40min
    (3600 * 24, 6),  # 6 times allowed per day
    )

LOGIN_GUARD_FREQUENCY_ALERT_ON = getattr(
    settings,
    'LOGIN_GUARD_FREQUENCY_ALERT_ON',
    False)

LOGIN_GUARD_FREQUENCY_ALERT = (
    (3600 * 24 * 3, 10),  # alert if 10 attempts for same user within 3 days
    )
