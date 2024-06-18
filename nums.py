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

# Function to filter and sort sequences based on minimum occurrences
def filter_and_sort_sequences(sequences, min_occurrences):
    filtered_sequences = {seq: count for seq, count in sequences.items() if count > min_occurrences}
    sorted_sequences = dict(sorted(filtered_sequences.items(), key=lambda item: item[1], reverse=True))
    return sorted_sequences

def main():
    st.title("Recurring Sequences Viewer")

    folder_path = 'csv_files'  # Folder containing the CSV files

    if not os.path.exists(folder_path):
        st.error(f"The folder '{folder_path}' does not exist.")
        return

    # Sidebar for settings
    st.sidebar.header("Settings")
    min_occurrences = st.sidebar.slider("Minimum Occurrences", 1, 10, 1)
    seq_length_range = st.sidebar.slider("Sequence Length Range", 2, 10, (2, 5))

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
        for seq_length in range(seq_length_range[0], seq_length_range[1] + 1):
            sequences = extract_sequences(numbers, seq_length)
            for seq, count in sequences.items():
                all_sequences[seq] += count

    # Display results for each sequence length
    for seq_length in range(seq_length_range[0], seq_length_range[1] + 1):
        filtered_and_sorted_sequences = filter_and_sort_sequences(
            {seq: count for seq, count in all_sequences.items() if len(seq) == seq_length},
            min_occurrences
        )

        if filtered_and_sorted_sequences:
            st.subheader(f"Recurring Sequences of Length {seq_length} Across All Files")
            df_sequences = pd.DataFrame(list(filtered_and_sorted_sequences.items()), columns=['Sequence', 'Count'])
            df_sequences['Sequence'] = df_sequences['Sequence'].apply(lambda x: ' -> '.join(map(str, x)))
            st.dataframe(df_sequences)
        #else:
        #    st.warning(f"No recurring sequences of length {seq_length} found with the given filters.")

if __name__ == "__main__":
    main()
