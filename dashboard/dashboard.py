import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')


def create_monthly(df: pd.DataFrame) -> pd.DataFrame:
    monthly_rent_df = df.resample("M", on='dteday').agg(
        {'cnt': 'sum'}).rename(columns={'cnt': 'total'})
    monthly_rent_df['month'] = monthly_rent_df.index.strftime('%B')
    monthly_rent_df['year'] = monthly_rent_df.index.strftime('%Y')
    monthly_rent_df = monthly_rent_df.reset_index()
    monthly_rent_df.drop('dteday', axis=1, inplace=True)
    return monthly_rent_df


# Load data
all_df = pd.read_csv("all_data.csv")

all_df['dteday'] = pd.to_datetime(all_df['dteday'])
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()


with st.sidebar:
    st.title('Menu')

    input_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )


    print(input_date, 'dasd')
    if len(input_date) == 2:
        start_date = input_date[0]
        end_date = input_date[1]
        main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                    (all_df["dteday"] <= str(end_date))]
    else:
        main_df = all_df

monthly_rent_df = create_monthly(main_df)

st.header('bike sharing data')
st.subheader('Number of bicycle rentals in each month in 2011 and 2012')

sns.barplot(data=monthly_rent_df, x='month', y='total', hue='year')
plt.xticks(rotation=45)
st.pyplot(plt)

st.subheader('The season with the most renters')

col1, col2 = st.columns(2)

with col1:
    st.scatter_chart(data=main_df, x='temp', y='cnt', color='season')
with col2:
    st.bar_chart(data=main_df, x='season', y='cnt')
