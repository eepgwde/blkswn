## @file _Fetcher.py
# @brief URLs, headers and JSON
# @author weaves
#
# @details
# Singleton to fetch and split.
#
# @note
# 

import logging
import configparser
import socks
import socket
from urllib import request

import ast
import re

from functools import partial

from blkswn import Fetcher
from blkswn import Configuration

class IceFire(Fetcher):
  """
  URL fetch with more features.
  """
  _tions = None
  _hdrs = None
  _opener = None
  index0 = None

  def __init__(self, **kwargs):
    # invoking the __init__ of the parent class  
    super().__init__(**kwargs)

  def _refs0(self, l0):
    """
    Extract valid URLs from a string

    Separated by comma, then by semi-colon
    """
    l1 = l0.split(',')
    parts = []
    for x in l1:
      l2 = re.sub(r'[<>]', '', x)
      l3 = l2.strip().split(';')
      for y in l3:
        l4 = y.strip()
        self.logger.info(str(Configuration.instance().isvalid0(l4)) + "; " + l4)
        if Configuration.instance().isvalid0(l4):
          parts.append(l4)
    return parts

  def render(self, **kwargs):
    if 'index' in kwargs:
      return self._refs0(kwargs['index'])

    if 'list' in kwargs:
      r1 = kwargs['list']
      return ast.literal_eval(r1.decode())
    
  def index(self, **kwargs):
    r = self.fetch(**kwargs)
    hdrs = r.info()
    if not 'Link' in hdrs:
      raise ValueError('No \'Link\' header in response.')
    self.index0 = self.render(index=hdrs['Link'])
    return self.render(list=r.read())

