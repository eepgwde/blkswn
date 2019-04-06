"""
Test file 

"""
## @file Test1.py
# @author weaves
# @brief Unittest
#
# @note
#
# Relatively complete test.

import sys, logging, os
from unidecode import unidecode
from datetime import datetime, timezone, timedelta, date
from collections import Counter
import re
from urllib.parse import urlparse

from blkswn import Configuration
from blkswn import IceFire

import unittest

logfile = os.environ['X_LOGFILE'] if os.environ.get('X_LOGFILE') is not None else "test.log"
logging.basicConfig(filename=logfile, level=logging.DEBUG)
logger = logging.getLogger('Test')
sh = logging.StreamHandler()
logger.addHandler(sh)

trs0 = os.path.join(os.path.dirname(__file__), "test.txt")


class Test1(unittest.TestCase):
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
        with open('hdrs.json') as f0:
            l0 = f0.read()
        self.logger.info(l0)

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

        self.logger.info(parts)

    def test_002(self):
        chs = IceFire(config = Configuration.instance().config, type0='characters')
        v0 = chs.mkUrl(page=1, pageSize=10)
        self.assertIsNotNone(v0)
        self.assertIsInstance(v0, str)
        self.assertTrue(len(v0) > 0)
        self.logger.info(v0)

    def test_004(self):
        chs = IceFire(config = Configuration.instance().config, type0='characters')
        v0 = chs.idx1
        self.assertIsNotNone(v0)
        self.assertIsInstance(v0, str)
        self.assertTrue(len(v0) > 0)
        self.logger.info(v0)

    def test_006(self):
        chs = IceFire(config = Configuration.instance().config, type0='characters')
        v0 = chs.index()
        self.logger.info(v0)
        self.logger.info(chs.index0)



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


