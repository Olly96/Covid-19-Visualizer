import unittest
from unittest.mock import Mock
import sys
randMock = Mock()
turtleMock = Mock()
sys.modules['random'] = randMock
sys.modules['turtle'] = turtleMock
import src.person as person

class TestStringMethods(unittest.TestCase):
    def test_constructor(self):
        turtleMock.RawTurtle = Mock()
        canvas_obj = Mock()
        person_obj = person.Person(5, [100, 400], [100, 400], 7, canvas_obj)
        turtleMock.RawTurtle.assert_called_once_with(canvas_obj)