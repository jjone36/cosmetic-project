from flask import Flask, render_template, url_for

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

# 1. Launch the application
server = Flask(__name__)

@server.route("/")
@server.route("/home")
def home():
    return render_template('home.html')


@server.route("/about")
def about():
    return render_template('about.html')


app = dash.Dash(__name__, server = server, url_base_pathname ='/dash')

# 2. Import the dataset
cosm = pd.read_csv('https://raw.githubusercontent.com/jjone36/Dash/master/data.csv')

option_1 = ['Moisturizer', 'Cleanser', 'Treatment', 'Face Mask', 'Eye cream', 'Sun protect']
option_2 = ['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']

category = []
for opt in option_1:
    category.append({'label' : opt, 'value' : opt})

skin = []
for opt in option_2:
    skin.append({'label' : opt, 'value' : opt})

# 3. Create a plotly figure

# 4. Create a Dash layout
app.layout = html.Div([
    # option 1
    html.Div([
            html.H2("Cosmetic Recommendation"),
            html.Label("Choose the category of cosmetics!"),
            dcc.Dropdown(id = 'item_opt', options = category, value = option_1[0])
            ],
             style = {'width': '300px', 'padding-left' : '100px', 'display': 'inline-block'}),
    # option 2
    html.Div([
            html.Label("   and your skin type!"),
            dcc.Dropdown(id = 'skin_opt', options = skin, value = option_2[0])
            ],
            style = {'width': '300px', 'padding-left' : '20px', 'display': 'inline-block'}),
    # graph
    dcc.Graph(id='graph', style = {'width' : '60%'}),
    # text search
    html.Div([dcc.Input(placeholder = 'Search Your Item', type = 'text', value = '')],
            style = {'padding-left': '100px'}),
], style = {'padding' : '50px'})

# 5. Add callback functions
@app.callback(Output('graph', 'figure'),
              [Input('item_opt', 'value'),
               Input('skin_opt', 'value')])
def update_figure(input_1, input_2):

    # filter the data
    df = cosm[(cosm['Category'] == input_1) & (cosm['Skin'] == input_2)]

    # Create a plotly figure
    trace = go.Scatter(x = df.X, y = df.Y, mode = 'markers',
                   marker = dict(size = 10,
                                color = 'rgba(51, 204, 153, .7)',
                                symbol = 'pentagon',
                                line = {'width':1}))
    layout = go.Layout(xaxis = dict(title = 'X-values',
                                    autorange = True,
                                    titlefont=dict(family='Arial, sans-serif',
                                                    size=18,
                                                    color='lightgrey')),
                       yaxis = dict(title = 'Y-values',
                                    autorange = True,
                                    titlefont=dict(family='Arial, sans-serif',
                                                    size=18,
                                                    color='lightgrey')))
    fig = go.Figure(data = [trace], layout = layout)

    return fig

@server.route('/dash')
def dashApp():
    return app.index()

if __name__ == '__main__':
    server.run(debug = True)
