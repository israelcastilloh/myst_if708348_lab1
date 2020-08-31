
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
import numpy as np
import yfinance as yf
from functions import *

path = '/Users/israelcastillo/Documents/m_st/myst_if708348_lab1/files/NAFTRAC_holdings'

def read_csv_files():
    files = file_walker(path)
    data_dict = {}
    for file in files:
        dates_dict = pd.read_csv(path+"/"+file, usecols=[1], nrows=1, header=None)
        dates_dict = clean_dates(str(dates_dict.iloc[0,0]))
        data_dict[dates_dict] = pd.read_csv(path+"/"+file, usecols=[0,1,3,4], skiprows=[0, 1]).dropna()
    return order_Dates_dict(data_dict)

def normalized_data(data_dict):
    for file in data_dict:
        #data_dict[file] = data_dict[file].drop(columns="Nombre", axis=0)
        data_dict[file]["Ticker"] = clean_tickers(data_dict, file)
        data_dict[file]["Precio"] = data_dict[file]["Precio"].replace(',','', regex=True).astype(float)
        data_dict[file]["Peso (%)"] = (data_dict[file]["Peso (%)"].astype(float))/100
    return data_dict

def get_global_tickers(normalized_data_dict):
    global_tickers = []
    for file in normalized_data_dict: global_tickers += normalized_data_dict[file]["Ticker"].tolist()
    return np.unique(global_tickers)

def get_first_tickers(normalized_data_dict):
    first_tickers = list(normalized_data_dict.values())[0]["Ticker"].tolist()
    first_tickers.remove('MXN CASH')
    first_tickers.remove('MXN CASH')
    first_tickers.remove('MXN CASH')
    return first_tickers

def get_rebalance_dates(normalized_data_dict):
    date_values = list(normalized_data_dict.keys())
    for i in range(len(date_values)):
        date_values[i]=str(datetime.strptime(date_values[i], '%d-%m-%Y').strftime('%Y-%m-%d'))
    return date_values

def yf_downloader(first_tickers, first_date, last_date):
    yf_data = {}
    for tickers in first_tickers:
        yf_data[tickers] = yf.download(tickers, start=first_date, end=last_date, interval = "1d", auto_adjust = True, prepost = True)
        route = str(tickers)
        yf_data[tickers].to_pickle(("/Users/israelcastillo/Documents/m_st/myst_if708348_lab1/files/"+route+".pkl"))

def data_passive_investment(ticker_to_yf, rebalance_date_values):
    data_yf={}
    rebalance_dates_prices={}
    condensed_df = []
    for ticker in ticker_to_yf:
        route = str(ticker)
        data_yf[ticker]=  pd.read_pickle(("/Users/israelcastillo/Documents/m_st/myst_if708348_lab1/files/"+route+".pkl"))
        data_yf[ticker] = data_yf[ticker][["Close"]].reset_index()
        data_yf[ticker] = data_yf[ticker][::-1].set_index("Date").rename(columns={"Close": ticker})
        rebalance_dates_prices[ticker] = pd.DataFrame()
        for date in rebalance_date_values:
            rebalance_dates_prices[ticker] = rebalance_dates_prices[ticker].append(data_yf[ticker][date])
    for i in range(len(ticker_to_yf)):
        condensed_df.append(list(rebalance_dates_prices.values())[i])
    condensed_df = pd.concat(condensed_df, axis=1).T
    condensed_df.loc['MXN CASH'] = 1
    condensed_df.index.names=["Ticker"]
    return condensed_df.sort_index()

def first_month_weightprice_calc(normalized_data_dict, passive_investment_historical_prices):
    first_month_weightprice = list(normalized_data_dict.values())[0][['Ticker', 'Peso (%)']].groupby('Ticker')['Peso (%)'].sum().sort_index()
    first_month_weightprice = pd.concat([first_month_weightprice, pd.DataFrame(passive_investment_historical_prices['2018-01-31'])], axis=1)
    first_month_weightprice['Capital Ponderado'] = first_month_weightprice['Peso (%)']*1000000
    first_month_weightprice['Títulos'] = (first_month_weightprice['Capital Ponderado']/first_month_weightprice.iloc[:,1]).round()
    return first_month_weightprice
