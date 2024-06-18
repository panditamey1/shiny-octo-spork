import streamlit as st
import pandas as pd
import os
from collections import defaultdict

# Function to read a single CSV file into a DataFrame
def read_csv_file(file_path):
    return pd.read_csv(file_path)

# Function to extract sequences of a given length from a list of numbers
def extract_sequences(data, seq_length):
    sequences = defaultdict(int)
    for i in range(len(data) - seq_length + 1):
        sequence = tuple(data[i:i+seq_length])
        sequences[sequence] += 1
    return sequences

# Function to filter and merge sequences starting with the given user sequence
def filter_and_merge_sequences(all_sequences, user_sequence, min_occurrences):
    merged_sequences = defaultdict(int)
    user_seq_len = len(user_sequence)

    # Check sequences starting with the user sequence
    for (seq_length, seq), count in all_sequences.items():
        if seq[:user_seq_len] == user_sequence and count >= min_occurrences:
            merged_sequences[seq] += count

    # Merge longer sequences into shorter ones
    final_sequences = defaultdict(int)
    for seq, count in merged_sequences.items():
        for i in range(len(seq) - user_seq_len + 1):
            sub_seq = seq[:user_seq_len + i]
            final_sequences[sub_seq] += count

    return final_sequences

def main():
    st.title("Recurring Sequences Viewer")

    folder_path = 'csv_files'  # Folder containing the CSV files

    if not os.path.exists(folder_path):
        st.error(f"The folder '{folder_path}' does not exist.")
        return

    # Sidebar for settings
    st.sidebar.header("Settings")
    min_occurrences = st.sidebar.slider("Minimum Occurrences", 1, 10, 1)
    max_seq_length = st.sidebar.slider("Maximum Sequence Length", 2, 20, 10)

    # Read CSV files from the folder
    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

    all_sequences = defaultdict(int)

    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        df = read_csv_file(file_path)
        
        if 'Number' not in df.columns:
            st.warning(f"File '{file_name}' does not contain a 'Number' column.")
            continue

        numbers = df['Number'].tolist()

        # Collect sequences across all files
        for seq_length in range(2, max_seq_length + 1):
            sequences = extract_sequences(numbers, seq_length)
            for seq, count in sequences.items():
                all_sequences[(seq_length, seq)] += count

    # User input for the starting sequence
    user_input = st.text_input("Enter the starting sequence (comma-separated numbers):", "")
    
    if user_input:
        try:
            user_sequence = tuple(map(int, user_input.split(',')))
            st.subheader(f"Checking sequences starting with {user_sequence}:")

            filtered_and_merged_sequences = filter_and_merge_sequences(all_sequences, user_sequence, min_occurrences)

            if filtered_and_merged_sequences:
                df_sequences = pd.DataFrame(list(filtered_and_merged_sequences.items()), columns=['Sequence', 'Count'])
                df_sequences['Sequence'] = df_sequences['Sequence'].apply(lambda x: ' -> '.join(map(str, x)))
                st.dataframe(df_sequences)
            else:
                st.warning(f"No recurring sequences found starting with {user_sequence} with the given filters.")
        except ValueError:
            st.error("Invalid input. Please enter a comma-separated list of numbers.")

if __name__ == "__main__":
    main()
