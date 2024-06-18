import streamlit as st
import json
import numpy as np
import pandas as pd


follow_counts = json.load(open('follow_counts.json'))

# take input number from user
number = st.number_input("Enter number:", min_value=0, max_value=36, step=1, key='number')
top_n = st.number_input("Enter number of top numbers:", min_value=1, max_value=36, step=1, value=10, key='top_n')


def get_top_following_numbers(number, top_n=5):
    number = str(number)
    follow_list = follow_counts[number]
    follow_count_pairs = [(i, follow_list[i]) for i in range(len(follow_list))]
    follow_count_pairs.sort(key=lambda x: x[1], reverse=True)
    # get key only
    follow_count_pairs = [i for i, _ in follow_count_pairs]
    return follow_count_pairs[:top_n]
if st.button("Show Top Numbers"):
    top_numbers = get_top_following_numbers(number, top_n=top_n)
    print(top_numbers)
    df = pd.DataFrame(top_numbers, columns=["Number", "Count"])
    st.write(f"Top {top_n} numbers following {number}:")
    st.table(df.transpose())