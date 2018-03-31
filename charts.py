import pandas as pd
import plotly.graph_objs as go
import quandl
import plotly.plotly as py
import plotly.tools as tls

quandl.ApiConfig.api_key = '4znMPd7_HKFqDvStTZ7e'

df = pd.read_csv('Stock_data.csv')

#Pie Chart 1. = by Industries
indNames = df['Industry'].unique()
labels1 = indNames
values1 = [df.Industry.str.count(indNames[0]).sum(), df.Industry.str.count(indNames[1]).sum(),df.Industry.str.count(indNames[2]).sum(),
         df.Industry.str.count(indNames[3]).sum(), df.Industry.str.count(indNames[4]).sum(), df.Industry.str.count(indNames[5]).sum(),
         df.Industry.str.count(indNames[6]).sum(), df.Industry.str.count(indNames[7]).sum(), df.Industry.str.count(indNames[8]).sum(),
         ]


figure1 = {
	'data': [{
		'values' : values1,
		'labels' : labels1,
		"hole": .4,
	    "type": "pie",
	    "hoverinfo":"label+percent",
	    'textposition' : 'outside',
	    'marker' : {
	    	'colors': [ 'rgb(128,0,38)', 'rgb(189,0,38)', 'rgb(227,26,28)', 'rgb(252,78,42)', 'rgb(253,141,60)',
	    		'rgb(254,178,76)', 'rgb(254,217,118)', 'rgb(255,237,160)', 'rgb(255,255,204)' ]
	    }
	}],

	'layout' : {
		'title' : '<b>Industries<b>'
			}
	}


#Pie Chart 2,3 by Long/Short
figure1L = {
	'data': [{
		'values' : df.LongAbs,
		'labels' : df.StockName,
		"hole": .4,
	    "type": "pie",
	    "hoverinfo":"label+percent",
	    'textinfo' : 'none',
	}],

	'layout' : {
		'title' : '<b>Long Portfolio<b>',
		'annotations' : [{
				'showarrow' : False,
				'text' : '150%',
				'x': 0.5,
				'y' : 0.5
				}]
			}
	}

#3
figure1S = {
	'data': [{
		'values' : df.ShortAbs,
		'labels' : df.StockName,
		"hole": .4,
	    "type": "pie",
	    "hoverinfo":"label+percent",
	    'textinfo' : 'none',
	    'marker' : {
	    	'colors': 'Greens'
	    }
	}],
	'layout' : {
		'title' : 'Short Portfolio',
		'annotations' : [{
				'showarrow' : False,
				'text' : '50%',
				'x': 0.5,
				'y' : 0.5
				}]
			}
	}


#map

dfg=df.CountryCode.value_counts().to_frame()
dfg.columns=({'Number of stocks',})
dfg['Code']=dfg.index
data = [ dict(
        type = 'choropleth',
        locations = dfg['Code'],
        z = dfg['Number of stocks'],
        text = dfg['Code'],
        colorscale = [[0, 'rgb(0,68,27)'], [0.25, 'rgb(0,109,44)'],[0.5, 'rgb(35,139,69)'], [0.75, 'rgb(65,171,93)'],
        [1, 'rgb(116,196,118)'],],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 2
            )),
        colorbar = dict(
            title = 'Number of stocks by country',)
      )]

layout = dict(
   		title = '<b>This map indicates where the stocks of your hedge fund are coming from!<b>',
   		showframe =False,
    geo = dict(
        showframe = False,
        showcountries=True,
        showlakes = True,
        showland = True,
            landcolor = 'rgb(229,245,224)',
            subunitcolor = 'rgb(229,245,224)',
            countrycolor = 'rgb(229,245,224)',),
)

mapp = dict( data=data, layout=layout )

if __name__ == '__main__':
    app.run_server()