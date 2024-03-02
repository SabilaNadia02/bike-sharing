import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_daily_rent(df):
    daily_rent_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    daily_rent_df = daily_rent_df.reset_index()
    daily_rent_df.rename(columns={
        "instant": "rent_count",
        "casual": "total_casual",
        "registered": "total_registered",
        "cnt": "total_count"
    }, inplace=True)
    
    return daily_rent_df    

def plot_chart1():
    fig, ax = plt.subplots(figsize=(16,8))
    sns.barplot(x='mnth', y='cnt', data=main_df, hue='yr', ax=ax)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Sewa Sepeda")
    return fig

def plot_chart2():
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x='season', y='cnt', data=main_df, hue='yr', ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Sewa Sepeda")
    return fig

def plot_chart3():
    fig, ax = plt.subplots(figsize=(12,6))
    sns.lineplot(x="hr", y="cnt", data=main_df2, err_style=None, hue='yr', ax=ax)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Sewa Sepeda")
    return fig
    
#Load data
data_main = pd.read_csv("https://raw.githubusercontent.com/SabilaNadia02/bike-sharing/main/data/day.csv")
data_main2 = pd.read_csv("https://raw.githubusercontent.com/SabilaNadia02/bike-sharing/main/data/hour.csv")

datetime_columns = ["dteday"]
data_main.sort_values(by="dteday", inplace=True)
data_main.reset_index(inplace=True)

for column in datetime_columns:
    data_main[column] = pd.to_datetime(data_main[column])

# Filter data
min_date = data_main["dteday"].min()
max_date = data_main["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://www.touristengland.com/wp-content/uploads/2018/08/Boris-Bikes.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = data_main[(data_main["dteday"] >= str(start_date)) & 
                (data_main["dteday"] <= str(end_date))]

main_df2 = data_main2[(data_main2["dteday"] >= str(start_date)) & 
                (data_main2["dteday"] <= str(end_date))]


# # Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent(main_df)

# User Interface
st.title('Bike Rent Dashboard')
st.subheader('Cycle Through Life: Rent Your Ride Today!')

col1, col2, col3 = st.columns(3)

with col1:
    total_casual = daily_rent_df.total_casual.sum()
    st.metric("Total Casual", value=total_casual)
    
with col2:
    total_registered = daily_rent_df.total_registered.sum()
    st.metric("Total Registered", value=total_registered)
    
with col3:
    total_count = daily_rent_df.total_count.sum()
    st.metric("Total Count", value=total_count)

# Jumlah sewa sepeda per bulan
def main():
    st.subheader("Jumlah Sewa Sepeda per Bulan")
    fig = plot_chart1()
    st.pyplot(fig)

if __name__ == "__main__":
    main()

col1, col2 = st.columns(2)

with col1:
    # Jumlah sewa sepeda per musim
    def main():
        st.subheader("Jumlah Sewa Sepeda per Musim")
        fig = plot_chart2()
        st.pyplot(fig)

    if __name__ == "__main__":
        main()

with col2:
    # Jumlah sewa sepeda berdasarkan jam
    def main():
        st.subheader("Jumlah Sewa Sepeda Harian Berdasarkan Jam")
        fig = plot_chart3()
        st.pyplot(fig)

    if __name__ == "__main__":
        main()

col1, col2 = st.columns(2)

with col1:
    # Rata jumlah sewa per minggu
    weekday_counts = main_df.groupby('weekday', observed=True)['cnt'].mean().reset_index().sort_values("cnt")

    st.subheader("Rata-Rata Jumlah Sewa per Minggu")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='weekday', y='cnt', data=weekday_counts, ax=ax)
    ax.set_xlabel("Minggu")
    ax.set_ylabel("Rata-Rata Sewa Sepeda")
    st.pyplot(fig)
    
with col2:
    # Rata jumlah sewa berdasarkan hari kerja
    workingday_counts = main_df.groupby('workingday', observed=True)['cnt'].mean().reset_index().sort_values("cnt")

    st.subheader("Rata-Rata Jumlah Sewa berdasarkan Hari Kerja")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x='workingday', y='cnt', data=workingday_counts, ax=ax)
    ax.set_xlabel("Hari Kerja")
    ax.set_ylabel("Rata-Rata Sewa Sepeda")
    st.pyplot(fig)
