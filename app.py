# Import needed packages 
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv(r"C:\Users\scott\Documents\GitHub\Py_Proj_repo\vehicles_us.csv")

# Function creations: 
# Will be passed to df's model column to only get the first word for the manufacterers
def get_manufact(model):
    return model.split(' ')[:1][0]

st.header('Project')

# Cleaning the dataset. Dropped is_4wd column has ~1/2 of it was missing. Converted dtype of columns
# to correct ones as well. 
df = df.drop('is_4wd', axis=1)
df['model_year'] = df['model_year'].where(df['model_year'].isna() == False, df['model_year'].mean())
df['cylinders'] = df['cylinders'].where(df['cylinders'].isna() == False, df['cylinders'].mean())
df['odometer'] = df['odometer'].where(df['odometer'].isna() == False, df['odometer'].mean())
df[['model_year', 'cylinders', 'odometer']] = df[['model_year', 'cylinders', 'odometer']].astype('int')
df['date_posted'] = pd.to_datetime(df['date_posted'], format='%Y-%m-%d')

st.write(df.sample(15))

st.write(px.histogram(df, x='model_year', y='price', histfunc='avg', color='condition', marginal='rug', hover_data=df.columns))

df['manufacterer'] = df['model'].apply(get_manufact)
st.write(px.histogram(df, x='manufacterer', color='type', marginal='rug', hover_data=df.columns))

st.write(px.scatter(df, x='odometer', y='price', color='condition'))


manu_list = sorted(df['manufacterer'].unique())
man1 = st.selectbox('Select first manufacterer',
    (manu_list)
)
man2 = st.selectbox('Select second manufacterer',
    (manu_list), 
    index = 1
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