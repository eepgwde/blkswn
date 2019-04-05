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

from functools import partial

from blkswn import Fetcher

class IceFire(Fetcher):
  """
  URL fetch with more features.
  """
  _tions = None
  _hdrs = None
  _opener = None

  def __init__(self, **kwargs):
    # invoking the __init__ of the parent class  
    super().__init__(**kwargs)

  def index(self, **kwargs):
    return self.fetch(**kwargs)

