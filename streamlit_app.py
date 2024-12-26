import streamlit as st
import json
import os
import pandas as pd
import math
from pathlib import Path
import altair as alt
import numpy as np
average_data = [
    {"month": "Jan-24", "Answered Call %": 74.67, "Not Ready %": 27.16 },
    {"month": "Feb-24", "Answered Call %": 73.72, "Not Ready %": 22.61 },
    {"month": "Mar-24", "Answered Call %": 76.01, "Not Ready %": 22.41 },
    {"month": "Apr-24", "Answered Call %": 75.77, "Not Ready %": 25.61 },
    {"month": "May-24", "Answered Call %": 77.11, "Not Ready %": 22.89 },
    {"month": "Jun-24", "Answered Call %": 76.5, "Not Ready %": 22.31},
    {"month": "Jul-24", "Answered Call %": 87.75, "Not Ready %": 25.25},
    {"month": "Aug-24", "Answered Call %": 86.56, "Not Ready %": 27.16 },
    {"month": "Sep-24", "Answered Call %": 83.61, "Not Ready %": 27.64 },
    {"month": "Oct-24", "Answered Call %": 87.22, "Not Ready %": 27 },
]



# Arguments should be the data you are entering as well as what you would like to name the JSON file. 
def write_to_json(data, file_name):
    json_data = json.dumps(data, indent=4)
    json_data = json.dumps(data, indent=4)
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, f"{file_name}.json")
    with open(file_path, "w") as json_file:
        json_file.write(json_data)
    print(f"JSON data written to {file_name}")
# When needing to reformat to match recharts. Data argument needs to come from method PhoneMetrics.create_employee_list
def bar_chart_restructure(data, metric_name, to_json, file_name):
    res_array = []
    for employee in data:
        for month in months:
            curr = {"month": month, "val": employee[f"{month} {metric_name}"]}
            res_array.append(curr)
    if to_json:
        write_to_json(res_array, file_name)
    else: 
        return res_array
# Main class for handling CSV metrics data
class PhoneMetrics:
    def __init__(self, csv_path, header_indexes, metrics_to_include, months):
        self.csv_path = csv_path
        self.metrics_to_include = metrics_to_include
        self.months = months
        self.dataframe = pd.read_csv(csv_path, header=header_indexes)
        # If there are issues with initializing, try moving 2 lines of code underneath to create_employee_list
        self.dataframe.insert(0, "Employee ID", range(1, len(self.dataframe) + 1))
        self.dataframe.columns = [" ".join(col).strip() for col in self.dataframe.columns]
    # This function creates an array, categorized by employee and contains each of their stats for every month. 
    def create_employee_list(self):
        months = [col.split(" ")[0] for col in self.dataframe.columns if any(month in col for month in self.months)]
        # # Initialize the array for the result
        result = []
        # Iterate through each pandas row
        for idx, row in self.dataframe.iterrows():
            # Row contains all monthly data for 1 employee
            employee_data = {}
            # we want to loop through each month and get all relevant data from current row for that month
            for month in months:
                # Targeting specifically Answered calls and not ready % in our row
                for metric in self.metrics_to_include:
                    # Get specific key CURRENTMONTH + METRIC. This is the key that we created for our condensed dataframe
                    column_name = f"{month} {metric}"
                    # DF.columns contains all of our needed columns. We want to make sure we accurately created the column name
                    if column_name in self.dataframe.columns:
                        curr = row[column_name]
                        if curr == "LOA" or str(curr) == "NaN":
                            employee_data[column_name] = None
                        else:
                            # Recall we are iterating every month and in one iteration of a specific metric. We want to 
                            employee_data[column_name] = float(row[column_name])
            result.append({**employee_data, "Employee ID": row["Employee ID"]})
        return result


# Add some spacing
PHONE_STATS_FILENAME = 'data/phonestats.csv'
months = ['Jan-24', 'Feb-24', 'Mar-24', 'Apr-24', 'May-24', 'Jun-24', 
          'Jul-24', 'Aug-24', 'Sep-24', 'Oct-24']
metrics_to_include = ["Answered Call %", "Not Ready %", "Tardies", "Absences"]
months = ["Jan-24", "Feb-24", "Mar-24", "Apr-24", "May-24", "Jun-24", "Jul-24", "Aug-24", "Sep-24", "Oct-24"] 
csv_headers = [0,2]

# Code below creates arrays for respective metric
phone_metric = PhoneMetrics(PHONE_STATS_FILENAME, csv_headers, metrics_to_include, months )
employee_list = phone_metric.create_employee_list()
bar_chart_restructure(employee_list, "Absences", True, "absences_data")




# case_census_filename = "data/case_census.csv"
# case_df = pd.read_csv(case_census_filename)
# json_data = case_df.to_json(orient="records", date_format="iso")
# json_data = json.dumps(json.loads(json_data))



# Organizes initial CSV to be organized by month
# def organize_data(df):
#     df.insert(0, "Employee ID", range(1, len(df) + 1))
#     df.columns = [" ".join(col).strip() for col in df.columns]
#     metrics_to_include = ["Answered Call %", "Not Ready %", "Tardies", "Absences"]
#     # print(df.columns)
#     months = [col.split(" ")[0] for col in df.columns if any(month in col for month in ["Jan-24", "Feb-24", "Mar-24", "Apr-24", "May-24", "Jun-24", "Jul-24", "Aug-24", "Sep-24", "Oct-24"])]
#     # # Initialize the array for the result
#     result = []
#     # Iterate through each pandas row
#     for idx, row in df.iterrows():
#         # Row contains all monthly data for 1 employee
#         employee_data = {}
#         # we want to loop through each month and get all relevant data from current row for that month
#         for month in months:
#             # Targeting specifically Answered calls and not ready % in our row
#             for metric in metrics_to_include:
#                 # Get specific key CURRENTMONTH + METRIC. This is the key that we created for our condensed dataframe
#                 column_name = f"{month} {metric}"
#                 # DF.columns contains all of our needed columns. We want to make sure we accurately created the column name
#                 if column_name in df.columns:
#                     curr = row[column_name]
#                     if curr == "LOA":
#                         employee_data[column_name] = None
#                     else:
#                         # Recall we are iterating every month and in one iteration of a specific metric. We want to 
#                         employee_data[column_name] = float(row[column_name])
#         result.append({**employee_data, "Employee ID": row["Employee ID"]})
#     return result



