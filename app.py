#!/usr/bin/env python

# # Interactive Dashboard #
# ### Covid-19 Death Count Analysis ###
# *Dataset Overview*
# ![Screenshot 2025-03-14 at 3.33.58 PM.png](attachment:4508d0ca-ad66-404a-b090-0116067f3537.png)



## Install packages if you have not used 
## Uncomment the following based on your need
#! pip install dash plotly 


# Import Necessary Libraries



import dash
from dash import dcc, html
import dash.dependencies as dd
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go # use for subplots
from plotly.subplots import make_subplots
#import seaborn as sns
import matplotlib.pyplot as plt
import dash.dash_table as dt



# Load and Preprocess the Data
# The dataset contains death counts categorized by disease, state, and time.



df = pd.read_csv('COVID-19_Death_Counts.csv')




df.columns




# Convert "End Date" to datetime
df["End Date"] = pd.to_datetime(df["End Date"])
df["Month"]= df["End Date"].dt.month
df["Year"]=df["End Date"].dt.year
df["Week"] = df["End Date"].dt.to_period("W")




### Log transformation of death count
for var in ['COVID-19 Deaths', 'Pneumonia Deaths', 'Influenza Deaths', 'Total Deaths']:
    df.loc[df[var] > 0, var + '_log'] = np.log(df[var])
    #print (df[var+'_log'])
df.columns


# Create Dropdown Options



# Define drowpdown options for disease
disease_options = {
    "COVID-19 Deaths": "COVID-19 Deaths",
    "Pneumonia Deaths": "Pneumonia Deaths",
    "Influenza Deaths": "Influenza Deaths",
    "Total Deaths": "Total Deaths"
}
disease_log= ['COVID-19 Deaths_log', 'Pneumonia Deaths_log', 'Influenza Deaths_log','Total Deaths_log']  
# Define dropdown options for states
state_options = [{'label': state, 'value': state} for state in df["State"].unique()]

# Define dropdown options for week

week_options = [{'label': week, 'value': week} for week in df["End Date"].unique()]

# Define dropdown options for year

year_options = [{'label': year, 'value': year} for year in df["Year"].unique()]


# Build the Dashboard Layout



app = dash.Dash(__name__)
server = app.server  # Required for Gunicorn in production
app.layout = html.Div([
    html.H1("Disease Death Rate Dashboard", style={'textAlign': 'center'}),
    # Dropdown for Time-Series Graph
    html.Div([
        html.H3("Time-Series Graph Controls"),
        html.Label("Select Disease:"),
        dcc.Dropdown(id='time-disease-dropdown', options=disease_options, value="COVID-19 Deaths", clearable=False),

        html.Label("Select State:"),
        dcc.Dropdown(id='time-state-dropdown', options=state_options, value="Alabama", clearable=False),

        html.Button("Update Graph", id="update-button", n_clicks=0),
        
        dcc.Graph(id='time-series-chart')
    ], style={'border': '1px solid black', 'padding': '10px', 'margin': '10px'}),

    # Dropdown and Slider for Box_Voin Graph
    html.Div([
        html.H3("Box_Violin Graph Controls"),
        html.Label("Select Disease:"),
        dcc.Dropdown(id='box-disease-dropdown', options=disease_options, value="Total Deaths", clearable=False),

        html.Label("Select State:"),
        dcc.Dropdown(id='box-state-dropdown', options=state_options, value="Alabama", clearable=False),

        html.Label("Filter Death Range:"),
        dcc.RangeSlider(
            id='box-death-slider',
            min=df["COVID-19 Deaths"].min(), 
            max=df["COVID-19 Deaths"].max(), 
            step=max(1, (df["COVID-19 Deaths"].max() - df["COVID-19 Deaths"].min()) // 10), 
            marks={i: str(i) for i in range(int(df["COVID-19 Deaths"].min()), int(df["COVID-19 Deaths"].max()), 
                                                  max(500, (int(df["COVID-19 Deaths"].max()) - int(df["COVID-19 Deaths"].min())) // 10))},
            value=[df["COVID-19 Deaths"].min(), df["COVID-19 Deaths"].max()]  
        ),

        html.Button("Update Graph", id="update-button2", n_clicks=0),
        
        dcc.Graph(id='box-violin-plot')
    ], style={'border': '1px solid black', 'padding': '10px', 'margin': '10px'}),



    # Dropdown for Scatterplot matrix
    html.Div([
        html.H3("Scatterplot matrix Controls"),
        html.Label("Select Year:"),
        dcc.Dropdown(id='scatter-year-dropdown', options=year_options, value="2020", clearable=False),

        html.Label("Select State:"),
        dcc.Dropdown(id='scatter-state-dropdown', options=state_options, value="United States", clearable=False),

        html.Button("Update Graph", id="update-button3", n_clicks=0),
        
        dcc.Graph(id= 'scatter-matrix')
    ],  style={'border': '1px solid black', 'padding': '10px', 'margin': '10px'}),


    # Dropdown for heatmap
    html.Div([
        html.H3("Heatmap Controls"),
        html.Label("Select Disease:"),
        dcc.Dropdown(id='heatmap-disease-dropdown', options=disease_options, value="COVID-19 Deaths", clearable=False),
        
        html.Button("Update Graph", id="update-button4", n_clicks=0),
        
        dcc.Graph(id= 'heatmap')
    ],  style={'border': '1px solid black', 'padding': '10px', 'margin': '10px'}),
  

    # Navigation Links
    dcc.Link("View Graphs in New Tab", href="/Disease Death RateDashboard", target="_blank"),


    # Page Content
    #dash.page_container
])






# # Use Plotly Express to create line charts #
# 
# fig = px.line(data_frame, x="X_column", y="Y_column", color="Category")
# 
# 
# Parameter	Description
# data_frame	The Pandas DataFrame containing the data.
# x	        The column to use for the x-axis (e.g., time or date).
# y	        The column to use for the y-axis (e.g., death rates).
# color	    (Optional) Categorizes lines based on another column.
# title	    (Optional) Sets the chart title.



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


# # Use Plotly Express to create box and violin plots #
# 
# fig1 = px.violin(data_frame, x=x, y=y, color=None, box=True, points="outliers")
# 
# Argument	Description
# data_frame	The Pandas DataFrame containing the data.
# x	        Categorical variable (e.g., "State", "Disease").
# y	        Numeric variable (e.g., "COVID-19 Deaths").
# color	    Adds color grouping (same as x).
# box	        If True, adds a boxplot inside the violin plot.
# points	    Shows individual points: "all", "outliers", "none". 
# 
# 



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


# # Use Plotly Express to create a scatterplot matrix #
# px.scatter_matrix(data_frame, dimensions, color=None, symbol=None, title=None)
# 
# Argument	Description
# data_frame	The Pandas DataFrame containing the data.
# dimensions	A list of numerical columns to be compared in the scatterplot matrix.
# color	    (Optional) Column name for grouping data by color.
# symbol	    (Optional) Column name for different point markers.
# size	    (Optional) Column name to set the size of scatterplot markers.
# title	    (Optional) Title of the scatterplot matrix.
# 
# 



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


    
    scatter_fig = px.scatter_matrix(filtered_df, dimensions=disease_log,
                            opacity=0.7,
                            labels={"value": "Deaths"})
                            #log_x= True,
                            #log_y= True )

    scatter_fig.update_layout(height=1200)

    return (scatter_fig,)


# # Create Heatmap #
# Aggregate data to see sum of death per year for a given disease
# Use px.imshow 
# 
# px.imshow(img, labels=None, x=None, y=None, color_continuous_scale=None, title=None)
# 
# Argument	Description
# img	        Required → A 2D array (list, NumPy array, or Pandas DataFrame) representing the heatmap values.
# x	        Labels for the x-axis (e.g., column names for heatmaps).
# y	        Labels for the y-axis (e.g., row names for heatmaps).
# labels	    Dictionary for axis labels (labels={"color": "Deaths"}).
# color_continuous_scale	Color scheme for heatmap ("Reds", "Viridis", "Blues", etc.).
# title	                Sets the heatmap title.
# zmin, zmax	            Min/max values for color scale.
# origin	                Determines the heatmap orientation ("upper" or "lower").



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


    heatmap_fig.update_layout(height=1200)

    return heatmap_fig


# # Running the App #



if __name__ == '__main__':
    app.run(debug=True, port=8052, use_reloader=False)


# In[ ]:










# In[ ]:





# In[ ]:




