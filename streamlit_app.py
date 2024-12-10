import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt

# %%
# Set the title and favicon that appear in the Browser's tab bar.
# st.set_page_config(
#     page_title='Analyst Phone Stats 2024',
#     page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
# )

# -----------------------------------------------------------------------------
# Declare some useful functions.

# @st.cache_data
# Get GDP Data creates dataframe for our csv and organizes it for manipulation
def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """
    months = ['Jan-24', 'Feb-24', 'Mar-24', 'Apr-24', 'May-24', 'Jun-24', 
          'Jul-24', 'Aug-24', 'Sep-24', 'Oct-24']
    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    # Read data with pandas
    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    PHONE_STATS_FILENAME = Path(__file__).parent/'data/phonestats.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)
    raw_phone_stats_df = pd.read_csv(PHONE_STATS_FILENAME, header=[0,2])

    MIN_YEAR = 1960
    MAX_YEAR = 2022
    MIN_PHONE_PERCENT = 60
    MAX_PHONE_PERCENT = 95
    MIN_READY_PERCENT = 60
    MAX_READY_PERCENT = 90

    # pivots all those year-columns into two: Year and GDP
    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )

    # Convert years from string to integers
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])

    return gdp_df

# gdp_df = get_gdp_data()
# print("GDP PDF here", gdp_df)

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# Analyst Dashboard

Browse through analyst performance statistics from 2024.
'''

# Add some spacing
''
''
PHONE_STATS_FILENAME = Path(__file__).parent/'data/phonestats.csv'
file_path = "phonestats.csv"
months = ['Jan-24', 'Feb-24', 'Mar-24', 'Apr-24', 'May-24', 'Jun-24', 
          'Jul-24', 'Aug-24', 'Sep-24', 'Oct-24']

# Our defined headers are the top row (Months) + 3rd Row (Absence, tardies, answered calls, not ready %)
df = pd.read_csv(PHONE_STATS_FILENAME, header=[0,2])
# Will consist of dataframes for each respective month
st.write("Aggregate Data Frame")
st.write(df)



# Establish a pre-determined minimum + maximum value based on dataset.
# min_value = gdp_df['Year'].min()
# max_value = gdp_df['Year'].max()
# # Creates slider element on DOM
# from_year, to_year = st.slider(
#     'Which years are you interested in?',
#     min_value=min_value,
#     max_value=max_value,
#     value=[min_value, max_value])
# # Grabs all UNIQUE countries from dataset
# countries = gdp_df['Country Code'].unique()
# # If there is no countries array
# if not len(countries):
#     st.warning("Select at least one country")

# # A multiselect DOM component for selecting countries
# selected_countries = st.multiselect(
#     'Which countries would you like to view?',
#     countries,
#     ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'])

''
''
''

# Filter the data. This will create a new dataframe among our original dataset that meets the following conditions: Is among the selected countries + greater than FROM year + less than TO year
# filtered_gdp_df = gdp_df[
#     (gdp_df['Country Code'].isin(selected_countries)) # Multi Select + Country Code Col Comparison
#     & (gdp_df['Year'] <= to_year) # All years less than the to_year
#     & (from_year <= gdp_df['Year']) # All years greater than the from year
# ]
# # Header H1 Element
month_data = {}
for month in months:
    month_data[month] = df[month]
st.header('Section 1', divider='gray')
def produce_altair_chart(df):
    c = (
    alt.Chart(df)
    .mark_circle()
    .encode(x="Answered Call %", y="Not Ready %", tooltip=["Answered Call %", "Not Ready %"])
    )
    return st.altair_chart(c, use_container_width=True)
tab_months = ['jan_tab', 'feb_tab', 'mar_tab', 'apr_tab', 'may_tab', 'jun_tab', 'jul_tab', 'aug_tab', 'sep_tab', 'oct_tab']
# Id like to find a way to optimize this code so that i can dynamically loop through this tab and make the same chart in a tab form.
all_tabs = [jan_tab, feb_tab, mar_tab, apr_tab, may_tab, jun_tab, jul_tab, aug_tab, sep_tab, oct_tab] = st.tabs(months)

for idx, tab in enumerate(all_tabs):
    current_month = months[idx]
    with tab:
        st.write(current_month)
        produce_altair_chart(month_data[current_month])
''
# Create line chart for newly filtered dataframe 
# st.line_chart(
#     filtered_gdp_df,
#     x='Year',
#     y='GDP',
#     color='Country Code',
# )

''
''


# first_year = gdp_df[gdp_df['Year'] == from_year]
# last_year = gdp_df[gdp_df['Year'] == to_year]
# Header for GDP in Most Recent Year
st.header(f'Section 2', divider='gray')

''
# Creates grid component with predetermined number of 
cols = st.columns(4)
for col in cols:
    with col:
        st.write("Column")
# # For each of our selected countries
# for i, country in enumerate(selected_countries):
#     # Determines column that we are placing into
#     col = cols[i % len(cols)]
#     # WITH keyword for placing into column or tab for streamlit
#     with col:
#         first_gdp = first_year[first_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
#         last_gdp = last_year[last_year['Country Code'] == country]['GDP'].iat[0] / 1000000000

#         if math.isnan(first_gdp):
#             growth = 'n/a'
#             delta_color = 'off'
#         else:
#             growth = f'{last_gdp / first_gdp:,.2f}x'
#             delta_color = 'normal'

#         st.metric(
#             label=f'{country} GDP',
#             value=f'{last_gdp:,.0f}B',
#             delta=growth,
#             delta_color=delta_color
#         )


