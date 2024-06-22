import streamlit as st
import pandas as pd
import os

# Load CSV files from the "csv_files" folder
csv_folder = 'csv_files'
csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]

# Function to load a CSV file
def load_csv(file):
    return pd.read_csv(os.path.join(csv_folder, file))

# Initialize session state variables
if 'current_file_index' not in st.session_state:
    st.session_state.current_file_index = 0

if 'number_index' not in st.session_state:
    st.session_state.number_index = 0

# Load the current CSV file
current_file = csv_files[st.session_state.current_file_index]
df = load_csv(current_file)

# Function to show the next number
def show_next_number():
    if st.session_state.number_index < len(df) - 1:
        st.session_state.number_index += 1
    else:
        st.session_state.number_index = 0
        if st.session_state.current_file_index < len(csv_files) - 1:
            st.session_state.current_file_index += 1
        else:
            st.session_state.current_file_index = 0

# Display the current number
current_number = df['Number'][st.session_state.number_index]
st.write(f"File: {current_file}")
st.write(f"Current Number: {current_number}")

# Button to show the next number
if st.button('Next Number'):
    show_next_number()
    df = load_csv(csv_files[st.session_state.current_file_index])
    current_number = df['Number'][st.session_state.number_index]
    st.write(f"Next Number: {current_number}")
