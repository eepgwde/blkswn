## @file _Utility.py
# @brief Analyzer for text files from IceFireR.py
# @author weaves
#
#

import logging
import configparser
import socks
import socket
from urllib import request

from functools import partial
from itertools import *

class _Utility(object):
  """
  A configuration singleton
  """
  _impl = None

  @classmethod
  def instance(cls, **kwargs):
    if cls._impl is None:
      cls._impl = _Utility()

      cls.config = configparser.ConfigParser()
      if kwargs.get('file', None) is not None:
          cls.config.read(kwargs['file'])
      if kwargs.get('config', None) is not None:
          cls.config = config.read(kwargs['config'])

    return cls._impl

#  def count0(self, s0):
    
