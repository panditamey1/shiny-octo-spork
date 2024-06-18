import os
import pandas as pd
import threading

# Directory containing the CSV files
csv_directory = 'csv_files'

# Function to display the last 20 numbers from the current position
def display_last_20_numbers_from_current(current_index, df):
    start_index = max(0, current_index - 19)
    print("Last 20 numbers from current position:")
    print(df['Number'][start_index:current_index + 1].to_list())

# Function to prompt user for input
def prompt_user():
    user_input = None
    def get_input():
        nonlocal user_input
        user_input = input("Enter 1/2/3: ")
    
    input_thread = threading.Thread(target=get_input)
    input_thread.start()
    input_thread.join(timeout=20)
    if user_input is None:
        print("Time's up! Showing next number...")
    else:
        try:
            user_input = int(user_input)
            if user_input in [1, 2, 3]:
                print(f"You entered: {user_input}")
            else:
                print("Invalid input! Showing next number...")
        except ValueError:
            print("Invalid input! Showing next number...")
    
    return user_input

# Function to process a single CSV file
def process_csv(file_path):
    df = pd.read_csv(file_path)
    for index, number in enumerate(df['Number']):
        print(f"Current number: {number}")
        display_last_20_numbers_from_current(index, df)
        user_input = prompt_user()
        if user_input is not None:
            # Process the input as needed
            pass

# Main function to iterate through CSV files in the directory
def main():
    for file_name in os.listdir(csv_directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(csv_directory, file_name)
            print(f"\nProcessing file: {file_path}")
            process_csv(file_path)

if __name__ == "__main__":
    main()
