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
  _page = None

  def __init__(self, **kwargs):
    """
    Set the type0 if given as a keyword.

    Set idx1 for use with index.

    Pass others to the parent URL fetch class.
    """
    if 'type0' in kwargs:
      self.type0 = kwargs['type0']

    self._ftchr = iter(IceFire(**kwargs))

  def __iter__(self):
    return self

  def _page0(self):
    self._page = None
    v0 = next(self._ftchr)
    self._page = iter(list(v0)[0])

  # Python 3 compatibility
  def __next__(self):
    """
    Iterate through the page captured as a list
    """
    if self._page is None:
      self._page0()

    try:
      v0 = dict(next(self._page))     # end of local list
    except StopIteration:
      self._page0()             # this will throw a StopIteration if no more pages
      v0 = next(self._page)

    return v0

