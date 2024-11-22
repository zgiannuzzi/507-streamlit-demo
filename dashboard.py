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

#Create a new table 
plot = pd.pivot_table(df, values='student_count', index=['state'],
                       columns=['learning_modality'], aggfunc="sum")
plot = plot.reset_index()

#Seperate data by Learning type
learning_hybrid = df[df['learning_modality'] == 'Hybrid']
learning_person = df[df['learning_modality'] == 'In Person']
learning_remote = df[df['learning_modality'] == 'Remote']

st.subheader("Select one of the buttoms and it gives you a list and bar plot based off the button selected")

#Creates radio buttons to allow you select type of learning
status = st.radio("Select type of learning to see a general overview of specific learning type data: ", ('Hybrid','In Person','Remote'))
#Checks which radio button is selected and provides bar plot for the selection
if(status == 'Hybrid'):
    st.dataframe(learning_hybrid)
    st.bar_chart(plot,x = "state",y = "Hybrid")
elif(status == 'In Person'):
    st.dataframe(learning_person)
    st.bar_chart(plot,x = "state",y = "In Person")
else:
    st.dataframe(learning_remote)
    st.bar_chart(plot,x = "state",y = "Remote")
## line chart by week

st.subheader("Select one or more of the options and it builds a barplot based off type of Learning, Student count, and State")
#Creates mulitselect box
Learning = st.multiselect("Select the type of learning you wish to see relative to Student count and State : ",
                         ['Hybrid', 'In Person', 'Remote'])
#As long as an option is selected display a bar chart with the information
if(len(Learning) > 0):
    st.bar_chart(plot,x = "state",y = Learning) 


st.text("""I wanted to be able to create a barplot based of a range of student counts but I could not figure out how to get the types to match and plot them""")
#Started to try and add slider functionality but had no luck 
Student_count = st.slider(
    "Schedule your appointment:", value=(0, 25000000)
)
if(Student_count[0] > 0):
    plot2 = pd.pivot_table(df, values=(Student_count[0],Student_count[1]), index=['state'],
                       columns=['learning_modality'], aggfunc="sum")
    plot2 = plot2.reset_index()
    st.bar_chart(plot2,x = "state",y = Learning)
