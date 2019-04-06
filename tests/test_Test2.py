"""
Test file 

"""
## @file Test2.py
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
from blkswn import IceFireR

import unittest

logfile = os.environ['X_LOGFILE'] if os.environ.get('X_LOGFILE') is not None else "test.log"
logging.basicConfig(filename=logfile, level=logging.DEBUG)
logger = logging.getLogger('Test')
sh = logging.StreamHandler()
logger.addHandler(sh)

trs0 = os.path.join(os.path.dirname(__file__), "test.txt")


class Test2(unittest.TestCase):
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
        chs = IceFireR(config = Configuration.instance().config,
                       type0='books',
                      logger=self.logger)

        ichs = iter(chs)
        v0 = next(chs)

        self.logger.info(type(v0))
        self.logger.info("dict: {cnt} {keys}".format(cnt=len(v0), keys=", ".join(v0.keys())))
        self.logger.info("dict: {url}".format(url=v0['url']))

        v0 = next(chs)

        self.logger.info(type(v0))
        self.logger.info("dict: {cnt} {keys}".format(cnt=len(v0), keys=", ".join(v0.keys())))
        self.logger.info("dict: {url}".format(url=v0['url']))


    def test_002(self):
        return
        chs = IceFireR(config = Configuration.instance().config,
                       type0='books',
                       logger=self.logger)

        ichs = iter(chs)
        houses = [ x for x in ichs ]

        self.assertIsNotNone(houses)
        self.assertTrue(len(houses) > 0)

        with open('books.txt', 'w') as f0:
            f0.write(str(houses))

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


