import unittest

def suite():
    res = unittest.TestLoader().discover("unitests", pattern="*.py")
    if res != 0:
        # Tests have failed no need to continue
        return res
    return unittest.TestLoader().discover("seltests", pattern="*.py")
