"""
Test file 

"""
## @file Test3.py
# @author weaves
# @brief Unittest
#
# @note
#
# Relatively complete test of IceFireA

import sys, logging, os
from unidecode import unidecode
from datetime import datetime, timezone, timedelta, date
from collections import Counter
import re
import itertools
from urllib.parse import urlparse

from blkswn import Configuration
from blkswn import IceFire
from blkswn import IceFireR
from blkswn import IceFireA

import unittest

logfile = os.environ['X_LOGFILE'] if os.environ.get('X_LOGFILE') is not None else "test.log"
logging.basicConfig(filename=logfile, level=logging.DEBUG)
logger = logging.getLogger('Test')
sh = logging.StreamHandler()
logger.addHandler(sh)

trs0 = os.path.join(os.path.dirname(__file__), "test.txt")


class Test3(unittest.TestCase):
    """
    A source directory dir0 is taken from the environment as SDIR or 
    is tests/media and should contain .m4a files.
    A file tests/p1.lst is also needed. It can list the files in the
    directory.
    """
    queue0 = None

    dir0 = os.getcwd()
    files0 = []
    files = []
    logger = None
    x0 = "empty"

    ## Sets pandas options and logging.
    @classmethod
    def setUpClass(cls):
        global logger
        cls.logger = logger
        Configuration.instance(file='blkswn.cfg')  # singleton

    ## Logs out.
    @classmethod
    def tearDownClass(cls):
        pass

    ## Null setup.
    def setUp(self):
        self.logger.info('setup')

    ## Null tear down
    def tearDown(self):
        self.logger.info('tearDown')

    ## Constructs
    def test_000(self):
        return
        chs = IceFireR(config = Configuration.instance().config,
                       type0='books',
                      logger=self.logger)

        ichs = iter(chs)

        v0 = next(chs)
        self.logger.info("dict: {type0} {cnt} {keys}"
                         .format(type0=type(v0), cnt=len(v0), keys=", ".join(v0.keys())))
        self.logger.info("dict: {url}".format(url=v0['url']))

        v0 = next(chs)
        self.logger.info("dict: {type0} {cnt} {keys}"
                         .format(type0=type(v0), cnt=len(v0), keys=", ".join(v0.keys())))
        self.logger.info("dict: {url}".format(url=v0['url']))


    def test_001(self):
        q0 = ['a','b','c']

        x = 'b'
        v0 = IceFireA.first_true(q0, default=x)
        self.logger.info("first_true: {0}".format(v0))
        self.assertTrue(v0 == q0[0])

        fpred = lambda x: x == 'b'

        x = '0'
        v0 = IceFireA.first_true(q0, default=x, pred=fpred)
        self.logger.info("first_true: {0}".format(v0))
        self.assertTrue(v0 == 'b')

        fpred = lambda x: x == 'x'

        v0 = IceFireA.first_true(q0, default=x, pred=fpred)
        self.logger.info("first_true: {0}".format(v0))
        self.assertTrue(v0 == x)

    def test_002(self):
        """
        Basic loading from file for testing.
        """
        books = IceFireA(type0="books", file="books.txt")
        self.assertIsNotNone(books)
        self.ar = books

    def test_004(self):
        """
        Counting
        """
        self.test_002()
        l0 = self.ar._src
        self.logger.info(type(l0))
        l1 = list(l0)
        self.logger.info("004: count: {cnt}".format(cnt=len(l1)) )

        pass

    def make0(self):
        ts = IceFire.types0
        ts = ", ".join(ts)
        self.logger.info("006: {ts}".format(ts=ts))

        self.srcs = ( ( "{x}".format(x=x), "{x}.txt".format(x=x) ) for x in IceFire.types0 )

        self.srcs = list(self.srcs)  
        self.logger.info(self.srcs)

        fctr = lambda x: IceFireA(type0=x[0], file=x[1])
        v0 = fctr(self.srcs[0])
        self.logger.info(type(v0))

        # check one
        self.srcs0 = ( fctr(x) for x in self.srcs )
        v0 = next(self.srcs0)
        self.logger.info(type(v0))

        # now all
        self.srcs0 = list( fctr(x) for x in self.srcs )

    def test_006(self):
        """
        Other checks
        """
        self.make0()
        srcs0 = ( list(x._src) for x in self.srcs0 )
        cnts = ( len(x) for x in srcs0 )

        self.logger.info(", ".join((str(x) for x in cnts)) )

    def test_008(self):
        self.make0()
        v0 = list((x._type0, x) for x in self.srcs0)
        self.logger.info(type(v0[0]))
        d0 = dict(v0)
        self.logger.info(d0.keys())

        ## Books from API
        b0 = list(d0['books']._src)
        self.logger.info("c). books from API: {0}".format(len(b0)))

    def test_010(self):
        d0 = IceFireA.make0()
        self.logger.info("factory: {0}".format(d0.keys()))

        h0 = d0['houses']._src # as an iterable
        walk, walk2 = itertools.tee(h0)

        # check it can work
        v0 = IceFireA.first_true(walk, default='null')
        self.logger.info(v0['url'])

        fpred = lambda x: x['name'].find("Breakstone") > -1
        v0 = IceFireA.first_true(walk2, default='null', pred=fpred)
        self.logger.info(v0['url'])

        self.logger.info("a). House Breakstone is at {0}".format(v0['url']))

        ## How many males, females and unknown genders are there in the first
        ## 40 characters? Note, index 0 does not correspond to a character, so
        ## full range is 1 - 40 both ends inclusive.

        c0 = d0['characters']._src # as an iterable
        walk, walk2 = itertools.tee(c0)

        c1 = itertools.take(40, c0)
        self.logger.info(type(c1))


        pass


#
# The sys.argv line will complain to you if you run it with ipython
# emacs. The ipython arguments are passed to unittest.main.

if __name__ == '__main__':
    if len(sys.argv) and "ipython" not in sys.argv[0]:
        # If this is not ipython, run as usual
        unittest.main(sys.argv)
    else:
        # If not remove the command-line arguments.
        sys.argv = [sys.argv[0]]
        unittest.main(module='Test', verbosity=3, failfast=True, exit=False)


