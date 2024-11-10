import streamlit as st
import pandas as pd
import plotly.express as px
st.header('Project')
df = pd.read_csv(r"C:\Users\scott\Documents\GitHub\Py_Proj_repo\vehicles_us.csv")
st.write(px.histogram(df, x='model_year', y='price', histfunc='avg', color='condition', marginal='rug', hover_data=df.columns))
