import unittest

def suite():
    return unittest.TestLoader().discover(".", pattern="*.py")

