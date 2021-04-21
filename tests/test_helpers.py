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
            "base_infection_probability": 0.3,
            "daily_prob_change": 0.9,
            "peak_infection_sars": 14,
            "daily_prob_increase_sars": 1.05,
            "daily_prob_decrease_sars": 0.95,
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
        infected.infection_probability = 0
        infected.incubation_period = 7
        infected.infected_time = 140
        infected.update_prob_tracker = 13
        helpers.update_probability_sars(infected, config)
        self.assertEqual(infected.infection_probability, 0)
        infected.infected_time = 169
        helpers.update_probability_sars(infected, config)
        self.assertEqual(infected.infection_probability, 0.3)
        infected.update_prob_tracker = 24
        helpers.update_probability_sars(infected, config)
        self.assertEqual(infected.infection_probability, 0.315)
        infected.update_prob_tracker = 24
        infected.infected_time = 337
        helpers.update_probability_sars(infected, config)
        self.assertEqual(infected.infection_probability, 0.29924999999999996)
        print(infected.infection_probability)

    def test_update_probability_covid(self):
        infected = Mock()
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
            "peak_infection_sars": 14,
            "daily_prob_increase_sars": 1.05,
            "daily_prob_decrease_sars": 0.95,
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
        infected.infection_probability = 0
        infected.incubation_period = 5
        infected.infected_time = 40
        infected.update_prob_tracker = 13
        helpers.update_probability_covid(infected, config)
        self.assertEqual(infected.infection_probability, 0)
        infected.infected_time = 49
        helpers.update_probability_covid(infected, config)
        self.assertEqual(infected.infection_probability, 0.6)
        infected.update_prob_tracker = 24
        helpers.update_probability_covid(infected, config)
        self.assertEqual(infected.infection_probability, 0.54)

    def test_update_vaccination_and_mask_status(self):
        config = {
            "vaccine_probability": 0.3,
            "mask_probability": 0.6,
            "vaccine_efficacy_range": [0.64, 0.67, 0.94, 0.95]
        }
        population = {}
        person_obj_1 = Mock()
        person_obj_1.vaccination_status = False
        person_obj_1.mask_status = False
        population[0] = person_obj_1
        person_obj_2 = Mock()
        person_obj_2.vaccination_status = False
        person_obj_2.mask_status = False
        population[1] = person_obj_2
        random_mock = Mock()
        random_mock.side_effect = [0.1, 0.55, 0.96, 0.76]
        randMock.random = random_mock
        randMock.choice = Mock(return_value=0.94)
        helpers.update_vaccination_and_mask_status(population, config)
        self.assertEqual(population[0].vaccination_status, True)
        self.assertEqual(population[0].vaccine_efficacy, 0.94)
        self.assertEqual(population[0].mask_status, True)
        self.assertEqual(population[1].vaccination_status, False)
        self.assertEqual(population[1].mask_status, False)

    def test_get_effective_probability(self):
        infected_person = Mock()
        infected_person.infection_probability = 0.6
        infected_person.mask_status = False
        susceptible_person = Mock()
        susceptible_person.vaccination_status = False
        susceptible_person.mask_status = False
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
        effective_probability = helpers.get_effective_probability(infected_person, susceptible_person, 10, config)
        self.assertEqual(effective_probability, 0.6)

        susceptible_person.vaccination_status = True
        susceptible_person.vaccine_efficacy = 0.95
        effective_probability = helpers.get_effective_probability(infected_person, susceptible_person, 10, config)
        self.assertEqual(effective_probability, 0.030000000000000027)

        infected_person.mask_status = True
        infected_person.infection_probability = 0.6
        susceptible_person.vaccination_status = False
        effective_probability = helpers.get_effective_probability(infected_person, susceptible_person, 3, config)
        self.assertEqual(effective_probability, 0.12)

        effective_probability = helpers.get_effective_probability(infected_person, susceptible_person, 1, config)
        self.assertEqual(effective_probability, 0.3)

        infected_person.mask_status = False
        susceptible_person.mask_status = True
        infected_person.infection_probability = 0.6
        susceptible_person.vaccination_status = False
        effective_probability = helpers.get_effective_probability(infected_person, susceptible_person, 3, config)
        self.assertEqual(effective_probability, 0.3)

        infected_person.mask_status = True
        susceptible_person.mask_status = True
        infected_person.infection_probability = 0.6
        susceptible_person.vaccination_status = False
        effective_probability = helpers.get_effective_probability(infected_person, susceptible_person, 3, config)
        self.assertEqual(effective_probability, 0.012)

        effective_probability = helpers.get_effective_probability(infected_person, susceptible_person, 1, config)
        print(effective_probability)
        self.assertEqual(effective_probability, 0.15)

    def test_get_infection_status(self):
        config = {
            "infection_distance": 5
        }
        infected_person = Mock()
        infected_person.turtle = Mock()
        infected_person.infection_probability = 0.6
        infected_person.mask_status = False
        susceptible_person = Mock()
        susceptible_person.turtle = Mock()
        susceptible_person.turtle.distance = Mock(return_value=3)
        helpers.get_effective_probability = Mock(return_value=0.5)
        randMock.random = Mock(return_value=0.6)
        self.assertEqual(helpers.get_infection_status(infected_person, susceptible_person, config), False)
        randMock.random = Mock(return_value=0.3)
        self.assertEqual(helpers.get_infection_status(infected_person, susceptible_person, config), True)
        susceptible_person.turtle.distance = Mock(return_value=8)
        self.assertEqual(helpers.get_infection_status(infected_person, susceptible_person, config), False)

    def test_calculate_infections(self):
        config = {
            "asymptomatic_probability": 0.3
        }
        infected = {}
        susceptible = {}
        population = {}
        infected_person_obj = Mock()
        infected[0] = True
        susceptible_person_obj_1 = Mock()
        susceptible_person_obj_1.status = "S"
        susceptible[1] = True
        susceptible_person_obj_2 = Mock()
        susceptible_person_obj_2.status = "S"
        susceptible[2] = True
        susceptible_person_obj_3 = Mock()
        susceptible_person_obj_3.status = "S"
        susceptible[5] = True
        population[0] = infected_person_obj
        population[1] = susceptible_person_obj_1
        population[2] = susceptible_person_obj_2
        population[5] = susceptible_person_obj_3
        get_infection_status_mock = Mock()
        get_infection_status_mock.side_effect = [True, True, False]
        helpers.get_infection_status = get_infection_status_mock
        random_mock = Mock()
        random_mock.side_effect = [0.2, 0.4]
        randMock.random = random_mock
        helpers.calculate_infections(population, susceptible, infected, config)
        self.assertEqual(susceptible_person_obj_1.status, "AI")
        self.assertEqual(susceptible_person_obj_2.status, "I")
        self.assertEqual(susceptible_person_obj_3.status, "S")

    def test_infect_random_people(self):
        population = {}
        config = {
            "initial_infection_percentage": 100,
            "asymptomatic_probability": 0.5
        }
        random_mock = Mock()
        random_mock.side_effect = [0.48, 0.36, 0.12, 0.62, 0.78, 0.91]
        randMock.random = random_mock
        randint_mock = Mock()
        randint_mock.side_effect = [0, 1, 2, 3, 4, 5]
        randMock.randint = randint_mock
        for i in range(6):
            person_obj = Mock()
            person_obj.turtle = Mock()
            population[i] = person_obj
        helpers.infect_random_people(population, config)
        self.assertEqual(population[0].status, "AI")
        self.assertEqual(population[1].status, "AI")
        self.assertEqual(population[2].status, "AI")
        self.assertEqual(population[3].status, "I")
        self.assertEqual(population[4].status, "I")
        self.assertEqual(population[5].status, "I")

    def test_quarantine_person(self):
        config = {
            "quarantine_location_x_limit": [-300, -260],
            "quarantine_location_y_limit": [-250, -210]
        }
        person_obj = Mock()
        person_obj.turtle = Mock()
        person_obj.status = "I"
        randint_mock = Mock()
        randint_mock.side_effect = [-299, -232, -200, -243, -262, -213, -273, -222]
        randMock.randint = randint_mock
        helpers.quarantine_person(person_obj, config)
        self.assertEqual(person_obj.status, "QI")
        self.assertEqual(person_obj.x_limit, [-300, -260])
        self.assertEqual(person_obj.y_limit, [-250, -210])
        person_obj.turtle.goto.assert_any_call(-299, -232)
        person_obj.status = "I"
        helpers.quarantine_person(person_obj, config)
        self.assertEqual(person_obj.status, "QI")
        self.assertEqual(person_obj.x_limit, [-300, -260])
        self.assertEqual(person_obj.y_limit, [-250, -210])
        person_obj.turtle.goto.assert_any_call(-200, -243)

        person_obj.status = "AI"
        helpers.quarantine_person(person_obj, config)
        self.assertEqual(person_obj.status, "QI")
        self.assertEqual(person_obj.x_limit, [-300, -260])
        self.assertEqual(person_obj.y_limit, [-250, -210])
        person_obj.turtle.goto.assert_any_call(-262, -213)

        person_obj.status = "S"
        helpers.quarantine_person(person_obj, config)
        self.assertEqual(person_obj.status, "QS")
        self.assertEqual(person_obj.x_limit, [-300, -260])
        self.assertEqual(person_obj.y_limit, [-250, -210])
        person_obj.turtle.goto.assert_any_call(-273, -222)

    def test_trace_contacts(self):
        population = {}
        config = {
            "asymptotic_testing_probability": 0.7,
            "time_conversion_factor": 24,
            "quarantine_probability": 0.7
        }
        contacts = {
            1: {
                3: True,
                4: True
            },
            8: {10: True}
        }
        infected = {}
        infected_obj_1 = Mock()
        infected_obj_1.infected_time = 169
        infected_obj_1.incubation_period = 7
        infected_obj_1.status = "I"
        infected[1] = True
        contact_obj_1 = Mock()
        contact_obj_1.infected_time = 150
        contact_obj_1.incubation_period = 6
        contact_obj_2 = Mock()
        contact_obj_2.infected_time = 40
        contact_obj_2.incubation_period = 5
        infected_obj_2 = Mock()
        infected_obj_2.infected_time = 169
        infected_obj_2.incubation_period = 7
        infected_obj_2.status = "AI"
        contact_obj_3 = Mock()
        contact_obj_3.infected_time = 83
        contact_obj_3.incubation_period = 5
        population[1] = infected_obj_1
        population[3] = contact_obj_1
        population[4] = contact_obj_2
        population[8] = infected_obj_2
        population[10] = contact_obj_3
        random_mock = Mock()
        random_mock.side_effect = [0.6, 0.23]
        randMock.random = random_mock
        helpers.quarantine_person = Mock()
        helpers.trace_contacts(population, infected, contacts, config)
        self.assertEqual(helpers.quarantine_person.call_count, 3)

    def test_update_contacts(self):
        population = {}
        config = {
            "infection_distance" : 5,
            "contact_tracing_efficiency": 0.7
        }
        contacts = {
            2: {
                4: True
            }
        }
        person_obj_1 = Mock()
        person_obj_1.status = "I"
        person_obj_1.turtle = Mock()
        person_obj_1.turtle.distance = Mock(return_value= 3)
        contact_obj_1 = Mock()
        contact_obj_1.status = "S"
        contact_obj_1.turtle = Mock()
        contact_obj_1.turtle.distance = Mock(return_value=3)
        person_obj_2 = Mock()
        person_obj_2.status = "AI"
        person_obj_2.turtle = Mock()
        person_obj_2.turtle.distance = Mock(return_value=3)
        population[0] = person_obj_1
        population[1] = contact_obj_1
        population[2] = person_obj_2
        random_mock = Mock()
        random_mock.side_effect = [0.6, 0.23, 0.4, 0.13]
        randMock.random = random_mock
        helpers.update_contacts(population, contacts, config)
        self.assertEqual(contacts, {2: {4: True, 0: True, 1: True}, 0: {1: True, 2: True}})

    def test_filter_infectious(self):
        population = {}
        susceptible = {10: True, 32: True}
        infected = {25: True, 0: True}
        person_obj_1 = Mock()
        person_obj_1.status = "I"
        person_obj_2 = Mock()
        person_obj_2.status = "AI"
        person_obj_3 = Mock()
        person_obj_3.status = "S"
        person_obj_4 = Mock()
        person_obj_4.status = "QI"
        person_obj_5 = Mock()
        person_obj_5.status = "QS"
        population[0] = person_obj_1
        population[1] = person_obj_2
        population[2] = person_obj_3
        population[3] = person_obj_4
        population[4] = person_obj_5
        helpers.filter_infectious(population, susceptible, infected)
        self.assertEqual(susceptible, {10: True, 32: True, 2: True})
        self.assertEqual(infected, {25: True, 0: True, 1: True})