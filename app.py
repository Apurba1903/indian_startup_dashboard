import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(layout="wide", page_title='Startup Analysis')


df = pd.read_csv('startup_cleaned.csv')

def load_investor_details(investor):
    st.title(investor)

    # Load the recent 5 investment of the investor
    last4_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last4_df)

    col1, col2 = st.columns(2)
    with col1:

        # Biggest Investments
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader('Biggest Investments')
        st.dataframe(big_series)

        # Sectors Invested
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct='%0.1f%%')
        st.pyplot(fig1)


    with col2:

        # Biggest Investments Pie
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)



st.sidebar.title('Startup Funding Analysis')


option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    st.title('Overall Analysis')


elif option == 'Startup':
    st.sidebar.selectbox('Select Startup', sorted(df["startup"].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')


else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)

    #st.title('Investor Analysis')












