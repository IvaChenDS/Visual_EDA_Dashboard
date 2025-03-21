import numpy as np  # Numerical operations and array handling
import pandas as pd  # Data manipulation and analysis

# Dash framework for building web applications
import dash  # Core Dash functionalities
from dash import dcc, html  # Directly use Dash Core Components (dcc) and HTML components (html)
import dash.dependencies as dd  # Handle app callbacks using Input, Output, and State


# Plotly for visualization
import plotly.express as px  # Simplified data visualization


df = pd.read_csv('COVID-19_Death_Counts.csv')
# Convert "End Date" to datetime
df["End Date"] = pd.to_datetime(df["End Date"])
df["Month"]= df["End Date"].dt.month
df["Year"]=df["End Date"].dt.year
df["Week"] = df["End Date"].dt.to_period("W")
### Clean Year ####
### Transform 2020/2021 io 2021; 2021/2022 to 2022
year_mapping = {
    '2019/2020': '2020',
    '2020/2021': '2021',
    '2021/2022': '2022'
}
df['Year'] = df['Year'].replace(year_mapping)

for var in ['COVID-19 Deaths', 'Pneumonia Deaths', 'Influenza Deaths', 'Total Deaths']:
    df[var + '_log'] = np.log(df[var].where(df[var] > 0, 1))  # Replace 0 with 1 for log calculation






# Define drowpdown options for disease
disease_options = {
    "COVID-19 Deaths": "COVID-19 Deaths",
    "Pneumonia Deaths": "Pneumonia Deaths",
    "Influenza Deaths": "Influenza Deaths",
    "Total Deaths": "Total Deaths",
    'COVID-19 Deaths_log': "COVID-19 Deaths_log", 
    'Pneumonia Deaths_log':"Pneumonia Deaths_log", 
    'Influenza Deaths_log': "Influenza Deaths_log",
    'Total Deaths_log': "Total Deaths_log"
}


# Define dropdown options for states
state_options = [{'label': state, 'value': state} for state in df["State"].unique()]

# Define dropdown options for week
week_options = [{'label': week, 'value': week} for week in df["End Date"].unique()]

# Define dropdown options for year
year_options = [{'label': year, 'value': year} for year in df["Year"].unique()]

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Disease Death Rate Dashboard", style={'textAlign': 'center'}),
    # Dropdown for Time-Series Graph
    html.Div([
        html.H3("Time-Series Graph"),
        html.Label("Select Disease:"),
        dcc.Dropdown(id='time-disease-dropdown', options=disease_options, value="COVID-19 Deaths", clearable=False),

        html.Label("Select State:"),
        dcc.Dropdown(id='time-state-dropdown', options=state_options, value="Alabama", clearable=False),

        html.Button("Update Graph", id="update-button", n_clicks=0),
        
        dcc.Graph(id='time-series-chart')
    ], style={'border': '1px solid black', 'padding': '10px', 'margin': '10px'}),

    # Dropdown and Slider for Box_Violin Graph
    html.Div([
        html.H3("Box_Violin Plot"),
        html.Label("Select Disease:"),
        dcc.Dropdown(id='box-disease-dropdown', options=disease_options, value="Total Deaths", clearable=False),

        html.Label("Select State:"),
        dcc.Dropdown(id='box-state-dropdown', options=state_options, value="United States", clearable=False),

        html.Label("Filter Death Range:"),
        dcc.RangeSlider(
                        id='box-death-slider',
                        min=0,     
                        max=df["COVID-19 Deaths"].max(),
                        step=50000,  
                        marks={i: f"{i//1000}k" for i in range(0, int(df["COVID-19 Deaths"].max()) + 1, 50000)},  
                        value=[0, df["COVID-19 Deaths"].max()]  # Default range from 0 to max
        ),

        html.Button("Update Graph", id="update-button2", n_clicks=0),
        
        dcc.Graph(id='box-violin-plot')
    ], style={'border': '1px solid black', 'padding': '10px', 'margin': '10px'}),



    # Dropdown for Scatterplot matrix
    html.Div([
        html.H3("Scatterplot matrix"),
        html.Label("Select Year:"),
        dcc.Dropdown(id='scatter-year-dropdown', options=year_options, value="2020", clearable=False),

        html.Label("Select State:"),
        dcc.Dropdown(id='scatter-state-dropdown', options=state_options, value="United States", clearable=False),

        html.Button("Update Graph", id="update-button3", n_clicks=0),
        
        dcc.Graph(id= 'scatter-matrix')
    ],  style={'border': '1px solid black', 'padding': '10px', 'margin': '10px'}),


    # Dropdown for heatmap
    html.Div([
        html.H3("Heatmap"),
        html.Label("Select Disease:"),
        dcc.Dropdown(id='heatmap-disease-dropdown', options=disease_options, value="COVID-19 Deaths", clearable=False),
        
        html.Button("Update Graph", id="update-button4", n_clicks=0),
        
        dcc.Graph(id= 'heatmap')
    ],  style={'border': '1px solid black', 'padding': '10px', 'margin': '10px'}),
  

    # Navigation Links
    dcc.Link("View Graphs in New Tab", href="/Disease Death RateDashboard", target="_blank"),

])

# Set up input parameters Time-Series Chart
@app.callback(
    dd.Output('time-series-chart', 'figure'),
    [dd.Input('update-button', 'n_clicks')],
    [dd.State('time-disease-dropdown', 'value'),
     dd.State('time-state-dropdown', 'value')]
)
def update_time_series(n_clicks, selected_disease, selected_state): 
    if n_clicks==0:
         return dash.no_update 
    
    if selected_state not in df["State"].unique():
        return px.line(title="No Data Available")
    
    filtered_df=df[df["State"]==selected_state].copy() 
    
    # Convert 'Week' column from Period to Timestamp if needed
    if isinstance(filtered_df["Week"].iloc[0], pd.Period):
        filtered_df["Week"] = filtered_df["Week"].dt.to_timestamp()

    # Convert to datetime (ensuring it's in timestamp format)
    filtered_df["Week"] = pd.to_datetime(filtered_df["Week"])

    # Sort the DataFrame
    filtered_df = filtered_df.sort_values(by=["Week"])


 
    #if "Week" is a Period object, it cannot be plotted in Plotly because it isn't JSON serializable.
    #We need to convert it to a string or timestamp before passing it to Plotly.   

    min_y_value = filtered_df[selected_disease].min()
    max_y_value = filtered_df[selected_disease].max()
    y_min = min_y_value * 0.9 if min_y_value > 0 else 0
    y_max = max_y_value * 1.1

    time_fig = px.line(filtered_df, x="Week", y=selected_disease,
                       title=f"{selected_disease} in {selected_state} Over Time",
                       labels={"Week": "Week", selected_disease: "Deaths"},
                       hover_data={"Week": "|%Y-%m-%d"} )

    time_fig.update_yaxes(range=[y_min, y_max])

    return time_fig
# Set up input parameters for box-violin plot
@app.callback(
    dd.Output('box-violin-plot', 'figure'),
    [dd.Input('update-button2', 'n_clicks')], 
    [dd.State('box-disease-dropdown', 'value'),
    dd.State('box-state-dropdown', 'value'),
    dd.State('box-death-slider', 'value')]
)
def box_violin(n_clicks, selected_disease, selected_state, death_range):
    if n_clicks==0:
         return dash.no_update 

    if not isinstance(death_range, (list, tuple)) or len(death_range) != 2:
        return dash.no_update 

    min_death, max_death = death_range


    df_filtered = df.dropna(subset=[selected_disease])

    filtered_df = df_filtered[(df_filtered['State'] == selected_state) & 
                              (df_filtered[selected_disease] >= min_death) & 
                              (df_filtered[selected_disease] <= max_death)].copy()

    
    if filtered_df.empty:
        return px.violin(title=f"No Data Available for {selected_disease} in {selected_state}")

        
# Boxplot & Violin Plot
    box_violin_fig = px.violin(filtered_df, x="Year", y=selected_disease, box=True, points="outliers", 
                               title=f"Violin Plot of {selected_disease} in {selected_state}")

    return box_violin_fig

# Set up Input parameters for scatter-matrix
@app.callback(
    [dd.Output('scatter-matrix', 'figure')],
    [dd.Input('update-button3', 'n_clicks')], 
    [dd.State('scatter-state-dropdown', 'value'),
    dd.State('scatter-year-dropdown', 'value')]
)


def scatter(n_clicks, selected_states, selected_years):
    if n_clicks==0:
         return dash.no_update
    
    filtered_df = df[(df['State'] == selected_states) & (df['Year'] == selected_years)].copy()
    
    if len(filtered_df) <=5:
        return px.scatter_matrix(title="No enough data available")

    diseases_log =['COVID-19 Deaths_log', 'Pneumonia Deaths_log', 'Influenza Deaths_log',
       'Total Deaths_log']
    
    scatter_fig = px.scatter_matrix(filtered_df, dimensions=diseases_log,
                            opacity=0.7,
                            labels={"value": "Deaths"},
                            title= f"Scatterplot Matrix of Log Transformation of Deaths Count in {selected_states} in Year {selected_years}")
                            

    scatter_fig.update_layout(height=800)

    return (scatter_fig,)

# Set up Input parameters for heatmap
@app.callback(
     dd.Output('heatmap', 'figure'),
    [dd.Input('update-button4', 'n_clicks')], 
    [dd.State('heatmap-disease-dropdown', 'value')]
    
)

def heatmap(n_clicks, selected_disease):
    if n_clicks is None or n_clicks == 0:
        return dash.no_update
    
    filtered_df = df[df["State"] != "United States"].copy()   ## excluding the United States from the heatmap 

    # Heatmap (Aggregated)
    pivot_df = filtered_df.pivot_table(index="Year", columns="State", values=selected_disease, aggfunc="sum")
    heatmap_fig = px.imshow(pivot_df, labels=dict(color="Deaths"),
                            color_continuous_scale = 'Reds',
                            title=f"Heatmap of {selected_disease} by Year")


    heatmap_fig.update_layout(height=800)

    return heatmap_fig

if __name__ == '__main__':
    app.run(debug=True, port=8052, use_reloader=False)
