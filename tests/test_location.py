import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
import sys
person_mock = unittest.mock.Mock()
sys.modules['src.person'] = person_mock
from src import location as loc

class TestStringMethods(unittest.TestCase):
        def test1(self):
            config = {
                "population_count": 3,
                "incubation_period": 7,
                "particle_size": 0.1,
                "vaccine_efficacy": 96
            }
            pop = loc.spawn_people_random(config, [100, 200], [300, 400], {})
            person_mock.Person.assert_any_call(0, [100, 200], [300, 400], 7,0.1, {})
            person_mock.Person.assert_any_call(1, [100, 200], [300, 400], 7, 0.1,{})
            person_mock.Person.assert_any_call(2, [100, 200], [300, 400], 7, 0.1,{})

        def test2(self):
            config = {
                "population_count": 4,
                "community_coordinates": [[100, 200, 100, 200], [300, 400, 300, 400]],
                "incubation_period":7,
                "particle_size": 0.1,
                "vaccine_efficacy": 96
            }
            pop = loc.spawn_people_communities(config, {})
            print(pop)
            person_mock.Person.assert_any_call(0, [100, 200], [100, 200], 7,0.1, {})
            person_mock.Person.assert_any_call(1, [100, 200], [100, 200], 7,0.1,{})
            person_mock.Person.assert_any_call(2, [300, 400], [300, 400], 7, 0.1,{})
            person_mock.Person.assert_any_call(3, [300, 400], [300, 400], 7, 0.1,{})

if __name__ == '__main__':
    unittest.main()