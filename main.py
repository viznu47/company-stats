import streamlit as st
st.set_page_config(page_title="Company stats", layout="wide", page_icon="📊")
import pandas as pd
import plotly.express as px
import altair as alt
import plotly.graph_objects as go
st.subheader("Company stats visualization using Streamlit by Viznu")


# query 1
st.text("1. Based on the sector display the number of companies")
df1 = pd.read_csv(r"C:\Users\Vishnu\Downloads\viznu\viznu\query1.csv")
t1,t2 = st.tabs(["Chart","Data"])
with t1:
    fig = px.bar(df1, x="no_of_companies", y="COMPANY_CLASS", orientation="h")      
    fig.update_traces(text=df1['no_of_companies'], textposition='outside')
    fig.update_layout(   
    xaxis_title="No.of companies",
    yaxis_title="Class") 
    st.plotly_chart(fig, use_container_width=True)
    
t2.dataframe(df1)


# query 2
st.text("2. List the number of companies that had been registered in each decade")
df2 = pd.read_csv(r"C:\Users\Vishnu\Downloads\viznu\viznu\query2.csv")

df2 = df2.drop([19,20], axis=0)
t1,t2 = st.tabs(["Chart","Data"])
with t1:
    fig = px.bar(df2, x="decade", y="count",
                 range_x=[1850, 2023])
    fig.update_xaxes(dtick=10)
    fig.update_traces(text=df2['count'], textposition='outside')
    st.plotly_chart(fig, use_container_width=True)
    
t2.dataframe(df2)


# query 3
st.text("3. Find top 5 companies with highest paid up capital as a list in each leap year after 2000")
df3 = pd.read_csv(r"C:\Users\Vishnu\Downloads\viznu\viznu\query3.csv")
df3.drop([47,48], axis=0, inplace=True)
df3 = df3.drop(['rank'], axis=1)

t1,t2 = st.tabs(["Chart","Data"])
t2.dataframe(df3)

with t1:
    fig = px.bar(df3, x="COMPANY_NAME", y="PAIDUP_CAPITAL", 
    animation_frame="year", range_y=[df3["PAIDUP_CAPITAL"].min(),df3["PAIDUP_CAPITAL"].max()])
    fig.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig, height=1000, use_container_width=True)
    
    fig = px.bar(df3, x="year", y="PAIDUP_CAPITAL", color="COMPANY_NAME" ,range_y=[df3["PAIDUP_CAPITAL"].min(),df3["PAIDUP_CAPITAL"].max()], 
                 range_x=[2000,2023], barmode="overlay")
    fig.update_layout(xaxis_tickangle=45)
    fig.update_xaxes(dtick=4)
    st.plotly_chart(fig, height=1000, use_container_width=True)


# query 4
st.text("4. Find top 5 companies that has highest paid up capital in each state")
df4 = pd.read_csv(r"C:\Users\Vishnu\Downloads\viznu\viznu\query4.csv")
df4 = df4.drop(["corporate_identification_number","rank"], axis=1)

exp = st.expander("Data")
exp.dataframe(df4)

stacked_bar_data = df4.groupby(['registered_state', 'paidup_capital']).size().reset_index(name='Count')
stacked_bar_chart = alt.Chart(df4).mark_bar().encode(
    x='registered_state',
    y='paidup_capital',
    color='company_name',
    # tooltip=['registered_state', 'paidup_capital', 'company_name']
).properties(
    height=800,
    title='Distribution of Companies by Registered State and Paid-up Capital')
st.altair_chart(stacked_bar_chart, use_container_width=True)

states = df4["registered_state"].unique()
ch  = st.selectbox("Select your state", states)
for state in states:
    if ch == state:
        t1,t2 = st.tabs(["Chart","Data"])
        with t1:
            state_df = df4.loc[df4["registered_state"] == f"{state}"]
            fig = px.bar(state_df, x="company_name", y="paidup_capital", color="company_name", title=f"Top five companies with highest capital in {state}")
            fig.update_layout(height=700)
            st.plotly_chart(fig, use_container_width=True)
            
        with t2:
            st.write(f"Dataframe for {state}:")
            st.dataframe(state_df)


# query 5
st.text("5. Which state has highest companies registered?")
df5 = pd.read_csv(r"C:\Users\Vishnu\Downloads\viznu\viznu\query5.csv")
t1,t2 = st.tabs(["Chart","Data"])
with t1:
    fig = px.bar(df5, x="REGISTERED_STATE", y="no_of_companies", title="Number of companies in each state", color="REGISTERED_STATE")
    fig.update_layout(  
    xaxis_tickangle=60, 
    xaxis_title="Registered states",
    yaxis_title="Companies count",
     height=900)
    st.plotly_chart(fig, use_container_width=True)

    
with t2:
    st.dataframe(df5)


# query 6
st.text("6. Find the year on which each state has their maximum registration")
df6 = pd.read_csv(r"C:\Users\Vishnu\Downloads\viznu\viznu\query6.csv")
t1,t2 = st.tabs(["Chart","Data"])

with t1:

    fig = px.bar(df6, x="REGISTERED_STATE", y="year", color="count", range_y=[1980,2023], color_continuous_scale='viridis', height=700, width=1000)
    fig.update_layout(xaxis_tickangle=60, xaxis_title="States",yaxis_title="Years")

    # fig.update_xaxes(dtick=5)
    st.plotly_chart(fig, use_container_width=True)

with t2:
    st.dataframe(df6)

# query 7
st.text("7. Find the sector that is most common in each state")
df7 = pd.read_csv(r"C:\Users\Vishnu\Downloads\viznu\viznu\myquery7.csv")
df7 = df7.dropna()
df7 = df7.drop(['rank'], axis=1)
st.dataframe(df7)
states = df7['registered_state'].unique()

ch  = st.selectbox("Select your state", states)
for state in states:
    if ch == state:
        t1,t2 = st.tabs(["Chart","Data"])
        with t1:
            state_df = df7.loc[df7["registered_state"] == f"{state}"]
            
            fig = px.pie(state_df, values="no_of_companies", names="company_class", height=600)
            st.plotly_chart(fig, use_container_width=True)

             # donut chart   
            # fig = go.Figure(data=[go.Pie(labels=state_df["company_class"], values=state_df["no_of_companies"], hole=.3)])
            # st.plotly_chart(fig)
            
        with t2:
            st.write(f"Dataframe for {state}:")
            st.dataframe(state_df)


# query 8
st.text("8. Based on sub_category give the count for companies in each state")
df8 = pd.read_csv(r"C:\Users\Vishnu\Downloads\viznu\viznu\query8.csv")
states = df8['REGISTERED_STATE'].unique()

ch  = st.selectbox("Select your state", states, key="state_select" )
for state in states:
    if ch == state:
        t1,t2 = st.tabs(["Chart","Data"])
        with t1:
            state_df = df8.loc[df8["REGISTERED_STATE"] == f"{state}"]
            
            fig = px.bar(state_df, x="COMPANY_SUB_CATEGORY", y="category_count", color_discrete_sequence=["blue", "green", "red", "yellow","purple"] ,height=600, color="COMPANY_SUB_CATEGORY")
            fig.update_traces(text=state_df['category_count'], textposition='outside')
            fig.update_layout( xaxis_title="Category",yaxis_title="Count", xaxis_showticklabels=False)
            st.plotly_chart(fig, use_container_width=True)

        with t2:
            st.write(f"Dataframe for {state}:") 
            st.dataframe(state_df)

# query 9
st.text("9. List the companies that have been recently enrolled in each state")
df9 = pd.read_csv(r"C:\Users\Vishnu\Downloads\viznu\viznu\query9.csv")
df9 = df9.drop(["rank", "corporate_identification_number"], axis=1)

ch  = st.selectbox("Select your state", states, key="state_select_2")
for state in states:
    if ch == state:
        t1,t2 = st.tabs(["Chart","Data"])
        with t1:
            state_df = df9.loc[df9["registered_state"] == f"{state}"]
            
            fig = px.scatter(state_df, x="company_name", y="date",color="company_name" , height=600, )
            fig.update_traces(marker_size=12, marker_symbol='diamond', marker_line_color='white')
            fig.update_layout(xaxis_tickangle=60 , xaxis_title="Company", yaxis_title="Date", xaxis_showticklabels=False )
            st.plotly_chart(fig, use_container_width=True)

        with t2:
            st.write(f"Dataframe for {state}:") 
            st.dataframe(state_df)

# query 10
st.text("10. Find the count of companies per company_status")
df10 = pd.read_csv(r"C:\Users\Vishnu\Downloads\viznu\viznu\query10.csv")
t1,t2 =  st.tabs(["Chart", "Data"])

with t1:
    fig = px.bar(df10, x="COMPANY_STATUS", y="count", height=600, color="COMPANY_STATUS")
    fig.update_layout(xaxis_tickangle=60 , xaxis_title="Company Status", yaxis_title="Number of companies")
    fig.update_traces(text=df10['count'], textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

with t2:
    st.dataframe(df10)


# query 11
st.text("11. Find the top 2 companies per principal business activity in 19th century")
df11 = pd.read_csv(r"C:\Users\Vishnu\Downloads\viznu\viznu\query11.csv")
t1,t2 =  st.tabs(["Chart", "Data"])
with t1:
    fig = px.bar(df11, x="PRINCIPAL_BUSINESS_ACTIVITY_AS_PER_CIN", y="PAIDUP_CAPITAL", color="COMPANY_NAME", barmode="overlay", height=800)

    fig.update_layout(  
        xaxis_tickangle=30, 
        xaxis_title="Principal amount",
        yaxis_title="Paid-up capital",
        legend=dict(
            font=dict(size=10),  
            yanchor="top",       
            xanchor="left",
        )
    )
    st.plotly_chart(fig, use_container_width=True)

t2.dataframe(df11)


# query 12
st.text("12. Find the company with higest paidup capital in each decade")
df12 = pd.read_csv(r"C:\Users\Vishnu\Downloads\viznu\viznu\query12.csv")
df12 = df12.drop([18,19], axis=0)
t1,t2 =  st.tabs(["Chart", "Data"])

with t1:
    fig = px.bar(df12, x="decade", y="PAIDUP_CAPITAL", color="COMPANY_NAME")
    st.plotly_chart(fig, use_container_width=True)

t2.dataframe(df12)