import os
import pandas as pd
import streamlit as st

# Directory containing the CSV files
csv_directory = 'csv_files'

# Function to display the last 20 numbers from the current position
def display_last_20_numbers_from_current(current_index, df):
    start_index = max(0, current_index - 19)
    st.write("Last 20 numbers from current position:")
    st.write(df['Number'][start_index:current_index + 1].to_list())

# Function to process a single CSV file
def process_csv(file_path):
    df = pd.read_csv(file_path)
    for index, number in enumerate(df['Number']):
        st.write(f"Current number: {number}")
        display_last_20_numbers_from_current(index, df)
        
        user_input = st.selectbox("Enter 1/2/3:", [1, 2, 3], key=f'{file_path}_{index}')
        if st.button("Submit", key=f'submit_{file_path}_{index}'):
            st.write(f"You entered: {user_input}")

# Main function to iterate through CSV files in the directory
def main():
    st.title("CSV Number Processor")
    st.write("Processing CSV files...")

    for file_name in os.listdir(csv_directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(csv_directory, file_name)
            st.write(f"\nProcessing file: {file_path}")
            process_csv(file_path)

if __name__ == "__main__":
    main()
