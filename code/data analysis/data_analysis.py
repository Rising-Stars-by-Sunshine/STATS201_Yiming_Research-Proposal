# -*- coding: utf-8 -*-
"""Data Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EiOV6f8YtB9a-EhkOMJPLavm6NkIdkfg
"""

!pip install pycountry-convert

!pip install sktime[all_extras]

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pycountry_convert as pc

from sktime.forecasting.base import ForecastingHorizon
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sktime.performance_metrics.forecasting import mean_squared_error
from sktime.forecasting.arima import AutoARIMA

from google.colab import drive
drive.mount('/content/drive')

"""## Data Info

Importing & showcasing the data
"""

df = pd.read_csv('global_data_on_sustainable_energy.csv')
df

df.info()

# Assuming 'data' is your DataFrame
for column in df.columns:
    if df[column].dtype == 'object':
        try:
            # Remove commas and convert to float
            df[column] = df[column].str.replace(',', '').astype(float)
        except ValueError:
            # If conversion fails, it's not a numerical column, so do nothing
            pass
df

df.info()

df.describe().T

#rename CO2
df.rename(columns={"Value_co2_emissions_kt_by_country":"CO2" , 'Land Area(Km2)':'Land'} , inplace=True)
df

#Data cleaning
df.dropna(subset=['Entity', 'Year'], inplace=True)  # Remove rows with missing 'Entity' or 'Year'
df.fillna(0, inplace=True)  # Fill other missing values with 0, you can adapt this based on the context
df



df2 = df

"""## CO2 Emission

Visualising CO2 emissions in respective countries. This part wil help us identify the significance of renewable energy.
"""

# Top 5 countries with highest CO2 emission
average_co2_emission_by_country = df.groupby('Entity')['CO2'].mean()
top_5_countries = average_co2_emission_by_country.nlargest(5)

plt.figure(figsize = (10, 6))
sns.barplot(x = top_5_countries.index, y = top_5_countries.values)
plt.xlabel('Country')
plt.ylabel('Average CO2 Emissions (kT x 1e6)')
plt.title('Top 5 Countries with Highest Average CO2 Emissions')

plt.xticks(rotation = 45, ha = 'center')

plt.tight_layout()
plt.show()

"""## Classification

I think I will firstly do a classification here, maybe by CNN. Then I can further research on the differences among regions.
"""

# Add a new column - "Continent", for classification by region
def country_to_continent(country_name):
    country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name

df['Continent'] = df['Entity'].apply(country_to_continent)
df.head(10)

# Creating an empty table df_energy_all with the necessary columns and data types
columns = ['Year', 'Asia', 'Europe', 'Africa', 'North America', 'South America', 'Oceania']
df_energy_all = pd.DataFrame(columns=columns)

# Creating a function to automatically calculate the average value for the continent for the year
def filter_and_calculate_mean(df, year, column_name):
    row_data = {'Year': year}
    for continent in columns[1:]:
        filtered_df = df[(df['Year'] == year) & (df['Continent'] == continent)]
        mean_value = filtered_df[column_name].mean()
        row_data[continent] = mean_value
    return row_data

column_name = 'Primary energy consumption per capita (kWh/person)'
data_to_concat = []

for year in range(2000, 2021):
    row_data = filter_and_calculate_mean(df, year, column_name)
    data_to_concat.append(row_data)

# Putting it all together
df_energy_all = pd.concat([df_energy_all, pd.DataFrame(data_to_concat)], ignore_index=True)

df_energy_all['Year'] = df_energy_all['Year'].astype('int64')

# Displaying the df_energy_all table for review
display(df_energy_all)

df_energy_cons_melted = pd.melt(df_energy_all, id_vars='Year', var_name='Region', value_name='Energy Consumption')

# Building a graph
plt.figure(figsize=(10, 6))
sns.set(style='whitegrid')
palette = sns.color_palette("husl", len(df_energy_cons_melted['Region'].unique()))

plot = sns.lineplot(data=df_energy_cons_melted, x='Year', y='Energy Consumption', hue='Region', palette=palette)

# Adding names to the graph
plt.xlabel('Year', fontweight='bold')
plt.ylabel('Energy Consumption (kWh/person)', fontweight='bold')
plt.title('Energy Consumption per Capita by Region (2000 - 2020)', fontweight='bold')
plt.legend(title='Region')
plt.margins(x=0)

# Adjust the placement of captions on the x-axis and change the date format
years = range(2000, 2021)
plot.set_xticks(years)
plot.set_xticklabels([str(year) for year in years], rotation=45)

plt.show()

"""The above graph clearly shows the trends in per capita egergy consumption by continent. The graphs are quite different from each other.

Top continents in terms of energy consumption:

1. Europe
2. Asia
3. North America
4. Oceania
5. South America
6. Oceania

The graph shows that energy consumption per capita in Oceania and Africa remained almost unchanged between 2000 and 2020. In addition, it is noticeable that from 2019 to 2020, all graphs begin to fall, so energy consumption per capita has generally decreased for all continents.

It is worth emphasizing that the lowest rates in Africa can be explained by the overall low level of industrialization and rather low living standards of the population in general, respectively, the availability of goods, and energy is such a good, is rather limited. Europe, in turn, has the highest rates, which is quite expected, however, it can be seen that since 2008 the amount of energy consumption per capita has been gradually decreasing, while the countries of Asia have moderately increasing rates, and perhaps soon they will have the highest rates, thereby overtaking the countries of Europe

## Inicator Correlation
"""

# Convert columns to numeric if they're not already
df2['Renewable energy share in the total final energy consumption (%)'] = pd.to_numeric(df2['Renewable energy share in the total final energy consumption (%)'], errors='coerce')
df2['Primary energy consumption per capita (kWh/person)'] = pd.to_numeric(df2['Primary energy consumption per capita (kWh/person)'], errors='coerce')

# Calculate the product and add as a new column
df2['Renewable energy consumption per capita'] = df2['Renewable energy share in the total final energy consumption (%)'] * df2['Primary energy consumption per capita (kWh/person)']
df2

"""### Animation on World Map"""

# Function to plot features on world map
def plot_world_map(column_name):
    fig = go.Figure()
    for year in range(2000, 2021):
        # Filter the data for the current year
        filtered_df2 = df2[df2['Year'] == year]

        # Create a choropleth trace for the current year
        trace = go.Choropleth(
            locations=filtered_df2['Entity'],
            z=filtered_df2[column_name],
            locationmode='country names',
            colorscale='Electric',  # Use a different color scale for better contrast
            colorbar=dict(title=column_name),
            zmin=df2[column_name].min(),
            zmax=df2[column_name].max(),
            visible=False  # Set the trace to invisible initially
        )

        # Add the trace to the figure
        fig.add_trace(trace)

    # Set the first trace to visible
    fig.data[0].visible = True

    # Create animation steps
    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method='update',
            args=[{'visible': [False] * len(fig.data)},  # Set all traces to invisible
                  {'title_text': f'{column_name} Map - {2000 + i}', 'frame': {'duration': 1000, 'redraw': True}}],
            label=str(2000 + i)  # Set the label for each step
        )
        step['args'][0]['visible'][i] = True  # Set the current trace to visible
        steps.append(step)

    # Create the slider
    sliders = [dict(
        active=0,
        steps=steps,
        currentvalue={"prefix": "Year: ", "font": {"size": 14}},  # Increase font size for slider label
    )]

    # Update the layout of the figure with increased size and change the template
    fig.update_layout(
        title_text=f'{column_name} Map with slider',  # Set the initial title
        title_font_size=24,  # Increase title font size
        title_x=0.5,  # Center the title
        geo=dict(
            showframe=True,
            showcoastlines=False,
            projection_type='natural earth'
        ),
        sliders=sliders,
        height=500,  # Set the height of the figure in pixels
        width=1000,  # Set the width of the figure in pixels
        font=dict(family='Arial', size=12),  # Customize font family and size for the whole figure
        margin=dict(t=80, l=50, r=50, b=50),  # Add margin for better layout spacing
        # Change the template to 'plotly_dark'
    )

    # Show the figure
    fig.show()

plot_world_map('Renewable energy consumption per capita')

euro_data = df2.query("Continent == 'Europe'")

euro_data = euro_data.drop(['Year', 'Entity','Continent'], axis=1)
euro_data

"""### Heatmap"""

plt.figure(figsize=(10, 8))
sns.heatmap(euro_data.corr(), annot=True, fmt=".1f", linewidths=.5, cmap='coolwarm')
plt.show()

Corr_Matrix = euro_data.corr()
# Taking the absolute values of the correlation coefficients
abs_corr = Corr_Matrix['Renewable energy consumption per capita'].abs()

print('Top 8 Features Most Correlated (by absolute value) to Renewable energy consumption per capita')
# Sorting by absolute values and taking the top 8
top_8 = abs_corr.sort_values(ascending=False).head(8)
print(top_8)

"""### Scatterplot"""

# Renewable Share vs GDP Growth
plt.figure(figsize=(10,6))
sns.regplot(x='Renewables (% equivalent primary energy)', y='Renewable energy consumption per capita', data=df, scatter_kws={'alpha':0.3})
plt.title('', size=15)
plt.xlabel('Renewable')
plt.ylabel('Renewable energy consumption')

plt.figure(figsize=(10,6))
sns.regplot(x='Low-carbon electricity (% electricity)', y='Renewable energy consumption per capita', data=df, scatter_kws={'alpha':0.3})
plt.title('', size=15)
plt.xlabel('Low-carbon electricity')
plt.ylabel('Renewable energy consumption')

plt.figure(figsize=(10,6))
sns.regplot(x='Latitude', y='Renewable energy consumption per capita', data=df, scatter_kws={'alpha':0.3})
plt.title('', size=15)
plt.xlabel('Latitude')
plt.ylabel('Renewable energy consumption')

plt.figure(figsize=(10,6))
sns.regplot(x='Energy intensity level of primary energy (MJ/$2017 PPP GDP)', y='Renewable energy consumption per capita', data=df, scatter_kws={'alpha':0.3})
plt.title('', size=15)
plt.xlabel('Energy intensity level of primary energy (MJ/$2017 PPP GDP)')
plt.ylabel('Renewable energy consumption')

plt.figure(figsize=(10,6))
sns.regplot(x='Access to electricity (% of population)', y='Renewable energy consumption per capita', data=df, scatter_kws={'alpha':0.3})
plt.title('', size=15)
plt.xlabel('Access to electricity')
plt.ylabel('Renewable energy consumption')

"""## Prediction"""

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression

target = 'Renewable energy consumption per capita'

features = ['Renewables (% equivalent primary energy)',
'Latitude',
'Energy intensity level of primary energy (MJ/$2017 PPP GDP)',
'Low-carbon electricity (% electricity)',
'Longitude']

x = euro_data[features]
y = euro_data[target]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)

"""### Linear Regression"""

linear_regression_model = LinearRegression()
linear_regression_model.fit(x_train, y_train)

linreg_predictions = linear_regression_model.predict(x_test)

lr_mse = mean_squared_error(y_test, linreg_predictions)

lr_r2 = r2_score(y_test, linreg_predictions)

result1 = pd.DataFrame({
    'Model': ['Linear Regression'],
    'MSE': [lr_mse],
    'R-squared': [lr_r2]
})
result1

"""### Random Forest"""

rf_param_grid = {'n_estimators': [100, 300, 500], 'max_depth': [None, 10, 20], 'min_samples_split': [2, 5, 10]}
rf_model = RandomForestRegressor(random_state=42)
rf_grid_search = GridSearchCV(estimator=rf_model, param_grid=rf_param_grid, scoring='neg_mean_squared_error', cv=5)
rf_grid_search.fit(x_train, y_train)
best_rf_params = rf_grid_search.best_params_

random_forest_model = RandomForestRegressor(**best_rf_params, random_state=42)

random_forest_model.fit(x_train, y_train)

rforest_predictions = random_forest_model.predict(x_test)

rf_mse = mean_squared_error(y_test, rforest_predictions)

rf_r2 = r2_score(y_test, rforest_predictions)

result2 = pd.DataFrame({
    'Model': ['Random Forest'],
    'MSE': [rf_mse],
    'R-squared': [rf_r2]
})
result2

"""### Gradient Boosting"""

gb_param_grid = {'n_estimators': [100, 300, 500], 'max_depth': [3, 5, 7], 'learning_rate': [0.01, 0.1, 0.2]}
gb_model = GradientBoostingRegressor(random_state=42)
gb_grid_search = GridSearchCV(estimator=gb_model, param_grid=gb_param_grid, scoring='neg_mean_squared_error', cv=5)
gb_grid_search.fit(x_train, y_train)
best_gb_params = gb_grid_search.best_params_

gradient_boosting_model = GradientBoostingRegressor(**best_gb_params, random_state=42)

gradient_boosting_model.fit(x_train, y_train)

gradboost_predictions = gradient_boosting_model.predict(x_test)

gb_mse = mean_squared_error(y_test, gradboost_predictions)

gb_r2 = r2_score(y_test, gradboost_predictions)

result3= pd.DataFrame({
    'Model': ['Gradient Boosting'],
    'MSE': [gb_mse],
    'R-squared': [gb_r2]
})
result3