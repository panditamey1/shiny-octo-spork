from collections import defaultdict
import os

import os
import streamlit as st
import pandas as pd
from collections import defaultdict
import json
import heapq

follow_counts = {}




import csv
from collections import Counter
number_counts = defaultdict(lambda: defaultdict(int))

# Function to read CSV and update counts
def update_counts_from_csv(file_path, number_counts=number_counts):
    # Read the numbers from the CSV file
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        numbers = [int(row['Number']) for row in csv_reader]

    # Initialize a nested dictionary to count occurrences

    # Update counts based on numbers coming after the previous number
    for i in range(len(numbers) - 1):
        current_number = numbers[i]
        next_number = numbers[i + 1]
        number_counts[current_number][next_number] += 1

    # Convert defaultdict to regular dict for clean output
    number_counts = {k: dict(v) for k, v in number_counts.items()}
    
    return number_counts
# Function to get top k numbers coming after a given number
def get_top_k_after_given_number(number, k, number_counts):
    if number not in number_counts:
        return []

    next_numbers = number_counts[number]
    top_k_numbers = sorted(next_numbers.items(), key=lambda item: item[1], reverse=True)[:k]
    
    # return [num for num, count in top_k_numbers]
    return top_k_numbers
csv_files = 'csv_files'
final_counts = defaultdict(int)
# number_counts = defaultdict(lambda: defaultdict(int))
for file_name in os.listdir(csv_files):
    if file_name.endswith('.csv'):
        file_path = os.path.join(csv_files, file_name)  
        number_counts = update_counts_from_csv(file_path)

# save number_counts to a json file
with open('number_counts.json', 'w') as f:
    json.dump(number_counts, f)
given_number = 15
k = 3
top_k = get_top_k_after_given_number(given_number, k, number_counts)
print(f"Top {k} numbers coming after {given_number}: {top_k}")
import pandas as pd
import os

# create dataframe
df = pd.DataFrame(top_k, columns=['Number', 'Count'])

