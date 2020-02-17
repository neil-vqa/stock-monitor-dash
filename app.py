from iexfinance.stocks import get_market_most_active
from iexfinance.stocks import get_market_gainers
from iexfinance.stocks import get_market_losers
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as do
from plotly.subplots import make_subplots
import streamlit as st
from st_rerun import rerun

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
	
	symbol = [data[0]['symbol'],data[1]['symbol'],data[2]['symbol']]
	df = yf.download(symbol,period='6mo',interval='1d',group_by='ticker',auto_adjust=True)

	data1 = df[symbol[0]]
	data2 = df[symbol[1]]
	data3 = df[symbol[2]]

	sub0 = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'},{'type':'domain'},{'type':'domain'}]])
	sub0.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= data[0]['latestPrice'],
			delta= {'reference': data[0]['previousClose'], 'relative': True},
			title = {"text": "<span style='font-size:0.95em;color:black'>{} | {}</span><br><span style='font-size:0.7em;color:gray'>{}</span>".format(data[0]['companyName'],symbol[0],data[0]['primaryExchange'])}
		), row=1, col=1
	)
	sub0.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= data[1]['latestPrice'],
			delta= {'reference': data[1]['previousClose'], 'relative': True},
			title = {"text": "<span style='font-size:0.95em;color:black'>{} | {}</span><br><span style='font-size:0.7em;color:gray'>{}</span>".format(data[1]['companyName'],symbol[1],data[1]['primaryExchange'])}
		), row=1, col=2
	)
	sub0.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= data[2]['latestPrice'],
			delta= {'reference': data[2]['previousClose'], 'relative': True},
			title = {"text": "<span style='font-size:0.95em;color:black'>{} | {}</span><br><span style='font-size:0.7em;color:gray'>{}</span>".format(data[2]['companyName'],symbol[2],data[2]['primaryExchange'])}
		), row=1, col=3
	)
	sub0.update_layout(margin= do.layout.Margin(t=60,b=0), plot_bgcolor='#EAEAEA', paper_bgcolor='#F2F2F2', height=240)

	sub1 = make_subplots(rows=2, cols=2,
		specs= [
			[{"rowspan": 2}, {}],
			[None, {}]
		], subplot_titles=('Price ({})'.format(data[0]['companyName']), 'Volume ({})'.format(data[0]['companyName']), 'Price Trend Comparison'), horizontal_spacing=0.04)
		
	sub1.add_trace(
		do.Scatter(
			x= data1.index,
			y= data1['Close'],
			name='Close',
			fill='tozeroy',
			mode='lines',
			marker_color='#2e7ec8'
		), row=1, col=1
	)
	sub1.add_trace(
		do.Bar(
			x= data1.index,
			y= data1['Volume'],
			name='Volume',
			marker_color='#2e7ec8'
		), row=1, col=2
	)
	sub1.add_trace(
		do.Scatter(
			x= data1.index,
			y= data1['Close'],
			name= symbol[0],
			marker_color='#2e7ec8'
		), row=2, col=2
	)
	sub1.add_trace(
		do.Scatter(
			x= data2.index,
			y= data2['Close'],
			name= symbol[1],
			marker_color='#3EBE51'
		), row=2, col=2
	)
	sub1.add_trace(
		do.Scatter(
			x= data3.index,
			y= data3['Close'],
			name= symbol[2],
			marker_color='#777877'
		), row=2, col=2
	)

	sub1.update_yaxes(showgrid=True,gridcolor='#F4EFEB',gridwidth=0.5, row=1, col=1)
	sub1.update_layout(margin= do.layout.Margin(t=30,b=15,r=0,l=0), showlegend=False, plot_bgcolor='#ffffff', hovermode='x')

	st.markdown('<h1 style="color:#017cbf; font-family:roboto;">MARKET MOVERS</h1> Trading as of ' + str(datay[0]['latestTime']), unsafe_allow_html=True)
	refresh = st.button('Refresh Dashboard',key='refresh_but')
	if refresh:
		rerun()
		
	st.subheader('Top 3 Gainers of the Day')
	st.plotly_chart(sub0, use_container_width=True)
	st.plotly_chart(sub1, use_container_width=True)


	sub2 = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'},{'type':'domain'},{'type':'domain'}]])
	sub2.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= datax[0]['latestPrice'],
			delta= {'reference': datax[0]['previousClose'], 'relative': True},
			title = {"text": datax[0]['companyName']}
		), row=1, col=1
	)
	sub2.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= datax[1]['latestPrice'],
			delta= {'reference': datax[1]['previousClose'], 'relative': True},
			title = {"text": datax[1]['companyName']}
		), row=1, col=2
	)
	sub2.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= datax[2]['latestPrice'],
			delta= {'reference': datax[2]['previousClose'], 'relative': True},
			title = {"text": datax[2]['companyName']}
		), row=1, col=3
	)
	sub2.update_layout(margin= do.layout.Margin(t=40,b=0), plot_bgcolor='#EAEAEA', paper_bgcolor='#F2F2F2', height=200)


	st.markdown('-----------------------')
	st.subheader('Top 3 Losers of the Day')
	st.plotly_chart(sub2, use_container_width=True)


	sub3 = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'},{'type':'domain'},{'type':'domain'}]])
	sub3.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= datay[0]['latestPrice'],
			delta= {'reference': datay[0]['previousClose'], 'relative': True},
			title = {"text": datay[0]['companyName']}
		), row=1, col=1
	)
	sub3.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= datay[1]['latestPrice'],
			delta= {'reference': datay[1]['previousClose'], 'relative': True},
			title = {"text": datay[1]['companyName']}
		), row=1, col=2
	)
	sub3.add_trace(
		do.Indicator(
			mode= 'number+delta',
			value= datay[2]['latestPrice'],
			delta= {'reference': datay[2]['previousClose'], 'relative': True},
			title = {"text": datay[2]['companyName']}
		), row=1, col=3
	)
	sub3.update_layout(margin= do.layout.Margin(t=40,b=0), plot_bgcolor='#EAEAEA', paper_bgcolor='#F2F2F2', height=200)

	st.subheader('Top 3 Most Active of the Day')
	st.plotly_chart(sub3, use_container_width=True)
	st.markdown('Data Sources: Yahoo! Finance, IEX Cloud | Design by: nvqa')

	_max_width_()


if __name__ == '__main__':
	main()
