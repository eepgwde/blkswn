## @file _IceFireR.py
# @brief Iterator that pages through the records in the pages
# @author weaves
#
# @details
# For a typical iterator interface this pages and records one record at a time.
#

import logging
import configparser
import socks
import socket
from urllib import request

from functools import partial

from blkswn import IceFire
from blkswn import Configuration

class IceFireR(object):

  _ftchr = None

  def __init__(self, **kwargs):
    """
    Set the type0 if given as a keyword.

    Set idx1 for use with index.

    Pass others to the parent URL fetch class.
    """
    if 'type0' in kwargs:
      self.type0 = kwargs['type0']

    self._ftchr = IceFire(**kwargs)

  def __iter__(self):
    return self

  # Python 3 compatibility
  def __next__(self):
    raise StopIteration()

