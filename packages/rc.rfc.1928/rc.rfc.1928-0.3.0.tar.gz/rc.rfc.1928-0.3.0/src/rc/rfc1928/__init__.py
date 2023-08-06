
__author__    = 'Andre Merzky <andre@merzky.net>'
__license__   = 'GNU AGPL.v3 *or* Commercial License'
__copyright__ = 'Copyright (C) 2019, RADICAL-Consulting UG'


# ------------------------------------------------------------------------------
#
from .rfc_1928 import RFC_1928, socksify


# ------------------------------------------------------------------------------
#
import os            as _os
import radical.utils as _ru

_mod_root = _os.path.dirname (__file__)

version_short, version_detail, version_base, \
               version_branch, sdist_name,   \
               sdist_path = _ru.get_version(_mod_root)
version = version_short


# ------------------------------------------------------------------------------

