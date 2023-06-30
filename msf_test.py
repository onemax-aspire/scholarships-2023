import unittest
import math
import pandas as pd
import random
from datetime import datetime, timedelta
import calendar
from itertools import combinations


class CoffeeScheduleTestCase(unittest.TestCase):
    def setUp(self):
        # Initialize the test data
        self.aspiring_professionals = []
        self.senior_executives = []

        industries = ['Technology', 'Finance', 'Marketing', 'Engineering', 'Art']
        interests_pool = [['AI', 'Data Science'], ['Investments', 'Risk Management'], ['Digital Marketing', 'Brand Management'],
                          ['Mechanical Engineering', 'Robotics'], ['Painting', 'Sculpture']]

        num_professionals = 10  # Number of aspiring professionals to generate
        num_executives = 10  # Number of senior executives to generate

        for i in range(1, num_professionals + 1):
            name = f'Aspiring{i}'
            industry = random.choice(industries)
            interests = random.choice(interests_pool)
            activity = round(random.uniform(0.4, 0.8), 1)
            aspiring_professional = {'id': i, 'name': name, 'industry': industry, 'interests': interests,
                                     'activity': activity}
            self.aspiring_professionals.append(aspiring_professional)

        for i in range(1, num_executives + 1):
            name = f'Senior{i}'
            industry = random.choice(industries)
            interests = random.choice(interests_pool)
            appearances = random.randint(1, 5)
            senior_executive = {'id': i, 'name': name, 'industry': industry, 'interests': interests,
                                'appearances': appearances}
            self.senior_executives.append(senior_executive)

    def test_data_collection(self):
        # Test the data collection step
        num_aspiring_professionals = len(self.aspiring_professionals)
        num_senior_executives = len(self.senior_executives)

        self.assertEqual(num_aspiring_professionals, 10, "Number of aspiring professionals is incorrect")
        self.assertEqual(num_senior_executives, 10, "Number of senior executives is incorrect")

    def test_data_preprocessing(self):
        # Test the data preprocessing step
        aspiring_df = pd.DataFrame(self.aspiring_professionals)
        senior_df = pd.DataFrame(self.senior_executives)

        self.assertTrue('industry' in aspiring_df.columns, "Missing 'industry' column in aspiring_df")
        self.assertTrue('interests' in aspiring_df.columns, "Missing 'interests' column in aspiring_df")
        self.assertTrue('industry' in senior_df.columns, "Missing 'industry' column in senior_df")
        self.assertTrue('interests' in senior_df.columns, "Missing 'interests' column in senior_df")

    def test_matching_algorithm(self):
        # Test the matching algorithm step
        aspiring_combinations = list(combinations(range(1, 11), 1))
        senior_combinations = list(combinations(range(1, 11), 1))

        coffee_schedule = self.generate_coffee_schedule(aspiring_combinations, senior_combinations)

        self.assertTrue(len(coffee_schedule) == 100, "Incorrect number of coffee schedule entries")

    def test_coffee_schedule_generation(self):
        # Test the coffee schedule generation step
        coffee_schedule = self.generate_coffee_schedule([(1,), (2,), (3,)], [(4,), (5,), (6,)])

        self.assertEqual(len(coffee_schedule), 9, "Incorrect number of coffee schedule entries")

    def test_weekly_coffee_chat_roster(self):
        # Test the weekly coffee chat roster with dates and times
        start_date = datetime(2023, 1, 1)
        coffee_schedule = self.generate_coffee_schedule([(1,), (2,), (3,)], [(4,), (5,), (6,)])

        weekly_roster = self.generate_weekly_roster(coffee_schedule, start_date)

        self.assertEqual(len(weekly_roster), 3, "Incorrect number of weekly rosters")

        for i, roster in enumerate(weekly_roster):
            expected_date = start_date + timedelta(weeks=i)
            self.assertEqual(roster['date'], expected_date.strftime('%Y-%m-%d'), "Incorrect date in weekly roster")

            for j, entry in enumerate(roster['schedule']):
                expected_time = self.calculate_coffee_time(j)
                self.assertEqual(entry['time'], expected_time.strftime('%H:%M'), "Incorrect time in coffee schedule")

    def generate_coffee_schedule(self, aspiring_combinations, senior_combinations):
        coffee_schedule = []

        for aspiring_comb in aspiring_combinations:
            for senior_comb in senior_combinations:
                aspiring_ids = aspiring_comb
                senior_ids = senior_comb

                for aspiring_id in aspiring_ids:
                    for senior_id in senior_ids:
                        entry = {'aspiring_id': aspiring_id, 'senior_id': senior_id}
                        coffee_schedule.append(entry)

        return coffee_schedule

    def generate_weekly_roster(self, coffee_schedule, start_date):
        weekly_roster = []

        for i, entry in enumerate(coffee_schedule):
            date = start_date + timedelta(days=i)
            day_of_week = calendar.day_name[date.weekday()]

            # Assuming coffee chats are scheduled from Monday to Friday
            if day_of_week in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                time = self.calculate_coffee_time(i % 8)
                entry_data = {'aspiring_id': entry['aspiring_id'], 'senior_id': entry['senior_id'], 'date': date.strftime('%Y-%m-%d'), 'time': time.strftime('%H:%M')}
                roster_exists = False

                for roster in weekly_roster:
                    if roster['date'] == date.strftime('%Y-%m-%d'):
                        roster['schedule'].append(entry_data)
                        roster_exists = True
                        break

                if not roster_exists:
                    weekly_roster.append({'date': date.strftime('%Y-%m-%d'), 'schedule': [entry_data]})

        return weekly_roster

    def calculate_coffee_time(self, index):
        hour = math.floor(index / 2) + 9  # Coffee chats start from 9 AM and occur every 30 minutes
        minute = 0 if index % 2 == 0 else 30
        return datetime(2023, 1, 1, hour, minute)


if __name__ == '__main__':
    unittest.main()
