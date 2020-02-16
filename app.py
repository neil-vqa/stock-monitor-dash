from alpha_vantage.timeseries import TimeSeries
from iexfinance.stocks import get_market_most_active
from iexfinance.stocks import get_market_gainers
from iexfinance.stocks import get_market_losers
import pandas as pd
import numpy as np
import plotly.graph_objects as do
from plotly.subplots import make_subplots
import streamlit as st

alpha_key = 'VQIPM38V4L0GPAL2'
bar_api = 'a2285049282b7e58dcbdcb3514497889'
iex_key = 'pk_e682e00599c744d9bb4d6686d4ee7549'


def _max_width_():
    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

def main():
	data = get_market_gainers(token=iex_key)
	datax = get_market_losers(token=iex_key)
	datay = get_market_most_active(token=iex_key)

	ticks = [data[0]['symbol'], data[1]['symbol'], data[2]['symbol']]

	ts = TimeSeries(key= alpha_key, output_format='pandas')

	data1, meta_data1 = ts.get_daily_adjusted(symbol=ticks[0])
	data2, meta_data2 = ts.get_daily_adjusted(symbol=ticks[1])
	data3, meta_data3 = ts.get_daily_adjusted(symbol=ticks[2])


	sub0 = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'},{'type':'domain'},{'type':'domain'}]])
	sub0.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= data[0]['latestPrice'],
			delta= {'reference': data[0]['previousClose']},
			title = {"text": '1 | {} | {}'.format(data[0]['companyName'],ticks[0])}
		), row=1, col=1
	)
	sub0.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= data[1]['latestPrice'],
			delta= {'reference': data[1]['previousClose']},
			title = {"text": '2 | {} | {}'.format(data[1]['companyName'],ticks[1])}
		), row=1, col=2
	)
	sub0.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= data[2]['latestPrice'],
			delta= {'reference': data[2]['previousClose']},
			title = {"text": '3 | {} | {}'.format(data[2]['companyName'],ticks[2])}
		), row=1, col=3
	)
	sub0.update_layout(margin= do.layout.Margin(t=40,b=0), plot_bgcolor='#EAEAEA', paper_bgcolor='#F2F2F2', height=200)


	sub1 = make_subplots(rows=2, cols=2,
		specs= [
			[{"rowspan": 2}, {}],
			[None, {}]
		], subplot_titles=('Price ({})'.format(data[0]['companyName']), 'Volume ({})'.format(data[0]['companyName']), 'Price Trend Comparison'), horizontal_spacing=0.04)
		
	sub1.add_trace(
		do.Scatter(
			x= data1.index,
			y= data1['4. close'],
			name='Close',
			fill='tozeroy',
			mode='lines',
			marker_color='#2e7ec8'
		), row=1, col=1
	)
	sub1.add_trace(
		do.Bar(
			x= data1.index,
			y= data1['6. volume'],
			name='Volume',
			marker_color='#2e7ec8'
		), row=1, col=2
	)
	sub1.add_trace(
		do.Scatter(
			x= data1.index,
			y= data1['4. close'],
			name= ticks[0],
			marker_color='#2e7ec8'
		), row=2, col=2
	)
	sub1.add_trace(
		do.Scatter(
			x= data2.index,
			y= data2['4. close'],
			name= ticks[1],
			marker_color='#3EBE51'
		), row=2, col=2
	)
	sub1.add_trace(
		do.Scatter(
			x= data3.index,
			y= data3['4. close'],
			name= ticks[2],
			marker_color='#777877'
		), row=2, col=2
	)

	sub1.update_yaxes(showgrid=True,gridcolor='#F4EFEB',gridwidth=0.5, row=1, col=1)
	sub1.update_layout(margin= do.layout.Margin(t=30,b=15,r=0,l=0), showlegend=False, plot_bgcolor='#ffffff', hovermode='x')

	st.title('Stock Monitoring')
	st.markdown('Trading as of ' + str(datay[0]['latestTime']))
	st.subheader('Top 3 Market Gainers of the Day')
	st.plotly_chart(sub0, use_container_width=True)
	st.plotly_chart(sub1, use_container_width=True)


	sub2 = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'},{'type':'domain'},{'type':'domain'}]])
	sub2.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= datax[0]['latestPrice'],
			delta= {'reference': datax[0]['previousClose']},
			title = {"text": datax[0]['companyName']}
		), row=1, col=1
	)
	sub2.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= datax[1]['latestPrice'],
			delta= {'reference': datax[1]['previousClose']},
			title = {"text": datax[1]['companyName']}
		), row=1, col=2
	)
	sub2.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= datax[2]['latestPrice'],
			delta= {'reference': datax[2]['previousClose']},
			title = {"text": datax[2]['companyName']}
		), row=1, col=3
	)
	sub2.update_layout(margin= do.layout.Margin(t=40,b=0), plot_bgcolor='#EAEAEA', paper_bgcolor='#F2F2F2', height=200)


	st.markdown('-----------------------')
	st.subheader('Top 3 Market Losers of the Day')
	st.plotly_chart(sub2, use_container_width=True)


	sub3 = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'},{'type':'domain'},{'type':'domain'}]])
	sub3.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= datay[0]['latestPrice'],
			delta= {'reference': datay[0]['previousClose']},
			title = {"text": datay[0]['companyName']}
		), row=1, col=1
	)
	sub3.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= datay[1]['latestPrice'],
			delta= {'reference': datay[1]['previousClose']},
			title = {"text": datay[1]['companyName']}
		), row=1, col=2
	)
	sub3.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= datay[2]['latestPrice'],
			delta= {'reference': datay[2]['previousClose']},
			title = {"text": datay[2]['companyName']}
		), row=1, col=3
	)
	sub3.update_layout(margin= do.layout.Margin(t=40,b=0), plot_bgcolor='#EAEAEA', paper_bgcolor='#F2F2F2', height=200)

	st.subheader('Top 3 Most Active of the Day')
	st.plotly_chart(sub3, use_container_width=True)
	st.markdown('Data Sources: Alpha Vantage, IEX Cloud | Design by: nvqa')

	_max_width_()


if __name__ == '__main__':
	main()
