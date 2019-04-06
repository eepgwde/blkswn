"""
Test file 

"""
## @file Test4.py
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
from functools import partial
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


class Test4(unittest.TestCase):
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

    def test_008(self):
        d0 = IceFireA.make0()

        ## Books from API
        b0 = list(d0['books']._src)
        self.logger.info("c). books from API: {0}".format(len(b0)))

    def test_010(self):
        d0 = IceFireA.make0()

        h0 = d0['houses']._src # as an iterable
        walk, walk2 = itertools.tee(h0)

        # check it can work
        v0 = IceFireA.first_true(walk, default='null')

        fpred = lambda x: x['name'].find("Breakstone") > -1
        v0 = IceFireA.first_true(walk2, default='null', pred=fpred)

        self.logger.info("a). House Breakstone is at {0}".format(v0['url']))

        ## b). How many males, females and unknown genders are there in the first
        ## 40 characters? Note, index 0 does not correspond to a character, so
        ## full range is 1 - 40 both ends inclusive.

        c0 = d0['characters']._src # as an iterable

        c1 = itertools.islice(c0, 40)
        walk, walk2 = itertools.tee(c1)

        gndrs = list((x['gender'] for x in walk2))
        gtypes = set(gndrs)

        ## lambda functions don't work, try partials
        def snap0(x, tag=""):
            return x == tag

        tag0 = list(gtypes)[0]
        snap1 = partial(snap0, tag=tag0)
        v0 = snap1(gndrs[0])

        ## List of partials

        fpreds = ( partial(snap0, tag=x) for x in gtypes )
        fpreds = list(fpreds)

        cnts = list( ( sum(map(fx, gndrs)) for fx in fpreds ))
        self.logger.info("b). first 40 gender distribution {} ".format(list(zip(gtypes, cnts))))

        ## d) How many books does the character ‘High Septon’ appear in?
        ## (ignoring ‘povcharacters’)

        d0 = IceFireA.make0()
        c0 = d0['characters']._src # as an iterable

        walk, walk2 = itertools.tee(c0)

        fpred = lambda x: x['name'].find("High Septon") > -1
        ckey0 = IceFireA.first_true(walk, default={ 'url': 'null' }, pred=fpred)

        ## to match the url of a character in books.characters
        tag0 = ckey0['url']
        snap1 = partial(snap0, tag=tag0)

        b0 = d0['books']._src # as an iterable
        walk, walk2 = itertools.tee(b0)

        bc = dict(((x['name'], x['characters']) for x in walk2))

        x00 = list(bc.values())
        x1 = x00[0]
        
        v0 = ( IceFireA.first_true(x, default='', pred=snap1) for x in x00 )
        v0 = list(v0)

        ## if length is greater than 0 is the URL of ckey0
        def snap2(x):
            return int(len(x) > 0)

        # finally, apply snap2 and sum 
        nckey0 = sum(map(snap2, v0))

        self.logger.info("d). {0} books have character High Septon {1}"
                         .format(nckey0, ckey0['url']))

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


