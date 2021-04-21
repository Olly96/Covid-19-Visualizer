import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
import sys
person_mock = unittest.mock.Mock()
sys.modules['src.person'] = person_mock
from src import location as loc

class TestStringMethods(unittest.TestCase):
        def test1(self):
            pop =  loc.spawn_people_random(3, [100, 200], [300, 400], 7, {})
            print(pop)
            person_mock.Person.assert_any_call(0, [100, 200], [300, 400], 7, {})
            person_mock.Person.assert_any_call(1, [100, 200], [300, 400], 7, {})
            person_mock.Person.assert_any_call(2, [100, 200], [300, 400], 7, {})

        def test2(self):
            pop = loc.spawn_people_communities(4, [[100, 200, 100, 200], [300, 400, 300, 400]], 7, {})
            print(pop)
            person_mock.Person.assert_any_call(0, [100, 200], [100, 200], 7, {})
            person_mock.Person.assert_any_call(1, [100, 200], [100, 200], 7, {})
            person_mock.Person.assert_any_call(2, [300, 400], [300, 400], 7, {})
            person_mock.Person.assert_any_call(3, [300, 400], [300, 400], 7, {})

if __name__ == '__main__':
    unittest.main()