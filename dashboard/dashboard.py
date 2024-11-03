import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


def create_sum_hour_df(df):
    sum_hour_df = df.groupby(by="hour").total.sum().sort_values(ascending=False).reset_index()
    sum_hour_df['hour'] = sum_hour_df['hour'].map(str)
    return sum_hour_df

def create_work_holiday_ratio(df):
    work_holiday_ratio = df.groupby(by="classify_day").agg({
        'casual' : 'sum',
        "registered" : 'sum',
        'total' : 'sum'}).reset_index()
    return work_holiday_ratio

cleaned_hour_df = pd.read_csv('https://drive.google.com/uc?export=download&id=1Gqq1hOdO7CyQ2t266StNGOo6o5KBATRd')
cleaned_day_df = pd.read_csv('https://drive.google.com/uc?export=download&id=1_xLobGvShWAotqwUHarx6aTi6OnR0oZV')

cleaned_hour_df["date"] = pd.to_datetime(cleaned_hour_df["date"])
cleaned_day_df["date"] = pd.to_datetime(cleaned_day_df["date"])

min_date = cleaned_day_df['date'].min()
max_date = cleaned_day_df['date'].max()



with st.sidebar:
    start_date, end_date = st.date_input(
        label = "Select date range",
        min_value = min_date,
        max_value = max_date,
        value=[min_date, max_date]
    )

main_day_df = cleaned_day_df[(cleaned_day_df["date"]>= str(start_date)) & (cleaned_day_df["date"] <= str(end_date))]
main_hour_df = cleaned_hour_df[(cleaned_hour_df["date"] >= str(start_date)) & (cleaned_hour_df["date"] <= str(end_date))]

sum_hour_df = create_sum_hour_df(main_hour_df)
work_holiday_ratio = create_work_holiday_ratio(main_day_df)

st.header("Melody's Bike Sharing Dashboard :bike:")

st.subheader('Daily Bike Rents')

col1, col2 = st.columns(2)

with col1:
    total_orders = main_day_df.total.sum()
    st.metric("Total Bike Rents", value=total_orders)

with col2:
    col1, col2 = st.columns(2)
    with col1:
        total_casual = main_day_df.casual.sum()
        st.metric("Casual", value=total_casual)
    with col2:
        total_registered = main_day_df.registered.sum()
        st.metric("Registered", value=total_registered)

fig, ax = plt.subplots(figsize=(30, 16))

ax.plot(
    main_day_df["date"],
    main_day_df["total"],
    marker = 'o',
    linewidth=2,
    color='#90CAF9'
)
ax.tick_params(axis='y', labelsize=18)
ax.tick_params(axis='x', labelsize=20)

st.pyplot(fig)



st.subheader("Highest & Lowest Bike Rent Time")


fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(30, 15))

colors = ['#90CAF9', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3']

ax[0].bar(x=sum_hour_df.head(5)['hour'], height=sum_hour_df.head(5)["total"], color=colors)
ax[0].set_ylabel(None)
ax[0].set_xlabel('Hour', fontsize=20)
ax[0].set_title("Highest Bike Rent Time", loc="center", fontsize=25)
ax[0].tick_params(axis='y', labelsize=18)
ax[0].tick_params(axis='x', labelsize=18)

ax[1].bar(x=sum_hour_df.tail(5).sort_values(by="total", ascending=True)['hour'], height=sum_hour_df.tail(5).sort_values(by="total", ascending=True)["total"], color=colors)
ax[1].set_ylabel(None)
ax[1].set_xlabel('Hour', fontsize=20)
ax[1].set_title("Lowest Bike Rent Time", loc="center", fontsize=25)
ax[1].tick_params(axis='y', labelsize=18)
ax[1].tick_params(axis='x', labelsize=18)

st.pyplot(fig)



st.subheader("Working Day and Off Day Bike Rent Ratio")


fig, ax = plt.subplots(figsize=(12,8))

ax.pie(
    x = [work_holiday_ratio[(work_holiday_ratio['classify_day']=="work")]["casual"].sum(), 
         work_holiday_ratio[(work_holiday_ratio['classify_day']=='work')]['registered'].sum(),
         work_holiday_ratio[(work_holiday_ratio['classify_day']=="off")]["casual"].sum(), 
         work_holiday_ratio[(work_holiday_ratio['classify_day']=='off')]['registered'].sum()],
    labels = ['work casual', 'work registered', 'off casual', 'off registered'],
    colors=["#80CFE8", "#69A9BE", "#CDCDCD", "#B8B7B7"], autopct='%1.1f%%', textprops={'fontsize':10}) 

st.pyplot(fig)


fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 8))

ax[0].pie(
    x = [work_holiday_ratio[(work_holiday_ratio['classify_day']=="work")]["casual"].sum(), 
         work_holiday_ratio[(work_holiday_ratio['classify_day']=='work')]['registered'].sum()],
    labels = ['casual', 'registered'], colors=["#80CFE8", "#69A9BE"], autopct='%1.1f%%')
ax[0].set_title('Working Day Casual and Registered')

ax[1].pie(
    x = [work_holiday_ratio[(work_holiday_ratio['classify_day']=="off")]["casual"].sum(), 
         work_holiday_ratio[(work_holiday_ratio['classify_day']=='off')]['registered'].sum()],
    labels = ['casual', 'registered'], colors=["#CDCDCD", "#B8B7B7"], autopct='%1.1f%%')
ax[1].set_title('Off Day Casual and Registered')

st.pyplot(fig)
