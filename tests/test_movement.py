import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from unittest.mock import Mock
import sys
randMock = Mock()
helperMock = Mock()
sys.modules['random'] = randMock
sys.modules['helpers'] = helperMock
import  src.movement as movement


class TestStringMethods(unittest.TestCase):
    # Standard scenario to generate displacement coordinate within given range
    def test_get_displacement_coordinates_1(self):
        mov = movement.Movement()
        uniformMock = Mock()
        uniformMock.side_effect = [150, 200]
        randMock.uniform = uniformMock
        person_obj = unittest.mock.Mock()
        turtle_obj = unittest.mock.Mock()
        turtle_obj.xcor = MagicMock(return_value=150)
        turtle_obj.ycor = MagicMock(return_value=200)
        person_obj.turtle = turtle_obj
        print(person_obj.turtle.xcor())
        person_obj.x_limit = [100, 500]
        person_obj.y_limit = [100, 500]
        self.assertEqual(mov.get_displacement_coordinates(person_obj, 10), [150, 200])
        randMock.uniform.assert_any_call(145, 155)
        randMock.uniform.assert_any_call(195, 205)

    # Scenario where x_bound_2 and y_bound_1 are greater than x_limit and y_limit
    def test_get_displacement_coordinates_2(self):
            mov = movement.Movement()
            uniformMock = Mock()
            uniformMock.side_effect = [493.8, 106.5]
            randMock.uniform = uniformMock
            person_obj = unittest.mock.Mock()
            turtle_obj = unittest.mock.Mock()
            turtle_obj.xcor = MagicMock(return_value=499)
            turtle_obj.ycor = MagicMock(return_value=102)
            person_obj.turtle = turtle_obj
            print(person_obj.turtle.xcor())
            person_obj.x_limit = [100, 500]
            person_obj.y_limit = [100, 500]
            self.assertEqual(mov.get_displacement_coordinates(person_obj, 10), [493.8, 106.5])
            randMock.uniform.assert_any_call(494, 500)
            randMock.uniform.assert_any_call(100, 107)
            # Scenario where x_bound_2 and y_bound_1 are greater than x_limit and y_limit
    # Scenario where x_bound_1 and y_bound_2 are greater than x_limit and y_limit
    def test_get_displacement_coordinates_3(self):
        mov = movement.Movement()
        uniformMock = Mock()
        uniformMock.side_effect = [104.5, 495]
        randMock.uniform = uniformMock
        person_obj = Mock()
        turtle_obj = Mock()
        turtle_obj.xcor = MagicMock(return_value=102)
        turtle_obj.ycor = MagicMock(return_value=499)
        person_obj.turtle = turtle_obj
        print(person_obj.turtle.xcor())
        person_obj.x_limit = [100, 500]
        person_obj.y_limit = [100, 500]
        self.assertEqual(mov.get_displacement_coordinates(person_obj, 10), [104.5, 495])
        randMock.uniform.assert_any_call(100, 107)
        randMock.uniform.assert_any_call(494, 500)

    def test_random_movement(self):
        mov = movement.Movement()
        population = {}
        infected = {}
        recovered = {}
        config = {
            "infection_duration": 1440,
            "local_distance": 5,
            "long_distance": 30,
            "sd_factor": 0.6,
            "type": "SARS-COV-2",
            "infection_distance": 5,
            "mask_prob_infected_out_range": 0.2,
            "mask_prob_infected_in_range": 0.5,
            "mask_prob_susceptible": 0.5,
            "mask_prob_both_out_range": 0.02,
            "mask_prob_both_in_range": 0.25,
            "vaccine_probability": -1,
            "vaccine_efficacy_range": [0.64, 0.67, 0.94, 0.95],
            "mask_probability": -1,
            "time_conversion_factor": 24,
            "base_infection_probability": 0.6,
            "daily_prob_change": 0.9,
            "peak_infection_sars": 10,
            "daily_prob_increase_sars": 1.1,
            "daily_prob_decrease_sars": 0.9,
            "initial_infection_percentage": 2,
            "asymptomatic_probability": 0.3,
            "testing_probability": 0.5,
            "contact_tracing_efficiency": 1,
            "quarantine_location_x_limit": [-300, -260],
            "quarantine_location_y_limit": [-250, -210]
        }
        rand_mock = Mock()
        rand_mock.side_effect = [0.2, 0.3, 0.6, 0.1,  0.8]
        randMock.random = rand_mock
        get_displacement_mock = Mock()
        get_displacement_mock.side_effect = [[120, 300], [100.8, 200], [206.9, 405]]
        mov.get_displacement_coordinates = get_displacement_mock
        mov.update_infection_status = Mock()
        for i in range(3):
            person_obj = Mock()
            turtle_obj = Mock()
            turtle_obj.goto = Mock()
            person_obj.turtle = turtle_obj
            if i % 2 == 0:
                person_obj.displacement_prob = 0.8
            else:
                person_obj.displacement_prob = 0.1
            population[i] = person_obj
            mov.random_movement(person_obj, config)

        population[0].turtle.goto.assert_any_call(120, 300)
        population[1].turtle.goto.assert_not_called()
        population[2].turtle.goto.assert_any_call(100.8, 200)

        # self.assertEqual(population[0].)

    def test_simulate_random_movement(self):
        mov = movement.Movement()
        population = {}
        infected = {}
        recovered = {}
        config = {
        "infection_duration": 1440,
        "local_distance": 5,
        "long_distance": 30,
        "sd_factor": 0.6,
        "type": "SARS-COV-2",
        "infection_distance": 5,
        "mask_prob_infected_out_range": 0.2,
        "mask_prob_infected_in_range": 0.5,
        "mask_prob_susceptible": 0.5,
        "mask_prob_both_out_range": 0.02,
        "mask_prob_both_in_range": 0.25,
        "vaccine_probability": -1,
        "vaccine_efficacy_range": [0.64, 0.67, 0.94, 0.95],
        "mask_probability": -1,
        "time_conversion_factor": 24,
        "base_infection_probability": 0.6,
        "daily_prob_change": 0.9,
        "peak_infection_sars": 10,
        "daily_prob_increase_sars": 1.1,
        "daily_prob_decrease_sars": 0.9,
        "initial_infection_percentage": 2,
        "asymptomatic_probability": 0.3,
        "testing_probability": 0.5,
        "contact_tracing_efficiency": 1,
        "quarantine_location_x_limit": [-300, -260],
        "quarantine_location_y_limit": [-250, -210]
}
        for i in range(3):
            person_obj = Mock()
            turtle_obj = Mock()
            turtle_obj.goto = Mock()
            person_obj.turtle = turtle_obj
            if i % 2 == 0:
                person_obj.displacement_prob = 0.8
                person_obj.is_quarantined = False
            else:
                person_obj.displacement_prob = 0.1
                person_obj.is_quarantined = True
            population[i] = person_obj
        mov.update_infection_status = Mock()
        mov.random_movement = Mock()
        mov.simulate_random_movement(population, infected, recovered, config)
        self.assertEqual(mov.random_movement.call_count, 2)
        self.assertEqual(mov.update_infection_status.call_count, 3)

    def test_update_infections(self):
        mov = movement.Movement()
        person_obj = Mock()
        turtle_obj = Mock()
        turtle_obj.color = Mock()
        person_obj.turtle = turtle_obj
        person_obj.status = "I"
        person_obj.is_ever_infected = True
        person_obj.infected_time = 1445
        person_obj.id = 23
        infected = {23: True}
        recovered = {}
        config = {
            "infection_duration": 1440,
            "local_distance": 5,
            "long_distance": 30,
            "sd_factor": 0.6,
            "type": "SARS-COV-2",
            "infection_distance": 5,
            "mask_prob_infected_out_range": 0.2,
            "mask_prob_infected_in_range": 0.5,
            "mask_prob_susceptible": 0.5,
            "mask_prob_both_out_range": 0.02,
            "mask_prob_both_in_range": 0.25,
            "vaccine_probability": -1,
            "vaccine_efficacy_range": [0.64, 0.67, 0.94, 0.95],
            "mask_probability": -1,
            "time_conversion_factor": 24,
            "base_infection_probability": 0.6,
            "daily_prob_change": 0.9,
            "peak_infection_sars": 10,
            "daily_prob_increase_sars": 1.1,
            "daily_prob_decrease_sars": 0.9,
            "initial_infection_percentage": 2,
            "asymptomatic_probability": 0.3,
            "testing_probability": 0.5,
            "contact_tracing_efficiency": 1,
            "quarantine_location_x_limit": [-300, -260],
            "quarantine_location_y_limit": [-250, -210]
        }
        print("lol",infected,recovered)
        mov.update_infection_status(person_obj, infected, recovered, config)
        print("lol",infected,recovered)
        self.assertEqual(infected, {})
        self.assertEqual(recovered, {23: True})

        person_obj_2 = Mock()
        turtle_obj_2 = Mock()
        turtle_obj_2.color = Mock()
        person_obj_2.turtle = turtle_obj
        person_obj_2.status = "AI"
        person_obj_2.is_ever_infected = True
        person_obj_2.infected_time = 1442
        person_obj_2.id = 45
        infected = {45: True}
        recovered = {}
        mov.update_infection_status(person_obj_2, infected, recovered, config)
        self.assertEqual(infected, {})
        self.assertEqual(recovered, {45: True})

        person_obj_3 = Mock()
        turtle_obj_3 = Mock()
        turtle_obj_3.color = Mock()
        person_obj_3.turtle = turtle_obj
        person_obj_3.status = "AI"
        person_obj_3.is_ever_infected = True
        person_obj_3.infected_time = 700
        person_obj_3.id = 78
        person_obj_3.update_prob_tracker = 10
        infected = {45: True}
        recovered = {}
        helperMock.update_probability_covid = Mock()
        mov.update_infection_status(person_obj_3, infected, recovered, config)
        # helperMock.update_probability_covid.assert_called_once()
        print(infected, recovered, person_obj_3)

    def test_simulate_movement_communities(self):
        mov = movement.Movement()
        population = {}
        infected = {}
        recovered = {}
        config = {
            "infection_duration": 1440,
            "local_distance": 5,
            "long_distance": 30,
            "sd_factor": 0.6,
            "type": "SARS-COV-2",
            "infection_distance": 5,
            "mask_prob_infected_out_range": 0.2,
            "mask_prob_infected_in_range": 0.5,
            "mask_prob_susceptible": 0.5,
            "mask_prob_both_out_range": 0.02,
            "mask_prob_both_in_range": 0.25,
            "vaccine_probability": -1,
            "vaccine_efficacy_range": [0.64, 0.67, 0.94, 0.95],
            "mask_probability": -1,
            "time_conversion_factor": 24,
            "base_infection_probability": 0.6,
            "daily_prob_change": 0.9,
            "peak_infection_sars": 10,
            "daily_prob_increase_sars": 1.1,
            "daily_prob_decrease_sars": 0.9,
            "initial_infection_percentage": 2,
            "asymptomatic_probability": 0.3,
            "testing_probability": 0.5,
            "contact_tracing_efficiency": 1,
            "quarantine_location_x_limit": [-300, -260],
            "quarantine_location_y_limit": [-250, -210],
            "community_travel_probability": 0.02,
            "visit_hub_probability": 0.1,
            "community_coordinates": [[-280, -100, 120, 300], [-80, 100, 120, 300], [120, 300, 120, 300], [-280, -100, -80, 100], [-80, 100, -80, 100], [120, 300, -80, 100], [-280, -100, -280, -100], [-80, 100, -280, -100], [120, 300, -280, -100]]
        }
        person_obj_1 = Mock()
        person_obj_1.is_quarantined = False
        turtle_obj_1 = Mock()
        turtle_obj_1.goto = Mock()
        person_obj_1.turtle = turtle_obj_1
        person_obj_2 = Mock()
        person_obj_2.is_quarantined = False
        turtle_obj_2 = Mock()
        turtle_obj_2.goto = Mock()
        person_obj_2.turtle = turtle_obj_2
        population[0] = person_obj_1
        population[1] = person_obj_2
        random_mock = Mock()
        random_mock.side_effect = [0.01, 0.5]
        randMock.random = random_mock
        randMock.choice = Mock(return_value=[-80, 100, -80, 100])
        randint_mock = Mock()
        randint_mock.side_effect = [75, 90]
        randMock.randint = randint_mock
        mov.random_movement = Mock()
        mov.update_infection_status = Mock()
        mov.simulate_movement_communities(population, infected, recovered, config)
        randMock.randint.assert_any_call(-80, 100)
        turtle_obj_1.goto.assert_called_once_with(75, 90)
        self.assertEqual(mov.random_movement.call_count, 1)
        self.assertEqual(mov.update_infection_status.call_count, 2)

    def test_simulate_movement_centralHub(self):
        mov = movement.Movement()
        population = {}
        infected = {}
        recovered = {}
        config = {
            "infection_duration": 1440,
            "local_distance": 5,
            "long_distance": 30,
            "sd_factor": 0.6,
            "type": "SARS-COV-2",
            "infection_distance": 5,
            "mask_prob_infected_out_range": 0.2,
            "mask_prob_infected_in_range": 0.5,
            "mask_prob_susceptible": 0.5,
            "mask_prob_both_out_range": 0.02,
            "mask_prob_both_in_range": 0.25,
            "vaccine_probability": -1,
            "vaccine_efficacy_range": [0.64, 0.67, 0.94, 0.95],
            "mask_probability": -1,
            "time_conversion_factor": 24,
            "base_infection_probability": 0.6,
            "daily_prob_change": 0.9,
            "peak_infection_sars": 10,
            "daily_prob_increase_sars": 1.1,
            "daily_prob_decrease_sars": 0.9,
            "initial_infection_percentage": 2,
            "asymptomatic_probability": 0.3,
            "testing_probability": 0.5,
            "contact_tracing_efficiency": 1,
            "quarantine_location_x_limit": [-300, -260],
            "quarantine_location_y_limit": [-250, -210],
            "community_travel_probability": 0.02,
            "visit_hub_probability": 0.1,
            "community_coordinates": [[-280, -100, 120, 300], [-80, 100, 120, 300], [120, 300, 120, 300],
                                      [-280, -100, -80, 100], [-80, 100, -80, 100], [120, 300, -80, 100],
                                      [-280, -100, -280, -100], [-80, 100, -280, -100], [120, 300, -280, -100]]
        }
        person_obj_1 = Mock()
        person_obj_1.is_central_hub = False
        person_obj_1.is_quarantined = False
        turtle_obj_1 = Mock()
        turtle_obj_1.goto = Mock()
        person_obj_1.turtle = turtle_obj_1
        person_obj_2 = Mock()
        person_obj_2.is_central_hub = True
        person_obj_2.is_quarantined = False
        turtle_obj_2 = Mock()
        turtle_obj_2.goto = Mock()
        person_obj_2.turtle = turtle_obj_2
        person_obj_3 = Mock()
        person_obj_3.is_central_hub = False
        person_obj_3.is_quarantined = False
        turtle_obj_3 = Mock()
        turtle_obj_3.goto = Mock()
        person_obj_3.turtle = turtle_obj_3
        population[0] = person_obj_1
        population[1] = person_obj_2
        population[2] = person_obj_2
        random_mock = Mock()
        random_mock.side_effect = [0.004, 0.5, 0.93]
        randMock.random = random_mock
        randMock.choice = Mock(return_value=30)
        randint_mock = Mock()
        randint_mock.side_effect = [10, 10, 200, 30, 0]
        randMock.randint = randint_mock
        mov.random_movement = Mock()
        mov.update_infection_status = Mock()
        get_displacement_mock = Mock()
        get_displacement_mock.side_effect = [[120, 300]]
        mov.get_displacement_coordinates = get_displacement_mock
        mov.simulate_movement_centralHub(population, infected, recovered, config)
        # randMock.randint.assert_any_call(-80, 100)
        turtle_obj_1.goto.assert_called_once_with(10, 10)
        turtle_obj_2.goto.assert_called_once_with(0, 30)
        self.assertEqual(mov.random_movement.call_count, 1)
        self.assertEqual(mov.update_infection_status.call_count, 3)
if __name__ == '__main__':
    unittest.main()