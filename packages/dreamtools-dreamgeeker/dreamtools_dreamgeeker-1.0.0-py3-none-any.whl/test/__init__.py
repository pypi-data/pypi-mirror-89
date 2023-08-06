import unittest

from dreamtools import tools
from dreamtools.config import CConfig
from dreamtools.logmng import CTracker

CConfig('dreamtools')


class MyTestCase(unittest.TestCase):
    def testinit(self):
        print('Configuration')
        print(tools.string_me(55))
    def testlog(self):
        CTracker.info_tracking('test message info', 'je test')


if __name__ == '__main__':
    unittest.main()
