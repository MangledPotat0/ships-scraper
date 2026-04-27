# -*- coding: utf-8 -*-
"""
/app/sources.py
Web sources for polling data.
"""

from enum import StrEnum

class Source(StrEnum):
    VESSELFINDER = "https://www.vesselfinder.com/vessels/details/"
