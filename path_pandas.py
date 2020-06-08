import pandas as pd
from collections import Counter

from plotly.graph_objs import Bar, Layout
from plotly import offline

filename = 'LA_County_Employee_Salaries.csv'

input_file = pd.read_csv(filename)
current_job = 'APPLICATION DEVELOPER II'
employee_names = []
job_history = []
previous_job =[]
frequency = {}

#Locate the employees who hold the position of current_job in 2018
for row in input_file:
    if row['Position Title'] == current_job and row['Year'] == 2018 :
        employee_names.append(row['Employee Name'] + row['Middle Initial'])

#match those employees in the input files and find their previous jobs.
input_file = pd.read_csv(filename)
for row in input_file:
    for employee_name in employee_names:
        if row['Employee Name'] + row['Middle Initial'] == employee_name:
            record = {
             row['Year']:row['Position Title'],
             }
            job_history.append(record)


#Filter out the current job
for i in job_history:
    for key, value in i.items():
        if value != current_job:
          previous_job.append(value)

for item in previous_job:
    if item in frequency:
        frequency[item] += 1
    else:
        frequency[item] = 1

x_values, y_values = [], []

for key, value in frequency.items():
    x_values.append(key)
    y_values.append(value)

data = dict(
    type = 'bar',
    x = x_values,
    y = y_values,
    marker={
        'color': 'rgb(60, 100, 150)',
        'line': {'width':1.5, 'color': 'rgb(25, 25, 25)'}
    },
    opacity = 0.6,
)


my_layout = {
    'title': f"Employee who are have the title of {current_job} in 2018 was: ",
    'titlefont': {'size': 24},
    'xaxis': {
        'title': 'Job Title',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14},
    },
    'yaxis': {
        'title': 'Job Count',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14},
    },
}

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='career_path.html')
