import math
import pandas as pd
import random
from datetime import datetime, timedelta
import calendar
import datetime
from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Data Collection (sample data)

# Define a list of industries and interests to generate sample data
industries = ['Technology', 'Finance', 'Marketing', 'Engineering', 'Art']
interests_pool = [['AI', 'Data Science'], ['Investments', 'Risk Management'], ['Digital Marketing', 'Brand Management'],
                  ['Mechanical Engineering', 'Robotics'], ['Painting', 'Sculpture']]

aspiring_professionals = []
num_professionals = 10  # Number of aspiring professionals to generate # use input function to take input from user 

# Generate random data for aspiring professionals
for i in range(1, num_professionals+1):
    name = f'Aspiring{i}'
    industry = random.choice(industries)
    interests = random.choice(interests_pool)
    activity = round(random.uniform(0.4, 0.8), 1)
    aspiring_professional = {'id': i, 'name': name, 'industry': industry, 'interests': interests, 'activity': activity}
    aspiring_professionals.append(aspiring_professional)

# Print the generated list
for professional in aspiring_professionals:
    print(professional)

senior_executives = []
num_executives = 10  # Number of senior executives to generate # use input function to take input from user 


# Generate random data for senior executives
for i in range(1, num_executives+1):
    name = f'Senior{i}'
    industry = random.choice(industries)
    interests = random.choice(interests_pool)
    appearances = random.randint(1, 5)
    senior_executive = {'id': i, 'name': name, 'industry': industry, 'interests': interests, 'appearances': appearances}
    senior_executives.append(senior_executive)

# Print the generated list
for executive in senior_executives:
    print(executive)


# Step 2: Data Preprocessing
aspiring_df = pd.DataFrame(aspiring_professionals)
senior_df = pd.DataFrame(senior_executives)

# Convert interests list to string
aspiring_df['interests'] = aspiring_df['interests'].apply(lambda x: ' '.join(x))
senior_df['interests'] = senior_df['interests'].apply(lambda x: ' '.join(x))

# Create a set of all unique industries and interests
all_industries = set(aspiring_df['industry']).union(set(senior_df['industry']))
all_interests = set(aspiring_df['interests']).union(set(senior_df['interests']))

# Perform one-hot encoding
aspiring_encoded = pd.get_dummies(aspiring_df[['industry', 'interests']], columns=['industry', 'interests'], prefix='', prefix_sep='')
senior_encoded = pd.get_dummies(senior_df[['industry', 'interests']], columns=['industry', 'interests'], prefix='', prefix_sep='')

# Add missing columns to the one-hot encoded matrices
missing_industries = all_industries - set(aspiring_encoded.columns)
missing_interests = all_interests - set(aspiring_encoded.columns)
for industry in missing_industries:
    aspiring_encoded[industry] = 0
    senior_encoded[industry] = 0
for interest in missing_interests:
    aspiring_encoded[interest] = 0
    senior_encoded[interest] = 0

# Ensure compatibility between X and Y matrices
if aspiring_encoded.shape[1] != senior_encoded.shape[1]:
    min_features = min(aspiring_encoded.shape[1], senior_encoded.shape[1])
    aspiring_encoded = aspiring_encoded.iloc[:, :min_features]
    senior_encoded = senior_encoded.iloc[:, :min_features]

# Step 3: Matching Algorithm
X = aspiring_encoded.to_numpy()
Y = senior_encoded.to_numpy()
similarity_matrix = cosine_similarity(X, Y)

# Step 4: Recommendation Generation
def generate_recommendations(aspiring_id, num_recommendations=1):
    aspiring_index = aspiring_df.loc[aspiring_df['id'] == aspiring_id].index[0]
    similarities = similarity_matrix[aspiring_index]
    top_indices = similarities.argsort()[:-num_recommendations-1:-1]
    return senior_df.iloc[top_indices]

# Generate all possible combinations of pairs
aspiring_combinations = list(combinations(aspiring_df['id'], 1))
senior_combinations = list(combinations(senior_df['id'], 1))

# Step 5: Coffee Schedule Generation
def generate_coffee_schedule(aspiring_combinations, senior_combinations):
    coffee_schedule = []
    
    for aspiring_combination in aspiring_combinations:
        aspiring_id_1 = aspiring_combination
        recommended_executives = generate_recommendations(aspiring_id_1, num_recommendations=len(senior_executives))
        #print(f'recommended_executives {recommended_executives} as: {aspiring_id_1}')
        for _, executive in recommended_executives.iterrows():
            senior_id_1 = executive['id']
        # for senior_combination in senior_combinations:
        #     senior_id_1 = senior_combination
            #if (aspiring_id_1, senior_id_1) != (aspiring_id_2, senior_id_2):
            coffee_schedule.append({
                'aspiring_id_1': aspiring_id_1,
                #'aspiring_id_2': aspiring_id_2,
                'senior_id_1': senior_id_1
                #'senior_id_2': senior_id_2
            })
    return coffee_schedule

# Generate the coffee schedule
coffee_schedule = generate_coffee_schedule(aspiring_combinations, senior_combinations)

# Step 5: Weekly Coffee Chat Roster with Dates and Times
from datetime import datetime, timedelta

def generate_pair_combinations(coffee_chats):
    pair_combinations = []

    for chat in coffee_chats:
        aspiring_ids = [chat['aspiring_id_1'], chat['aspiring_id_2']]
        senior_ids = [chat['senior_id_1'], chat['senior_id_2']]
        combinations_list = list(combinations(aspiring_ids + senior_ids, 2))
        pair_combinations.extend(combinations_list)

    return pair_combinations

def remove_duplicates(coffee_chats):
    unique_chats = []
    unique_pairs = set()

    for chat in coffee_chats:
        pair = tuple(sorted([chat['aspiring_id_1'], chat['aspiring_id_2'], chat['senior_id_1'], chat['senior_id_2']]))
        if pair not in unique_pairs:
            unique_pairs.add(pair)
            unique_chats.append(chat)

    return unique_chats

def num_of_weeks_in_month(year, month):
    from math import ceil
    from calendar import monthrange

    return int(ceil(float(monthrange(year, month)[0]+monthrange(year,month)[1])/7))


def generate_coffee_chats(coffee_schedule, start_date, num_months, start_month):
    coffee_chats = []
    current_date = start_date.replace(hour=13, minute=0)  # Set the time to 1:00 PM
    month_number = start_date.month
    week_number = 1  # Initialize the week number to 1
    repeated_pairs = set()  # Track repeated pairs
    
    for _ in range(num_months):
        if month_number > 12:
            month_number = 1
        _, num_days = calendar.monthrange(start_date.year, month_number)
        month_name = calendar.month_name[month_number]
        weeks_no = len(calendar.monthcalendar(start_date.year, month_number))
        
        for week in range(1, weeks_no+1):
            random.shuffle(coffee_schedule)
            meeting_count = 0  # Counter to keep track of the number of meetings scheduled in the day
            
            for pair in coffee_schedule:
                aspiring_id_1 = pair['aspiring_id_1']
                senior_id_1 = pair['senior_id_1']

                if month_number >= start_month and current_date.hour == 13:
                    # Check if the meeting count for the week has reached the maximum limit
                    if meeting_count < 4:
                        # Check if the pair is not repeated before all other pairs meet at least once
                        if (aspiring_id_1, senior_id_1) not in repeated_pairs:
                            coffee_chats.append({
                                'aspiring_id_1': aspiring_id_1,
                                'senior_id_1': senior_id_1,
                                'month': month_name,
                                'week_number': week_number,
                                'date': current_date.strftime('%Y-%m-%d'),
                                'time': current_date.strftime('%H:%M')
                            })
                            meeting_count += 1
                            repeated_pairs.add((aspiring_id_1, senior_id_1))
                    else:
                        break
                        
            current_date_day_no = current_date.day
            current_date += timedelta(days=7)  # Move to the next week
            
            if num_days < current_date_day_no + 7:
                break

            week_number = week + 1  # Increment the week number when a week has passed
            
        month_number += 1  # Move to the next month
        week_number = 1  # Reset the week number to 1 at the start of a new month

    return coffee_chats


# Specify the start date and number of months to generate coffee chats
start_date = datetime(2023, 1, 1)  # Start date
num_months = 3  # Number of months to generate coffee chats
start_month = 1  # Start month number

# Step 6: Generate the coffee chat roster
coffee_chats = generate_coffee_chats(coffee_schedule, start_date, num_months, start_month)

# Print the coffee chat roster
# print("\nCoffee Chat Roster:")
# for chat in coffee_chats:
#     print(chat)

print("\nCoffee Chat Roster:")
current_month = ""  # Track the current month
current_week = 0  # Track the current week number
for chat in coffee_chats:
    month_name = chat['month']
    week_number = chat['week_number']
    
    if month_name != current_month:
        current_month = month_name
        print(f"\nMonth: {current_month}")

    if week_number != current_week:
        current_week = week_number
        print(f"Week: {current_week}")

    aspiring_id_1 = chat['aspiring_id_1']
    senior_id_1 = chat['senior_id_1']
    time = chat['time']
    date = chat['date']

    print(f"Aspiring Professional {aspiring_id_1} meets with Senior Executive {senior_id_1}")
    print(f"Time: {time}")
    print(f"Date: {date}\n")
