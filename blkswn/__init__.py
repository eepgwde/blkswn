# -*- coding: utf-8 -*-

from blkswn._version import __version__
from blkswn._Stack import Stack
from blkswn._Queue import Queue
from blkswn._Fetcher import Fetcher
from blkswn._Fetcher import _Singleton as Configuration
from blkswn._IceFire import IceFire
from blkswn._IceFireR import IceFireR
from blkswn._IceFireA import IceFireA

from blkswn._Utility import _Utility as Utility

__copyright__ = 'Copyright 2019 Walter Eaves'
__license__ = 'GPLv3'
__title__ = 'blkswn'

# appease flake8: the imports are purposeful
(__version__, Stack, Queue)
