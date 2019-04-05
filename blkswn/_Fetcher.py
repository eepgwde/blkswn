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
    self.logger.info(self.config.sections())
    if 'fetcher-proxy' in self.config.sections():
      d0 = self.config['fetcher-proxy']
      if d0['type'].startswith("socks5"):
        socks.set_default_proxy(socks.SOCKS5, d0['host'], int(d0['port']))
        socket.socket = socks.socksocket
      if 'hdrs' in d0:
        self.logger.info(d0['hdrs'])
        self._hdrs = ast.literal_eval(d0['hdrs'])
        self.logger.info(self._hdrs)
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
  _impl = None

  @classmethod
  def instance(cls, **kwargs):
    if cls._impl is None:
      cls._impl = configparser.ConfigParser()
      if kwargs.get('file', None) is not None:
          cls._impl.read(kwargs['file'])
      if kwargs.get('config', None) is not None:
          cls._impl = config.read(kwargs['config'])

    return cls._impl

