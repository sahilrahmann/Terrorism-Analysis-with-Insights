# Importng the required packages
import pandas as pd
import webbrowser
import dash
import dash_html_components as html
from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc


# Creating Dash object
app = dash.Dash(__name__)

server = app.server

# Modal Content
desc = "Protective vehicles are less in numbers with the Army and are distributed uniformly across the area. Similarly, Explosive Detection Dogs ( ED Dogs ) are only less in the entire country. This web application can be used as a Predictive Analysis tool to find the trendline of each kind of Attack ( Bombing, Assassination, Etc.). This tool help in finding the concentration of Attack type - Bombing in the area which would help in allocation of the resources. Visualizing the data gives clear patterns about the data and makes it easy for the analysis. There are two components: 1. Map Tool -> It is used to generate a Scatter Geo Map with markers for highlighting the latitude/longitude where the incident happened based on combinations of Month, Day, Attack Type, Region, Country, State and City, and filter the 9 Type of Attacks ( Bombing, Assassination, Kidnapping, Etc.). Clicking and hovering of the mouse show pieces of information. 2. Chart Tool -> It is used to show the Stacked Line Chart images of the frequency of terrorist incidents each year. One can Group first by (Country Attacked, Region, Target Nationality, Target Type, Type of Attack, Weapon Type, Terrorist Organisation) with a search based on the selected Group. Both the components are available separately for the World and India. In this project, the dataset has approximately 1,90,000 records. Python programming language has been used for the development of this project, whereas Dash and Plotly are the critical components used to form the UI (User Interface) for the webpage and Bootstrap has been used for the styling purpose."

# Creating Modal layout
global modal
modal = html.Div(
    [
        html.Br(),
        dbc.Button("About the project", id="open"),
        dbc.Modal([
            dbc.ModalHeader(
                html.H2("About the project"),
            ),
            dbc.ModalBody(
                dbc.Form(
                    [
                        html.H6(desc, style={'text-align': 'justify'})
                    ],
                    inline=True,
                )
            ),
            dbc.ModalFooter(
                dbc.Button("Close", id="close", className="ml-auto")
            ),
        ],
            id="modal",
            is_open=False,    # True, False
            size="xl",        # "sm", "lg", "xl"
            backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
            scrollable=True,  # False or True if modal has a lot of text
            centered=True,    # True, False
            fade=True         # True, False
        ),
    ],
)

# Loading the Dataset
def load_data():
    dataset_name = "finaldataset.csv"
    pd.options.mode.chained_assignment = None

    global df
    df = pd.read_csv(dataset_name)

    global month_list
    month = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }
    month_list = [{"label": key, "value": values} for key, values in
                  month.items()]

    global date_list
    date_list = [x for x in range(1, 32)]

    global region_list
    region_list = [{"label": str(i), "value": str(i)} for i in sorted(
        df['region_txt'].unique().tolist())]

    global country_list
    country_list = df.groupby("region_txt")["country_txt"].unique().apply(
        list).to_dict()

    global state_list
    state_list = df.groupby("country_txt")["provstate"].unique().apply(
        list).to_dict()

    global city_list

    city_list = df.groupby("provstate")["city"].unique().apply(
        list).to_dict()

    global attack_type_list
    attack_type_list = [{"label": str(i), "value": str(i)} for i in df[
        'attacktype1_txt'].unique().tolist()]

    global year_list
    year_list = sorted(df['iyear'].unique().tolist())

    global year_dict
    year_dict = {str(year): str(year) for year in year_list}

    global chart_dropdown_values
    chart_dropdown_values = {"Terrorist Organisation": 'gname',
                             "Target Nationality": 'natlty1_txt',
                             "Target Type": 'targtype1_txt',
                             "Type of Attack": 'attacktype1_txt',
                             "Weapon Type": 'weaptype1_txt',
                             "Region": 'region_txt',
                             "Country Attacked": 'country_txt'
                             }

    chart_dropdown_values = [{"label": keys, "value": value} for keys, value in
                             chart_dropdown_values.items()]

# To open the browser
def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')

# Application UI
def create_app_ui():
    main_layout = html.Div([
        html.Br(),

        # Heading
        html.H1('Terrorism Analysis with Insights', id='Main_title', style={"text-align":"center"}),
        html.Br(),

        # Tabs
        dcc.Tabs(id="Tabs", value="Map",style={'width': '95%','fontFamily': 'Sans-Serif','margin-left': 'auto','margin-right': 'auto'},
                 children=[

            # Map Tool tab
            dcc.Tab(label="Map tool", id="Map tool", value="Map",
                    children=[
                        dcc.Tabs(id="subtabs", value="WorldMap", style={'width': '95%','fontFamily': 'Sans-Serif','margin-left': 'auto','margin-right': 'auto'},
                                 children=[
                            # Map Tool Subtabs
                            dcc.Tab(label="World Map tool", id="World", value="WorldMap"),
                            dcc.Tab(label="India Map tool", id="India", value="IndiaMap")
                        ]),
                        html.Br(),

                        # Dropdowns
                        html.Div([
                            dcc.Dropdown(
                                id='month',
                                options=month_list,
                                placeholder='Select Month',
                                multi=True,
                                style={'padding': '3px', 'width': '80%', 'margin': 'auto', 'textAlign': 'center'}
                            ),
                            dcc.Dropdown(
                                id='date',
                                placeholder='Select Day',
                                options=date_list,
                                multi=True,
                                style={'padding': '3px', 'width': '80%', 'margin': 'auto', 'textAlign': 'center'}
                            ),
                            dcc.Dropdown(
                                id='region-dropdown',
                                options=region_list,
                                placeholder='Select Region',
                                multi=True,
                                style={'padding': '3px', 'width': '80%', 'margin': 'auto', 'textAlign': 'center'}
                            ),
                            dcc.Dropdown(
                                id='country-dropdown',
                                options=[{'label': 'All', 'value': 'All'}],
                                placeholder='Select Country',
                                multi=True,
                                style={'padding': '3px', 'width': '80%', 'margin': 'auto', 'textAlign': 'center'}
                            ),
                            dcc.Dropdown(
                                id='state-dropdown',
                                options=[{'label': 'All', 'value': 'All'}],
                                placeholder='Select State or Province',
                                multi=True,
                                style={'padding': '3px', 'width': '80%', 'margin': 'auto', 'textAlign': 'center'}
                            ),
                            dcc.Dropdown(
                                id='city-dropdown',
                                options=[{'label': 'All', 'value': 'All'}],
                                placeholder='Select City',
                                multi=True,
                                style={'padding': '3px', 'width': '80%', 'margin': 'auto', 'textAlign': 'center'}
                            ),
                            dcc.Dropdown(
                                id='attacktype-dropdown',
                                options=attack_type_list,
                                placeholder='Select Attack Type',
                                multi=True,
                                style={'padding': '3px', 'width': '80%', 'margin': 'auto', 'textAlign': 'center'}
                            ),html.Br(),
                        ], style={"width":"70%", 'margin-left': 'auto','margin-right': 'auto', "cursor":"pointer"}),

                        # Year Slider
                        html.Div([
                            html.H5('Select the Year', id='year_title'),
                            html.Div([
                                dcc.RangeSlider(
                                    id='year-slider',
                                    min=min(year_list),
                                    max=max(year_list),
                                    value=[min(year_list), max(year_list)],
                                    marks=year_dict,
                                    step=None
                                )
                            ]),
                        ],style={"width":"95%", 'margin-left': 'auto','margin-right': 'auto', "cursor":"pointer"}),
                        html.Br()
                    ]),

            # Chart Tool Tab
            dcc.Tab(label="Chart Tool", id="chart tool", value="Chart",
                    children=[

                        # Chart Tool -> World Chart Tool Subtab
                        dcc.Tabs(id="subtabs2", value="WorldChart",style={'width': '95%','fontFamily': 'Sans-Serif','margin-left': 'auto','margin-right': 'auto'}, children=[
                            dcc.Tab(label="World Chart tool", id="WorldC", value="WorldChart", children=[
                                html.Br(),

                                html.Div([

                                    # Dropdown
                                    dcc.Dropdown(id="Chart_Dropdown", options=chart_dropdown_values,
                                                 placeholder="Select option", value="region_txt",
                                                 style={'padding': '3px', 'width': '80%', 'margin': 'auto', 'textAlign': 'center'}),
                                    html.Br(),
                                    html.Hr(),

                                    # Search Input
                                    dcc.Input(id="search", placeholder="Search Filter", style={'padding': '3px', 'width': '64%', 'margin-left': '18%', 'textAlign': 'center'}),
                                    html.Hr(),
                                    html.Br()
                                ],style={"width":"70%", 'margin-left': 'auto','margin-right': 'auto', "cursor":"pointer"}),

                                ]),

                            # Chart Tool -> India Chart Tool Subtab
                            dcc.Tab(label="India Chart tool", id="IndiaC", value="IndiaChart", children=[
                                html.Br(),

                                html.Div([

                                    # Dropdown
                                    dcc.Dropdown(
                                        id="Chart_Dropdownn",
                                        options=chart_dropdown_values,
                                        placeholder="Select option",
                                        value="region_txt",
                                    style={'padding': '3px', 'width': '80%', 'margin': 'auto', 'textAlign': 'center'}),
                                    html.Br(),
                                    html.Hr(),

                                    # Search Input
                                    dcc.Input(id="searchh", placeholder="Search Filter", style={'padding': '3px', 'width': '64%', 'margin-left': '18%', 'textAlign': 'center'}),
                                    html.Hr(),
                                    html.Br()
                                ],style={"width":"70%", 'margin-left': 'auto','margin-right': 'auto', "cursor":"pointer"}),
                            ])
                        ]),
                    ])
                 ]),

        html.Div([

            # Loading Circle and Declaring Graph
            dcc.Loading(children=[html.Div(id="graph-object", children="Graph will be shown here")], type='circle',
                        style={"backgroundColor": "transparent", "z-index": "1", "position": "absolute"}),
        ],style={'width': '95%', 'margin-left': 'auto', 'margin-right': 'auto'}),




        html.Br(),
        html.Br(),

        # Footer
        html.Footer(id="footer",
                    style={"padding-bottom": "1px"},
                    children=[

                        # Name of the creator
                        html.H3(style={"text-align": "center"}, children=[
                            html.H3(children="Made by Sahil Rahman ", style={"display": "inline"}),
                        ]),

                        # Email of the creator
                        html.H6(style={"text-align": "center"}, children=[
                            html.H6(children="Email: srjordon414@gmail.com", style={"display": "inline"}),
                        ]),

                        # Linkedin profile of the creator
                        html.H6(style={"text-align": "center"}, children=[
                            html.H6(children="Linkedin: https://www.linkedin.com/in/sahilrahman/", style={"display": "inline"}),
                            html.Br(),
                            modal,

                        ]),
                        html.Br(),

                    ]),
        html.Br(),

    ])

    # Returning Main Layout
    return main_layout


# Callback of the page
@app.callback(

    # Callback Output -> Graph
    dash.dependencies.Output('graph-object', 'children'),
              [

                  # Callback Inputs -> Dropdowns
                  dash.dependencies.Input("Tabs", "value"),
                  dash.dependencies.Input('month', 'value'),
                  dash.dependencies.Input('date', 'value'),
                  dash.dependencies.Input('region-dropdown', 'value'),
                  dash.dependencies.Input('country-dropdown', 'value'),
                  dash.dependencies.Input('state-dropdown', 'value'),
                  dash.dependencies.Input('city-dropdown', 'value'),
                  dash.dependencies.Input('attacktype-dropdown', 'value'),
                  dash.dependencies.Input('year-slider', 'value'),

                  dash.dependencies.Input("Chart_Dropdown", "value"),
                  dash.dependencies.Input("search", "value"),
                  dash.dependencies.Input("subtabs2", "value"),

                  dash.dependencies.Input("Chart_Dropdownn", "value"),
                  dash.dependencies.Input("searchh", "value"),
                  dash.dependencies.Input("subtabs2", "value"),
              ]
              )
# Function to use the above Callback
def update_app_ui(Tabs, month_value, date_value, region_value, country_value, state_value, city_value, attack_value,
                  year_value, chart_dp_value, search,
                  subtabs2, Chart_Dropdownn_value, searchh,
                  subtabs22):
    fig = None

    if Tabs == "Map":
        print("Data Type of month value = ", str(type(month_value)))
        print("Data of month value = ", month_value)

        print("Data Type of Day value = ", str(type(date_value)))
        print("Data of Day value = ", date_value)

        print("Data Type of region value = ", str(type(region_value)))
        print("Data of region value = ", region_value)

        print("Data Type of country value = ", str(type(country_value)))
        print("Data of country value = ", country_value)

        print("Data Type of state value = ", str(type(state_value)))
        print("Data of state value = ", state_value)

        print("Data Type of city value = ", str(type(city_value)))
        print("Data of city value = ", city_value)

        print("Data Type of Attack value = ", str(type(attack_value)))
        print("Data of Attack value = ", attack_value)

        print("Data Type of year value = ", str(type(year_value)))
        print("Data of year value = ", year_value)

        year_range = range(year_value[0],
                           year_value[1] + 1)

        new_df = df[df["iyear"].isin(year_range)]

        if month_value == [] or month_value is None:
            pass
        else:
            if date_value == [] or date_value is None:
                new_df = new_df[
                    new_df["imonth"].isin(month_value)]
            else:
                new_df = new_df[new_df["imonth"].isin(
                    month_value)
                                & (new_df["iday"].isin(date_value))]
        if region_value == [] or region_value is None:
            pass
        else:
            if country_value == [] or country_value is None:
                new_df = new_df[new_df["region_txt"].isin(region_value)]
            else:
                if state_value == [] or state_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(
                        region_value)) &
                                    (new_df["country_txt"].isin(country_value))]
                else:
                    if city_value == [] or city_value is None:
                        new_df = new_df[(new_df["region_txt"].isin(
                            region_value)) &
                                        (new_df["country_txt"].isin(country_value)) &
                                        (new_df["provstate"].isin(state_value))]
                    else:
                        new_df = new_df[(new_df["region_txt"].isin(
                            region_value)) &
                                        (new_df["country_txt"].isin(country_value)) &
                                        (new_df["provstate"].isin(state_value)) &
                                        (new_df["city"].isin(city_value))]

        if attack_value == [] or attack_value is None:
            pass
        else:
            new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)]

        mapFigure = go.Figure()
        if new_df.shape[0]:
            pass
        else:
            new_df = pd.DataFrame(columns=['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
                                           'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])

            new_df.loc[0] = [0, 0, 0, None, None, None, None, None, None, None, None]

        mapFigure = px.scatter_mapbox(new_df,
                                      lat="latitude",
                                      lon="longitude",
                                      color="attacktype1_txt",
                                      hover_name="city",
                                      hover_data=["region_txt", "country_txt", "provstate", "city", "attacktype1_txt",
                                                  "nkill", "iyear", "imonth", "iday"],
                                      zoom=1
                                      )
        mapFigure.update_layout(mapbox_style="open-street-map",
                                autosize=True,
                                margin=dict(l=20, r=20, t=20, b=20), template = 'plotly_dark',
                                )

        fig = mapFigure

    elif Tabs == "Chart":
        fig = None
        if subtabs2 == "WorldChart":
            if chart_dp_value is not None:
                if search is not None:
                    chart_df = df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
                    chart_df = chart_df[chart_df[chart_dp_value].str.contains(search,case=False)]
                else:  # this else means search not given
                    chart_df = df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
            else:  # if dropdown also not selcted dont update any
                raise PreventUpdate
            chartFigure = px.area(chart_df, x="iyear", y="count",color=chart_dp_value, template='plotly_dark')
            fig = chartFigure
        elif subtabs22 == "IndiaChart":

            n_df = df[[df['region_txt'] == "South Asia"] and df[
                'country_txt'] == "India"]

            if Chart_Dropdownn_value is not None:
                if searchh is not None:
                    chart_df = n_df.groupby("iyear")[Chart_Dropdownn_value].value_counts().reset_index(name="count")
                    chart_df = chart_df[chart_df[Chart_Dropdownn_value].str.contains(searchh, case=False)]
                else:
                    chart_df = n_df.groupby("iyear")[Chart_Dropdownn_value].value_counts().reset_index(name="count")
            else:
                raise PreventUpdate
            chartFigure = px.area(chart_df, x="iyear", y="count", color=Chart_Dropdownn_value, template='plotly_dark')
            fig = chartFigure

        else:
            return None
    return dcc.Graph(figure=fig)


# Callback for the selected month
@app.callback(
    Output("date", "options"),
    [Input("month", "value")])

# Function to call the above Callback
def update_date(month):
    option = []
    if month:
        option = [{"label": m, "value": m} for m in
                  date_list]
    return option


# Callback for the Selected Subtabs
@app.callback([Output("region-dropdown", "value"),
               Output("region-dropdown", "disabled"),
               Output("country-dropdown", "value"),
               Output("country-dropdown", "disabled")],
              [Input("subtabs", "value")])

# Function to call the above Callback
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":
        pass
    elif tab == "IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c


# Callback for the selected Region Dropdown
@app.callback(
    Output('country-dropdown', 'options'),
    [Input('region-dropdown', 'value')])

# Function to call the above Callback
def set_country_options(region_value):
    option = []
    if region_value is None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label': m, 'value': m} for m in option]


# Callback for the selected Country Dropdown
@app.callback(
    Output('state-dropdown', 'options'),
    [Input('country-dropdown', 'value')])

# Function to call the above Callback
def set_state_options(country_value):
    option = []
    if country_value is None:
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label': m, 'value': m} for m in option]


# Callback for the selected State Dropdown
@app.callback(
    Output('city-dropdown', 'options'),
    [Input('state-dropdown', 'value')])

# Function to call the above Callback
def set_city_options(state_value):
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label': m, 'value': m} for m in option]


# Callback for the Modal
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)

# Function to call the above Callback
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Main Execution Function
def main():

    # Calling the function load_data()
    load_data()

    # Calling the function open_browser()
    open_browser()

    global app

    # Putting the Appliction UI into app.layout
    app.layout = create_app_ui()

    # Setting the title of the Web-Application
    app.title = "Terrorism Analysis with Insights"

    # To run the application
    app.run_server()


# Calling out the entry point
if __name__ == '__main__':
    main()