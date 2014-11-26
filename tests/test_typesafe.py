from dynct.util.typesafe._decorator import typesafe

__author__ = 'justusadam'

import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):

        @typesafe
        def a(c:str='', b:str='') -> str:
            return ''

        a(b='')



if __name__ == '__main__':
    unittest.main()