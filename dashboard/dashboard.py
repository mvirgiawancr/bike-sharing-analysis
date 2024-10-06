import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    perday_df = pd.read_csv('./main_data.csv')
    perday_df['dteday'] = pd.to_datetime(perday_df['dteday'])
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    perday_df['season_name'] = perday_df['season'].map(season_map)
    return perday_df

perday_df = load_data()


st.title('Bike Rental Analysis Dashboard')


st.sidebar.header('Filters')
year_filter = st.sidebar.selectbox('Select Year', ['All'] + sorted(perday_df['dteday'].dt.year.unique().tolist()))
season_filter = st.sidebar.multiselect('Select Season', perday_df['season_name'].unique())


if year_filter != 'All':
    filtered_df = perday_df[perday_df['dteday'].dt.year == year_filter]
else:
    filtered_df = perday_df

if season_filter:
    filtered_df = filtered_df[filtered_df['season_name'].isin(season_filter)]

st.header('Key Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Total Rentals", f"{filtered_df['cnt'].sum():,}")
col2.metric("Average Daily Rentals", f"{filtered_df['cnt'].mean():.2f}")
col3.metric("Highest Rental Day", filtered_df.loc[filtered_df['cnt'].idxmax(), 'dteday'].strftime('%Y-%m-%d'))


st.header('Monthly Rentals')
monthly_rentals = filtered_df.groupby(filtered_df['dteday'].dt.strftime('%B'))['cnt'].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(12, 6))
monthly_rentals.plot(kind='bar', ax=ax)
plt.title('Total Rentals by Month')
plt.ylabel('Total Rentals')
plt.xticks(rotation=45)
st.pyplot(fig)


st.header('Weekday vs Weekend Rentals')
weekday_rentals = filtered_df[filtered_df['weekday'] < 5]['cnt'].sum()
weekend_rentals = filtered_df[filtered_df['weekday'] >= 5]['cnt'].sum()
fig, ax = plt.subplots()
ax.pie([weekday_rentals, weekend_rentals], labels=['Weekday', 'Weekend'], autopct='%1.1f%%')
plt.title('Weekday vs Weekend Rentals')
st.pyplot(fig)


st.header('Seasonal Rental Performance')
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='season_name', y='cnt', data=filtered_df, order=['Spring', 'Summer', 'Fall', 'Winter'], ax=ax)
plt.title('Rental Performance by Season')
plt.xlabel('Season')
plt.ylabel('Number of Rentals')
st.pyplot(fig)


st.header('Daily Rental Trend')
daily_trend = filtered_df.set_index('dteday')['cnt']
fig, ax = plt.subplots(figsize=(12, 6))
daily_trend.plot(ax=ax)
plt.title('Daily Rental Trend')
plt.xlabel('Date')
plt.ylabel('Number of Rentals')
st.pyplot(fig)