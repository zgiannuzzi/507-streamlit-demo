import streamlit as st
import pandas as pd

st.header("2024 AHI 507 Streamlit Example")
st.subheader("We are going to go through a couple different examples of loading and visualization information into this dashboard")

st.text("""In this streamlit dashboard, we are going to focus on some recently released school learning modalities data from the NCES, for the years of 2021.""")

# ## https://healthdata.gov/National/School-Learning-Modalities-2020-2021/a8v3-a3m3/about_data
df = pd.read_csv("https://healthdata.gov/resource/a8v3-a3m3.csv?$limit=50000") ## first 1k 

## data cleaning 
df['week_recoded'] = pd.to_datetime(df['week'])
df['zip_code'] = df['zip_code'].astype(str)

df['week'].value_counts()

## box to show how many rows and columns of data we have: 
col1, col2, col3 = st.columns(3)
col1.metric("Columns", df.shape[1]) 
col2.metric("Rows", len(df))
col3.metric("Number of unique districts/schools:", df['district_name'].nunique())

## exposing first 1k of NCES 20-21 data
st.dataframe(df)



table = pd.pivot_table(df, values='student_count', index=['week'],
                       columns=['learning_modality'], aggfunc="sum")

table = table.reset_index()
#table.columns

table2 = pd.pivot_table(df, values='student_count', index=['state'],
                       columns=['learning_modality'], aggfunc="sum")
table2 = table.reset_index()

learning_hybrid = df[df['learning_modality'] == 'Hybrid']
learning_person = df[df['learning_modality'] == 'In Person']
learning_remote = df[df['learning_modality'] == 'Remote']

status = st.radio("Select type of learning: ", ('Hybrid','In Person','Remote'))
if(status == 'Hybrid'):
    st.dataframe(learning_hybrid)
    st.bar_chart(table2,x = "State",Y = "Hybrid")
elif(status == 'In Person'):
    st.dataframe(learning_person)
else:
    st.dataframe(learning_remote)
## line chart by week


Learning = st.multiselect("Type of learning: ",
                         ['Hybrid', 'In Person', 'Remote'])

""" 
st.bar_chart(
    table,
    x="week",
    y="Hybrid",
)

st.bar_chart(
    table,
    x="week",
    y="In Person",
)

st.bar_chart(
    table,
    x="week",
    y="Remote",
)
"""