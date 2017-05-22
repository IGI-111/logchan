import unittest

def suite():
    res = unittest.TestLoader().discover("unittests", pattern="*.py")
    if res != 0:
        return res
    return unittest.TestLoader().discover("seltests", pattern="*.py")
