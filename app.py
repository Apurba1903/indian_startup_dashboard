import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(layout="wide", page_title='Startup Analysis')


df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')

df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# General Analysis
def load_overall_analysis():
    st.title('Overall Analysis')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Total Invested Amount
        total = round(df['amount'].sum())
        st.metric('Total', str(total) + ' Cr')

    with col2:
        # Maximum Amount Infused in a Startup
        max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('Max', str(round(max_funding)) + ' Cr')

    with col3:
        # Average Funding to Company
        avg_funding = df.groupby('startup')['amount'].sum().mean()
        st.metric('Avg', str(round(avg_funding)) + ' Cr')

    with col4:
        # Total Funded Startups
        total_funded_startups = df['startup'].nunique()
        st.metric('Total Funded Startups', str(total_funded_startups))


    # Month on Month Graph
    st.header('Month on Month Graph')
    selected_variable = st.selectbox('Select Type', options=['Total', 'Count'])
    if selected_variable == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
        fig5, ax5 = plt.subplots()
        ax5.plot(temp_df['x_axis'], temp_df['amount'])
        st.pyplot(fig5)
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
        fig6, ax6 = plt.subplots()
        ax6.plot(temp_df['x_axis'], temp_df['amount'])
        st.pyplot(fig6)





# Investor Sector
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

        # Cities
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('Invested Cities')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct='%0.1f%%')
        st.pyplot(fig3)


    with col2:

        # Biggest Investments Pie
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

        # Rounds Invested
        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Rounds Invested')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct='%0.1f%%')
        st.pyplot(fig2)

        # Year on Investment
        year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader('Year on Year Investment')
        fig4, ax4 = plt.subplots()
        ax4.plot(year_series.index, year_series.values)
        st.pyplot(fig4)





st.sidebar.title('Startup Funding Analysis')


option = st.sidebar.selectbox('Select One', ['Overall', 'Startup', 'Investor'])

if option == 'Overall':
    load_overall_analysis()


elif option == 'Startup':
    st.sidebar.selectbox('Select Startup', sorted(df["startup"].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')


else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)

