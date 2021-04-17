import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from unittest.mock import Mock
import sys
randMock = Mock()
helperMock = Mock()
sys.modules['random'] = randMock
import  src.helpers as helpers

class TestStringMethods(unittest.TestCase):
    def test_update_probability_sars(self):
        infected = Mock()
        infected.infection_probability