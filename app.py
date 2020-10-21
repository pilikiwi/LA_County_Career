import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import csv

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


filename = './data/LA_County_Employee_Salaries_2019.csv'
filename_jobs = './data/job_titles_unique.csv'

options = []

with open(filename_jobs) as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        row = row[0]
        options.append({"label": row, "value": row})

df = pd.read_csv(filename)
target_job = 'INFORMATION TECHNOLOGY SPECIALIST II'
previous_job =[]
frequency = {}

#load the employee name and job title column only
#employee_name_title = df[['Employee Name', 'Middle Initial', 'Position Title']]

#Locate the employees who hold the position of target_job in 2019
current_employees = df[(df['Position Title'] == target_job) & (df['Year'] == 2019)]#.set_index("Employee Name")

"""print(current_employees['Base Earnings'].agg(['median', 'mean']))"""

current_employees = current_employees[['Employee Name', 'Middle Initial']]

#Find the job history for each employee
job_history = pd.merge(current_employees, df)
job_grouped = job_history.groupby(['Employee Name', 'Position Title']).count().reset_index()

#double check, but this number looks right
job_grouped = job_grouped['Position Title'].value_counts().drop(target_job).reset_index()

fig = px.bar(job_grouped, x="index", y="Position Title")

app.layout = html.Div(children=[
    html.Div([dcc.Dropdown(id="my-dynamic-dropdown")]),
    html.Div(id='dropdown_output'),
    html.H1(children='County Jobs'),
    dcc.Graph(id='previous_jobs',figure=fig)
])



@app.callback(
    dash.dependencies.Output("my-dynamic-dropdown", "options"),
    [dash.dependencies.Input("my-dynamic-dropdown", "search_value")],
)
def update_options(search_value):
    if not search_value:
        raise PreventUpdate
    search_value = search_value.upper()
    return [o for o in options if search_value in o["label"]]

@app.callback(
    dash.dependencies.Output("dropdown_output", "options"),
    [dash.dependencies.Input("my-dynamic-dropdown", "options")],
)
def update_show(options):
    return 'options'

if __name__ == '__main__':
    app.run_server(debug=False)