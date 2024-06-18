
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

# Example usage:
# file_path = 'numbers.csv'  # replace with your CSV file path
# sorted_counts = update_counts_from_csv(file_path)
# print(sorted_counts)

csv_files = 'csv_files'
final_counts = defaultdict(int)
for file_name in os.listdir(csv_files):
    if file_name.endswith('.csv'):
        # df = pd.read_csv(os.path.join(csv_files, file_name))
        # numbers = df['Number'].tolist()
        # for i in range(len(numbers) - 1):
        #     if numbers[i] not in follow_counts:
        #         follow_counts[numbers[i]] = []
        #     follow_counts[numbers[i]].append(numbers[i + 1])
        sorted_counts = update_counts_from_csv(os.path.join(csv_files, file_name), number_counts)

# Sort the final counts dictionary by count values
#sorted_final_counts = dict(sorted(final_counts.items(), key=lambda item: item[1], reverse=True))
print(sorted_counts)

def get_top_k_after(number_counts, number, k):
    if number not in number_counts:
        return []

    # Use heapq to get the top k counts
    heap = []
    for next_number, count in number_counts[number].items():
        heapq.heappush(heap, (-count, next_number))
    
    top_k = []
    while heap and len(top_k) < k:
        count, next_number = heapq.heappop(heap)
        top_k.append((next_number, -count))
    
    return top_k
given_number = 4
k = 7
top_k_numbers = get_top_k_after(number_counts, given_number, k)
print(f"Top {k} numbers coming after {given_number}: {top_k_numbers}")

# Display the sorted counts
# save follow_counts to json file
#with open('follow_counts.json', 'w') as f:
#    json.dump(follow_counts, f)

