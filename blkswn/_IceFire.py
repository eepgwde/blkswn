## @file _IceFire.py
# @brief Iterator that pages through the server.
# @author weaves
#
# @details
# Each object is fixed to a URL base.
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

  These support an iterator interface that steps through pages and fetches pages of
  records.

  The record schema are handled in another class.

  @note
  I've not used the pointers in the header 'next', 'prev', 'first' or 'last'
  """
  index0 = None

  types0 = ( 'houses', 'characters', 'books')  # these are known to work
  type0 = 'houses'                             # the default used by the ctr.
  idx0 = "https://www.anapioficeandfire.com/api/{type0}"
  idx1 = None
  base0 = "https://www.anapioficeandfire.com/api/{type0}?page={page}&pageSize={pageSize}"

  cpage = None
  npage = None

  def mkUrl(self, page=1, pageSize=10):
    """
    Make an enquiry URL
    """
    return self.base0.format(type0=self.type0, page=page, pageSize=pageSize)

  def __init__(self, **kwargs):
    """
    Set the type0 if given as a keyword.

    Set idx1 for use with index.

    Pass others to the parent URL fetch class.
    """
    super().__init__(**kwargs)
    if 'type0' in kwargs:
      self.type0 = kwargs['type0']

    self.idx1 = self.idx0.format(type0=self.type0)

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

  def extract(self, **kwargs):
    """
    Utility method to extract information.

    'index' extracts URLs; 'list' returns a data payload; 'pages' gets max and min pages.
    """
    if 'index' in kwargs:
      return self._refs0(kwargs['index'])

    if 'list' in kwargs:
      r1 = kwargs['list']
      return ast.literal_eval(r1.decode())

    if 'pages' in kwargs:
      r1 = kwargs['pages']
      c0 = Configuration.instance().qparts
      f0 = lambda x: c0(x, fconv=int)['page']
      return [ f0(x) for x in r1 ]

    if 'pageSize' in kwargs:    # returns a set
      r1 = kwargs['pageSize']
      c0 = Configuration.instance().qparts
      f0 = lambda x: c0(x, fconv=int)['pageSize']
      return { f0(x) for x in r1 }

  def __iter__(self):
    return self

  # Python 3 compatibility
  def __next__(self):
    if self.npage is None:
      self.index()
    else:
      if self.npage >= max(self.pages):
        raise StopIteration()

    return self._page0(page=self.npage+1, pageSize=self.pageSize)

  def _page0(self, page=None, pageSize=None):
    """
    Step through the pages.

    @note
    I've not used the pointers in the header 'next', 'prev', 'first' or 'last'
    """
    yield self.cpage
    self.npage = page
    url0 = self.mkUrl(page=self.npage, pageSize=self.pageSize)
    r = self.fetch(url=url0)
    self.cpage = self.extract(list=r.read())

  def index(self, **kwargs):
    """
    Gets the first page and processes the Link header to get the page count and page size.
    """
    if not 'url' in kwargs:
      kwargs['url'] = self.idx1
    r = self.fetch(**kwargs)
    hdrs = r.info()
    if not 'Link' in hdrs:
      raise ValueError('No \'Link\' header in response.')
    self.index0 = self.extract(index=hdrs['Link'])
    self.pages = self.extract(pages=self.index0)
    self.pageSize = max(self.extract(pageSize=self.index0))
    self.cpage = self.extract(list=r.read())
    self.npage = min(self.pages)

