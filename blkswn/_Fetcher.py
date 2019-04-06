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
from urllib.parse import urlparse

import ast
import re

from functools import partial

class Fetcher(object):
  """
  URL fetch with more features.
  """
  _tions = None
  _hdrs = None
  _opener = None

  def __init__(self, **kwargs):
    self.config = kwargs.get('config', configparser.ConfigParser())
    self.logger = kwargs.get('logger', logging.getLogger('Test'))
    if 'fetcher-proxy' in self.config.sections():
      d0 = self.config['fetcher-proxy']
      if d0['type'].startswith("socks5"):
        socks.set_default_proxy(socks.SOCKS5, d0['host'], int(d0['port']))
        socket.socket = socks.socksocket
      if 'hdrs' in d0:
        self._hdrs = ast.literal_eval(d0['hdrs'])
        self._opener = request.build_opener()
        self._opener.addheaders = self._hdrs
    pass

  def fetch(self, **kwargs):
    if self._opener is not None:
      request.install_opener(self._opener)
    return request.urlopen(kwargs['url'])

  def dispose(self):
    """
    The media info has to be re-created for every file.
    """
    pass


class _Singleton(object):
  """
  A configuration singleton
  """
  _impl = None
  config = None

  @classmethod
  def instance(cls, **kwargs):
    if cls._impl is None:
      cls._impl = _Singleton()
      cls.config = configparser.ConfigParser()
      if kwargs.get('file', None) is not None:
          cls.config.read(kwargs['file'])
      if kwargs.get('config', None) is not None:
          cls.config = config.read(kwargs['config'])

    return cls._impl

  def isvalid0(self, url):
    """
    Utility boolean test method to check is a string is a URI.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

    return True

  def qparts(self, purl):
    qs = [ x.split('=') for x in purl.split('&') ]
    return dict(qs)

