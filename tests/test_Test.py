"""
Test file 

"""
## @file Test.py
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
import configparser
import json
import ast

import unittest

from blkswn import Stack
from blkswn import Fetcher, Configuration
from blkswn import IceFire

logfile = os.environ['X_LOGFILE'] if os.environ.get('X_LOGFILE') is not None else "test.log"
logging.basicConfig(filename=logfile, level=logging.DEBUG)
logger = logging.getLogger('Test')
sh = logging.StreamHandler()
logger.addHandler(sh)

trs0 = os.path.join(os.path.dirname(__file__), "test.txt")

class Test(unittest.TestCase):
    """
    A source directory dir0 is taken from the environment as SDIR or 
    is tests/media and should contain .m4a files.
    A file tests/p1.lst is also needed. It can list the files in the
    directory.
    """
    stack0 = None

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

        for root, dirs, files in os.walk(cls.dir0, topdown=True):
            for name in files:
                cls.files.append(os.path.join(root, name))

        cls.files.sort()
        cls.files0 = cls.files.copy()
        cls.logger.info('files: ' + unidecode('; '.join(cls.files)))
    
    ## Logs out.
    @classmethod
    def tearDownClass(cls):
        pass

    ## Null setup.
    def setUp(self):
        self.logger.info('setup')
        if not type(self).files:
            type(self).files = type(self).files0
            
        self.file0, *type(self).files = type(self).files

    ## Null tear down
    def tearDown(self):
        self.logger.info('tearDown')

    ## Constructs
    def test_000(self):
        self.stack0 = Stack()
        self.assertIsNotNone(self.stack0)

    ## Check empty responses
    ## Call prior
    def test_001(self):
        self.test_000()
        self.assertIsNotNone(self.stack0)
        self.logger.info('stack0: ' + str(self.stack0))
        self.assertTrue(self.stack0.is_empty())

    def test_002(self):
        self.test_001()
        x0 = "empty1"
        with self.assertRaises(IndexError):
            x0 = self.stack0.pop()
        self.logger.info('stack0: ' + x0)

    def test_003(self):
        self.test_001()
        x1 = "empty1"
        with self.assertRaises(IndexError):
            x1 = self.stack0.peek()
        self.logger.info('stack0: ' + x1)

    ### push one
    def test_004(self):
        self.test_001()
        x1 = self.stack0.push(self.x0)
        self.assertIsNone(x1)
        self.assertFalse(self.stack0.is_empty())

    ## check identity on pop
    def test_005(self):
        self.test_004()
        x1 = self.stack0.pop()
        self.assertIsNotNone(x1)
        self.logger.info('stack0: ' + x1)
        self.assertEqual(x1, self.x0)
        self.assertIs(x1, self.x0)

    ## check identity on peek
    def test_006(self):
        self.test_004()
        x1 = self.stack0.peek()
        self.assertIsNotNone(x1)
        self.logger.info('stack0: ' + x1)
        self.assertEqual(x1, self.x0)
        self.assertIs(x1, self.x0)

    ## Check with a load
    def test_007(self):
        self.test_001()
        sz0 = len(self.files)
        self.assertTrue(sz0 > 0)
        self.logger.info('stack0: pushing: sz0: ' + str(sz0))

        for name in self.files:
            self.stack0.push(name)

        self.assertTrue(self.stack0.size() > 0)
        self.assertEqual(sz0, self.stack0.size())

        while sz0 > 0:
            self.stack0.pop()
            sz0 -= 1

        self.assertTrue(self.stack0.is_empty())

    def test_009(self):
        config = Configuration.instance(file='blkswn.cfg').config

        v0 = config.sections()
        self.logger.info(str(v0))
        self.assertIsNotNone(v0)
        self.assertTrue(config['fetcher-proxy'])
        self.logger.info(config['fetcher-proxy']['host'])
        self.logger.info(config['fetcher-proxy']['port'])
        self.logger.info(config['fetcher-proxy']['type'])
        ftchr = Fetcher(logger=self.logger, config=config)
        # ftchr = Fetcher(logger=self.logger)
        self.assertIsNotNone(ftchr)
        self.logger.info(ftchr)

    def test_011(self):
        """
        This uses the singleton constructed above.
        """
        v0 = "http://www.bt.com/"

        ftchr = Fetcher(logger=self.logger, config=Configuration.instance().config)
        r = ftchr.fetch(url=v0)
        self.assertIsNotNone(r)

        v0 = "http://www.anapioficeandfire.com/api/characters/2105"
        ctr = 1;
        while ctr > 0:
            ctr -= 1
            r = ftchr.fetch(url=v0)
            self.assertIsNotNone(r)
            self.logger.info(str(r.info()))
            self.logger.info(r.read())

    def test_013(self):
        """
        This uses the singleton constructed above.
        """

        ftchr = Fetcher(logger=self.logger, config=Configuration.instance().config)
        v0 = "http://www.anapioficeandfire.com/api/characters"
        ctr = 1;
        while ctr > 0:
            ctr -= 1
            r = ftchr.fetch(url=v0)
            self.assertIsNotNone(r)
            self.logger.info(str(r.info()))
            self.logger.info(r.read())


    def test_015(self):
        """
        Houses use the Link response header to get the number of pages and the page size.
        """
        ftchr = Fetcher(logger=self.logger, config=Configuration.instance().config)
        idx0 = "https://www.anapioficeandfire.com/api/houses"

        r = ftchr.fetch(url=idx0)
        hdrs = r.info()
        r1 = r.read()

        self.assertTrue('Link' in hdrs)
        self.logger.info(hdrs['Link'])
        with open('houses.bytes', 'wb') as f0:
            f0.write(r1)

        with open('hdrs.json', 'w') as f0:
            f0.write(hdrs['Link'])

        x0 = ast.literal_eval(r1.decode())
        self.logger.info(type(x0))
        self.assertTrue(len(x0) > 0)
        self.logger.info(x0[-1])

    def test_017(self):
        """
        Houses use the Link response header to get the number of pages and the page size.
        """
        ftchr = IceFire(logger=self.logger, config=Configuration.instance().config)
        idx0 = "https://www.anapioficeandfire.com/api/houses"
        r = ftchr.index(url=idx0)
        r1 = r.read()
        x0 = ast.literal_eval(r1.decode())
        self.logger.info(x0[-1])


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


