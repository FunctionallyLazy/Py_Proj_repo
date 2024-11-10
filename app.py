import streamlit as st
import pandas as pd
import plotly.express as px

def get_manufact(model):
    return model.split(' ')[:1][0]

st.header('Project')
df = pd.read_csv(r"C:\Users\scott\Documents\GitHub\Py_Proj_repo\vehicles_us.csv")
st.write(px.histogram(df, x='model_year', y='price', histfunc='avg', color='condition', marginal='rug', hover_data=df.columns))

df['manufacterer'] = df['model'].apply(get_manufact)
st.write(px.histogram(df, x='manufacterer', color='type', marginal='rug', hover_data=df.columns))

st.write(px.scatter(df, x='odometer', y='price', color='condition'))


manu_list = df['manufacterer'].unique()
man1 = st.selectbox('Select first manufacterer',
    (manu_list)
)
man2 = st.selectbox('Select second manufacterer',
    (manu_list)
)
distNormalize = None
distNormalizeAgree = st.checkbox('Normalize')

if distNormalizeAgree:
    distNormalize = 'percent'
else:
    distNormalize = None


filtered_df = df.query("manufacterer == @man1 or manufacterer == @man2")
st.write(px.histogram(filtered_df, x='price',color='manufacterer', marginal='rug', histnorm=distNormalize, hover_data=df.columns))

st.write(px.box(df, x='fuel', y='days_listed', color='fuel'))