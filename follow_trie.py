import csv
from collections import defaultdict, deque
import heapq

import os
import streamlit as st
import pandas as pd
from collections import defaultdict
import json
follow_counts = {}




import csv
from collections import Counter
# number_counts = defaultdict(lambda: defaultdict(int))

# # Function to read CSV and update counts
# def update_counts_from_csv(file_path, number_counts=number_counts):
#     # Read the numbers from the CSV file
#     with open(file_path, mode='r') as file:
#         csv_reader = csv.DictReader(file)
#         numbers = [int(row['Number']) for row in csv_reader]

#     # Initialize a nested dictionary to count occurrences

#     # Update counts based on numbers coming after the previous number
#     for i in range(len(numbers) - 1):
#         current_number = numbers[i]
#         next_number = numbers[i + 1]
#         number_counts[current_number][next_number] += 1

#     # Convert defaultdict to regular dict for clean output
#     number_counts = {k: dict(v) for k, v in number_counts.items()}
    
#     return number_counts

# Example usage:
# file_path = 'numbers.csv'  # replace with your CSV file path
# sorted_counts = update_counts_from_csv(file_path)
# print(sorted_counts)

# Define the Trie Node
class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.counts = defaultdict(int)
        self.top_k_heap = []

# Define the Trie structure
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, sequence):
        node = self.root
        for num in sequence:
            node = node.children[num]

    def update_counts(self, sequence):
        node = self.root
        for i in range(len(sequence) - 1):
            current_num = sequence[i]
            next_num = sequence[i + 1]
            node = node.children[current_num]
            node.counts[next_num] += 1
            # Maintain a max-heap for the top k counts
            heapq.heappush(node.top_k_heap, (-node.counts[next_num], next_num))
            # If heap size exceeds k, remove the smallest element
            if len(node.top_k_heap) > k:
                heapq.heappop(node.top_k_heap)

    def get_top_k(self, number, k):
        node = self.root
        if number not in node.children:
            return []

        node = node.children[number]
        # Retrieve top k elements from the heap
        top_k = []
        while node.top_k_heap and len(top_k) < k:
            count, num = heapq.heappop(node.top_k_heap)
            top_k.append((num, -count))
        
        # Restore the heap since heaps are mutable and pop removes elements
        for count, num in top_k:
            heapq.heappush(node.top_k_heap, (-count, num))
        
        return top_k

# Function to read CSV and update counts
def update_counts_from_csv(file_path, trie, k):
    # Read the numbers from the CSV file
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        numbers = [int(row['Number']) for row in csv_reader]

    # Update counts in the trie
    trie.update_counts(numbers)

# Example usage:

csv_files = 'csv_files'
final_counts = defaultdict(int)
trie = Trie()
k = 5
for file_name in os.listdir(csv_files):
    if file_name.endswith('.csv'):
        # df = pd.read_csv(os.path.join(csv_files, file_name))
        # numbers = df['Number'].tolist()
        # for i in range(len(numbers) - 1):
        #     if numbers[i] not in follow_counts:
        #         follow_counts[numbers[i]] = []
        #     follow_counts[numbers[i]].append(numbers[i + 1])
        
        update_counts_from_csv(os.path.join(csv_files, file_name), trie, k)

# Get top k numbers coming after a given number
given_number = 4
top_k_numbers = trie.get_top_k(given_number, k)
print(f"Top {k} numbers coming after {given_number}: {top_k_numbers}")
