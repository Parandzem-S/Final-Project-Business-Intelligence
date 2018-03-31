import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go 
import quandl
import pandas as pd
import datetime
import datetime as dt
import flask
import os
from pandas_datareader.data import DataReader
import time
from charts import figure1, figure1L, figure1S, mapp


quandl.ApiConfig.api_key = '4znMPd7_HKFqDvStTZ7e'
stock_names=pd.read_csv("Stock_data.csv")
df=pd.read_csv('Stocks.csv') 
dfg=stock_names.CountryCode.value_counts().to_frame()
dfg.columns=({'Number of stocks',})
dfg['Code']=dfg.index


app=dash.Dash()
app.css.append_css({'external_url':'https://codepen.io/chriddyp/pen/bWLwgP.css'})

app.layout = html.Div([
#first row, the text
html.Div([
    html.Div([
        html.H2('150/50 Hedge Fund Dashboard for Clients',
            style={'display': 'inline-block','float': 'left','font-size': '2em','margin-left': '7px', 'marginTop': 0,'font-weight': 'bolder',
                       'font-family': 'Product Sans',
                       'color': "rgba(117, 117, 117, 0.95)"}),
        html.H3('Welcome back! Track your Investment Portfolio performance with this dash.',
                style={'display': 'inline-block','float': 'left','font-size': '1.5em','marginBottom': 150, 'marginTop': 0,
                       'font-family': 'Product Sans',
                       'color': "rgb(0, 143, 179)",
                       }),
               ], className = 'six columns', id = 'h'),
        html.Div([
            html.Img(src="https://cdn2.iconfinder.com/data/icons/complex-arrows-add-on-flat/48/Complex_Arrows-21-512.png",
                style={'height': '65px','float': 'left'}),
            html.H4('Return',style = {'margin' : 'center', 'marginTop': 0, 'font-family': 'Product Sans','color' : 'rgb(35,139,69)'}),
            html.P('4.49%', style={'marginTop': 0,'font-family': 'Product Sans','color' : '#005977','font-size': '1.65em','font-weight': 'bolder'})
], className = 'two columns'),
        html.Div([
             html.Img(src="https://cdn2.iconfinder.com/data/icons/complex-arrows-add-on-flat/48/Complex_Arrows-22-512.png",
                style={'height': '65px','float': 'left'}),
            html.H5('Variance',style = {'margin' : 'center', 'marginTop': 0,'font-family': 'Product Sans','color' : 'rgb(35,139,69)'}),
            html.P('0.08%', style={'marginTop': 0,'font-family': 'Product Sans','color' : '#005977', 'font-size': '1.65em','font-weight': 'bolder'})
], className = 'two columns'),
        html.Div([
            html.Img(src="https://cdn2.iconfinder.com/data/icons/complex-arrows-add-on-flat/48/Complex_Arrows-22-512.png",
                style={'height': '65px','float': 'left'}),
            html.H5('CVaR',style = {'margin' : 'center','marginTop': 0,'font-family': 'Product Sans','color' : 'rgb(35,139,69)'}),
            html.P('0.1%', style={'marginTop': 0,'font-family': 'Product Sans','color' : '#005977','font-size': '1.65em','font-weight': 'bolder'})
], className = 'two columns'),
], style = {'backgroundColor': '#D5F2EC', 'display': 'inline-block', 'height' : 100}, className = 'row'),

#2nd row, division for candlestick & text
    html.Div([
        html.Div([
            dcc.Graph(id='figure2')
            ],  className = 'seven columns'),
        html.Div([
            dcc.Dropdown(
            id='stock-ticker-input',
            options=[{'label': s, 'value': s} for s in stock_names.StockName],
            value=stock_names.StockName[0]),
            html.P("Please, select a stock"),
            ], style={'marginTop': 100}, className = 'two columns'),
        html.Div([
            html.P(children="STOCK SELECTION STRATEGY-GARP MODEL", style = {'font-size': '1.8em','fontWeight':'bold','margin' : 'center','font-family': 'Product Sans','color' : 'rgb(35,139,69)'}),
            html.Ol([html.Li(children="Combination of both value and growth investing", style={'fontWeight':'bold'}),
            html.Li(children='Companies that are both undervalued and have solid sustainable growth potential',style={'fontWeight':'bold'}),
            html.Li(children='P/E ratios in the range of 15-25',style={'fontWeight':'bold'}),
            html.Li(children='PEG is superior indicator for stock picking which is no higher than 1 and, in most cases, closer to 0.5',style={'fontWeight':'bold'})]),
            html.P(children="For more information about the method see:",style={'fontWeight':'bold'}),
            html.A('Investopedia.com',href= "https://www.investopedia.com/university/stockpicking/stockpicking5.asp",style={'fontWeight':'bold'}),
            ], className='three columns')
        ], className = 'row'),

#3RD ROW, market graph & industry pie chart
    html.Div([
        html.Div([
            dcc.Graph(id='figure5')
            ], className = 'seven columns'),
        html.Div([
            dcc.Graph(id = 'pie', figure = figure1)
            ], className = 'four columns')
        ], className = 'row'),
#4TH ROW, the mapp   
    html.Div([
        html.Div([
            dcc.Graph(id='figure3', figure=mapp)
            ], className = 'seven columns'),
        html.Div([
            dcc.RadioItems(
            id='option_in',
            options=[
            {'label':"Long Portfolio", 'value':'figure1L'},
            {'label':'Short Portfolio','value':'figure1S'},
            ], value='figure1L')
            ], style={'marginTop': 200}, className = 'one columns'),          
        html.Div(id='pies', className = 'four columns'),    
        ])
 ])


@app.callback(
    Output(component_id='figure2', component_property='figure'),
    [Input(component_id='stock-ticker-input', component_property='value')],
)

def update_graph_2(input_value):
    input1 = "WIKI/" + input_value
    df=quandl.get(input1,start_date="2017-1-1")  
    data = [dict(
    x = df.index,
    type = 'candlestick',
    open = df.Open,
    high = df.High,
    low = df.Low,
    close = df.Close,
    yaxis = 'y6',
    name = input_value,
    increasing = dict( line = dict( color = '#17BECF') ),
    decreasing = dict( line = dict( color = '#7F7F7F') ),
) ]

    layout=dict()
    fig = dict(data=data, layout=layout )
    fig['data'].append( dict( x=df.index, y=df.Volume,
                         type='bar', yaxis='y1', name='Volume'))

    fig['layout'] = dict()
    fig['layout']['plot_bgcolor'] = 'rgb(250, 250, 250)'
    fig['layout']['xaxis'] = dict( rangeselector = dict( visible = True ) )
    fig['layout']['yaxis'] = dict( domain = [0, 0.2], showticklabels = False )
    fig['layout']['yaxis2'] = dict( domain = [0.1, 0.9] )
    fig['layout']['legend'] = dict( orientation = 'h', y=1, x=0.3, yanchor='bottom' )
    fig['layout']['margin'] = dict( t=40, b=40, r=40, l=40 )
    
    rangeselector=dict(
    visibe = True,
    x = 0, y = 1,
    font = dict( size = 13 ),
    buttons=list([
        dict(count=1,
             label='reset',
             step='all'),
        dict(count=1,
            label='1mo',
            step='month',
            ),
        dict(count=6,
            label='6mo',
            step='month',
            stepmode='backward'),
        dict(count=1,
             label='1yr',
             step='year',
             stepmode='backward'),  
        dict(step='all')
    ]))
    fig['layout']['xaxis']['rangeselector'] = rangeselector
    return fig


#Stock comparison graph callback
@app.callback(
    Output(component_id='figure5', component_property='figure'),
    [Input(component_id='stock-ticker-input', component_property='value')],
)

def update_graph_5(input_value):
    input5 = "WIKI/" + input_value
    data= quandl.get(input5,start_date="2010-01-01")
    sp = quandl.get("MULTPL/SP500_REAL_PRICE_MONTH",start_date="2010-01-01")
    dj = quandl.get("BCB/UDJIAD1", start_date="2010-01-01")

    t1 = go.Scatter(x=dj.index, y= data.Close, mode = 'lines', name = input_value
        )
    t2 = go.Scatter(x=dj.index, y= sp.Value, mode = 'lines', name = 'S&P500'
        )
    t3 = go.Scatter(x=dj.index, y= dj.VALUE, mode = 'lines', name = 'Dow Jones'
        )
    data5=[t1, t2, t3]

    layout5 = dict(
    title='<b>Stock Prices vs. Market Indices<b>',
    legend = dict(orientation = 'h', y=1, x=0.3),
    margin = dict( t=40, b=40, r=40, l=40 ),
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='reset',
                     step='all'),
                dict(count=1,
                     label='1mo',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6mo',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                    label='1yr',
                    step='year',
                    stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date'
    )
)
    figure5 = dict(data=data5, layout = layout5)
    return figure5

#Radio-plots
@app.callback(
    Output(component_id='pies', component_property='children'),
    [Input(component_id='option_in', component_property='value')]
)

def update_graph_1(selected_values):
    graphs=[]
    if 'figure1L' in selected_values:
        graphs.append(dcc.Graph(id='figure1L', figure=figure1L)),
    if 'figure1S' in selected_values:
        graphs.append(dcc.Graph(id='figure1S', figure=figure1S))  
    return graphs

if __name__ == '__main__':
    app.run_server()
