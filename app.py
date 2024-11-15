# Import needed packages 
import streamlit as st
import os
import pandas as pd
import plotly.express as px

# Was having issues just passing "vehicles_us.csv" to read_csv method along with other variants. 
# This was the only method that worked locally and when pushing to render
file_path = os.path.join(os.path.dirname(__file__), "vehicles_us.csv")
df = pd.read_csv(file_path)

# Function creations: 
# Will be passed to df's model column to only get the first word for the manufacterers
def get_manufact(model):
    return model.split(' ')[:1][0]

st.header('Sprint 4 Project - Vehicle Dataset Analysis')


# Cleaning the dataset. Dropped is_4wd column has ~1/2 of it was missing. Converted dtype of columns
# to correct ones as well. 
df = df.drop('is_4wd', axis=1)
df['model_year'] = df['model_year'].where(df['model_year'].isna() == False, df['model_year'].mean())
df['cylinders'] = df['cylinders'].where(df['cylinders'].isna() == False, df['cylinders'].mean())
df['odometer'] = df['odometer'].where(df['odometer'].isna() == False, df['odometer'].mean())
df[['model_year', 'cylinders', 'odometer']] = df[['model_year', 'cylinders', 'odometer']].astype('int')
df['date_posted'] = pd.to_datetime(df['date_posted'], format='%Y-%m-%d')

st.write('Sample of the dataset')
st.write(df.sample(15))

# Hist of Condition vs Model year measured by the avg prices 
st.write('Condition vs Model year by average prices')
st.write(px.histogram(df, x='model_year', y='price', histfunc='avg', color='condition', marginal='rug', hover_data=df.columns))

# Creating the manufacterer column referencing the above function get_manufact() 
# then creating a hist of the types per manufacterer
st.write('Vehicle type count per manufacterer')
df['manufacterer'] = df['model'].apply(get_manufact)
st.write(px.histogram(df, x='manufacterer', color='type', marginal='rug', hover_data=df.columns))

# Scatterplot of odometer and price. Slider to set max odometer value (in thousandths)
st.write('Correlation between Odometer and Price')
scatter_x_max = st.slider('Max odometer value (thousands)', 1,1000, 500)
fig = px.scatter(df, x='odometer', y='price', color='condition')
fig.update_layout(xaxis=dict(range=[0,scatter_x_max*1000]))
st.write(fig)

# Alphabetically sorted list of manufacterers
manu_list = sorted(df['manufacterer'].unique())

# Dropdowns for future reference in manufacterer x price hist
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

# Filtering initial df into seperate df with only the selected manufacterers 
filtered_df = df.query("manufacterer == @man1 or manufacterer == @man2")
st.write('Vehicle Price distribution comparison by manufacterers')
st.write(px.histogram(filtered_df, x='price',color='manufacterer', marginal='rug', histnorm=distNormalize, hover_data=df.columns))

# Boxplot of fuel x days_listed to show each fuel types quartiles and outliers 
st.write('Fuel type across days listed')
st.write(px.box(df, x='fuel', y='days_listed', color='fuel'))