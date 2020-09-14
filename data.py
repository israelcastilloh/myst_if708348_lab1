
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
import warnings
#pd.set_option('display.max_rows', None)
warnings.filterwarnings('ignore')
from pathlib import Path
import os


path = "/files/NAFTRAC_holdings"
start = "/"
relative_path = os.path.relpath(path, start)
path = relative_path

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
        data_dict[file]["Ticker"] = clean_tickers(data_dict, file)
        data_dict[file]["Precio"] = data_dict[file]["Precio"].replace(',','', regex=True).astype(float)
        data_dict[file]["Peso (%)"] = (data_dict[file]["Peso (%)"].astype(float))/100
        data_dict[file] = data_dict[file].set_index("Ticker").sort_index()
        data_dict[file] = data_dict[file].reset_index()
    return data_dict

def compiled_norm(data):
    data = pd.concat(data, axis=1)
    return data

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
    print(first_tickers)
    for tickers in first_tickers:
        print(tickers)
        yf_data[tickers] = yf.download(tickers, start=first_date, end=last_date, actions=False, interval = "1d", auto_adjust = False, prepost = False)
        route = str(tickers)
        yf_data[tickers].to_pickle(("/Users/israelcastillo/Documents/m_st/myst_if708348_lab1/files/"+route+".pkl"))

def data_passive_investment(ticker_to_yf, rebalance_date_values):
    data_yf={}
    rebalance_dates_prices={}
    condensed_df = []
    for ticker in ticker_to_yf:
        route = str(ticker)
        #data_yf[ticker]=  yf.download(ticker, start='2018-01-31', end='2020-08-24', actions=False, interval = "1d", auto_adjust = False, prepost = False)
        data_yf[ticker] = pd.read_pickle(("/Users/israelcastillo/Documents/m_st/myst_if708348_lab1/files/"+route+".pkl"))
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
    first_month_weightprice.iloc[:,1] = first_month_weightprice.iloc[:,1]
    first_month_weightprice['Peso (%)'] = first_month_weightprice['Peso (%)'].astype(float)
    first_month_weightprice.loc['MXN CASH']['Peso (%)'] = 0.0431001
    first_month_weightprice['Capital Ponderado'] = 0
    for i in range(len(first_month_weightprice['Capital Ponderado'])):
        first_month_weightprice.iloc[i,2] = (first_month_weightprice.iloc[i,0]*float(1000000)).round(4)
    #first_month_weightprice['Títulos'] = (first_month_weightprice['Capital Ponderado']/first_month_weightprice.iloc[:,1]).apply(np.floor)
    first_month_weightprice['Comisión'] = ((first_month_weightprice['Capital Ponderado']/first_month_weightprice.iloc[:,1]).apply(np.floor) * first_month_weightprice.iloc[:,1] * 0.00125)
    first_month_weightprice.loc['MXN CASH']['Comisión'] = 0
    first_month_weightprice['Capital - Comision'] = (first_month_weightprice['Capital Ponderado'] - first_month_weightprice['Comisión'])
    first_month_weightprice['Títulos P.'] = (first_month_weightprice['Capital - Comision']/first_month_weightprice.iloc[:,1]).apply(np.floor)
    first_month_weightprice.loc['MXN CASH']['Títulos P.'] = first_month_weightprice.loc['MXN CASH']['Peso (%)']*1000000
    first_month_weightprice['Postura.'] = (first_month_weightprice['Títulos P.']*first_month_weightprice.iloc[:,1])
    return first_month_weightprice

def portfolio_value_pas(rebalance_date_values, first_month_weightprice, passive_investment_historical_prices):
    portfolio_value=pd.DataFrame()
    for i in range(1, len(rebalance_date_values)+1):
        titles_per_ticker = first_month_weightprice['Títulos P.'] * passive_investment_historical_prices.iloc[:,i-1]
        portfolio_value[0] = ["2020-01-30", 1000000]
        portfolio_value[i] = [rebalance_date_values[i-1], titles_per_ticker.sum()]
    portfolio_value = portfolio_value.T
    portfolio_value = portfolio_value.rename(columns={0: "timestamp", 1: "capital"})
    portfolio_value["capital"] = portfolio_value["capital"].astype(float).round(2)-4
    portfolio_value["return"] = 0
    portfolio_value["rend_acum"] = 0
    for i in range(1, len(rebalance_date_values)+1):
        portfolio_value.iloc[0,1] = 1000000
        portfolio_value.iloc[i,2] = (portfolio_value["capital"][i]/portfolio_value["capital"][i-1]-1).round(4)
        portfolio_value.iloc[0,3] = 0
        portfolio_value.iloc[i,3] = round(portfolio_value.iloc[i,2] + portfolio_value.iloc[i-1,3],4)
    return portfolio_value

def active_initializer(data):
    data = data.iloc[:, [0,1]]
    maxValueIndexObj = data.idxmax()
    max_weight_ticker = maxValueIndexObj["Peso (%)"]
    data.loc[max_weight_ticker]["Peso (%)"]  = data.loc[max_weight_ticker]["Peso (%)"]/2
    data.loc['MXN CASH']['Peso (%)'] = data.loc['MXN CASH']['Peso (%)']+ (1-data.sum()["Peso (%)"])
    data['Capital Ponderado'] = 1000000*data['Peso (%)']
    data['Títulos'] = data['Capital Ponderado']/data.iloc[:,1]
    data['Comisión'] = (data['Capital Ponderado']/data.iloc[:,1] * data.iloc[:,1] * 0.00125)
    data.loc['MXN CASH']['Comisión'] = 0
    data['Capital - Comision'] = (data['Capital Ponderado'] - data['Comisión'])
    data['Títulos P.'] = (data['Capital - Comision']/data.iloc[:,1]).apply(np.floor)
    data['Postura.'] = (data['Títulos P.']*data.iloc[:,1])
    return data


def signal_dates(first_month_weightprice_active, rebalance_date_values):
    #signal_dates = yf.download("AMXL.MX", start='2018-01-31', end='2020-08-24', actions=False,
    #interval = "1d", auto_adjust = False, prepost = False)
    #signal_dates = signal_dates[["Open", "Close"]]
    #signal_dates = signal_dates.drop(["Open"], axis=1)
    #signal_dates.to_pickle(("/Users/israelcastillo/Documents/m_st/myst_if708348_lab1/files/"+"SignalDates"+".pkl"))
    cash_available = 109402.86
    signal_dates = pd.read_pickle(("/Users/israelcastillo/Documents/m_st/myst_if708348_lab1/files/"+"SignalDates"+".pkl")).round(2)
    signal_dates["Buy?"] = "Nothing"
    signal_dates["precio"] = 0
    signal_dates["Cash"] = cash_available
    signal_dates["Diff"] = 0
    signal_dates["Inversion"] = 0
    signal_dates["Titulos"] = 0
    signal_dates["comision"] = 0
    signal_dates["I - C"] = 0
    signal_dates["titulos_c"] = 0
    signal_dates["titulos_t"] = 0
    signal_dates["c_acum"] = 0
    for i in range(1, len(signal_dates)):
        signal_dates.iloc[0,2] = "Buy"
        signal_dates.iloc[0,3] = signal_dates.iloc[0,1]
        signal_dates.iloc[0,7] = 3811
        signal_dates.iloc[0,8] = signal_dates.iloc[0,7] * signal_dates.iloc[0,3] * .00125
        signal_dates.iloc[i,4] = signal_dates.iloc[i-1,4]
        signal_dates.iloc[0,10] = signal_dates.iloc[0,7]
        signal_dates.iloc[0,11] = signal_dates.iloc[0,7]
        signal_dates.iloc[0,12] = signal_dates.iloc[0,8]

        diff = (signal_dates.iloc[i-1,1]/signal_dates.iloc[i-1,0]-1)
        if diff < -.01:
            signal_dates.iloc[i,2] = "Buy"
            signal_dates.iloc[i,3] = signal_dates.iloc[i,0]
            signal_dates.iloc[i-1,5] = diff
            signal_dates.iloc[i,6] = signal_dates.iloc[i,4]*.10
            signal_dates.iloc[i,4] = signal_dates.iloc[i,4] - signal_dates.iloc[i,6]
            signal_dates.iloc[i,7] = signal_dates.iloc[i,6] / signal_dates.iloc[i,3]
            signal_dates.iloc[i,8] = (signal_dates.iloc[i,7] * signal_dates.iloc[i,3] * 0.00125)
            signal_dates.iloc[i,9] = signal_dates.iloc[i,6] - signal_dates.iloc[i,8]
            signal_dates.iloc[i,10] = signal_dates.iloc[i,9] / signal_dates.iloc[i,3]
        signal_dates.iloc[i,11] = signal_dates.iloc[i-1,11] + signal_dates.iloc[i,10]
        signal_dates.iloc[i,12] = signal_dates.iloc[i-1,12] + signal_dates.iloc[i,8]
    return signal_dates

def signal_dates_redux(data):
    data = data[["titulos_t", "titulos_c", "precio", "comision", "c_acum", "Cash"]]
    data["comision"] = data["comision"].round(2)
    data["c_acum"] = data["c_acum"].round(2)
    data["titulos_c"] = data["titulos_c"].apply(np.floor)
    data["titulos_t"] = data["titulos_t"].apply(np.floor)
    return data

def df_operaciones_f(data):
    data = signal_dates_redux(data)
    df_operaciones = pd.DataFrame()
    for i in range(0, len(data)):
        if data.iloc[i, 2] != 0:
            df_operaciones = df_operaciones.append(data.iloc[i, :])
    return df_operaciones

def portfolio_value_active(rebalance_date_values, first_month_weightprice_active,
passive_investment_historical_prices, signal_dates):
    signal_dates=signal_dates_redux(signal_dates)
    first_month_weightprice_active = first_month_weightprice_active[["Peso (%)", "Títulos P."]]
    signal_dates = signal_dates.T
    rebalances = {}
    titulos_acum = {}
    condensed_df = pd.DataFrame(columns=["capital", "return", "rend_acum"])
    for date in rebalance_date_values:
        rebalances[date] = first_month_weightprice_active
        rebalances[date]["Precios"] = passive_investment_historical_prices[date]
        titulos_acum[date] = signal_dates[date][['titulos_t', 'c_acum', 'Cash']]
        rebalances[date].iloc[4,1] = titulos_acum[date].loc['titulos_t']
        rebalances[date].iloc[24,1] = titulos_acum[date].loc['Cash']
        rebalances[date].iloc[24,0] = titulos_acum[date].loc['Cash']/1000000
        rebalances[date].iloc[4,0] = rebalances[date].iloc[4,0] + 1 - rebalances[date].sum().loc['Peso (%)']
        rebalances[date]["Postura"] = rebalances[date]['Títulos P.'] * rebalances[date]['Precios']
        value = rebalances[date].sum()["Postura"].round(2)
        condensed_df.loc[date] = value
    insert_line = pd.DataFrame({'capital' : 1000000}, index = ['2018-01-30'])
    condensed_df = pd.concat([insert_line, condensed_df])
    condensed_df['rend_acum'] = 0
    for i in range(0, len(condensed_df)):
        condensed_df.iloc[i,1] = ((condensed_df.iloc[i,0]/condensed_df.iloc[i-1,0])-1).round(4)
        condensed_df.iloc[0,1] = 0
        condensed_df.iloc[i,2] = condensed_df.iloc[i,1] + condensed_df.iloc[i-1,2]
    return condensed_df.reset_index()

def market_benchmarks(df_pasiva, df_activa):
    rf = 0.0770
    df_medidas = pd.DataFrame(index=['rend_m', 'rend_c', 'sharpe'],
                            columns=['descripcion', 'inv_activa', 'inv_pasiva'])
    df_medidas.loc['rend_m']['inv_activa'] = round(np.mean(df_activa['return']),4)
    df_medidas.loc['rend_m']['inv_pasiva'] = round(np.mean(df_pasiva['return']),4)
    df_medidas.loc['rend_c']['inv_activa'] = df_activa.iloc[-1,3]
    df_medidas.loc['rend_c']['inv_pasiva'] = df_pasiva.iloc[-1,3]
    df_medidas.loc['sharpe']['inv_activa'] = round((df_medidas.loc['rend_m']['inv_activa'] - rf/12)/ np.std(df_activa['return']),4)
    df_medidas.loc['sharpe']['inv_pasiva'] = round((df_medidas.loc['rend_m']['inv_pasiva'] - rf/12)/np.std(df_pasiva['return']),4)
    df_medidas.loc['rend_m']['descripcion'] = "Rendimiento Promedio Mensual"
    df_medidas.loc['rend_c']['descripcion'] = "Rendimiento Mensual Acumulado"
    df_medidas.loc['sharpe']['descripcion'] = "Sharpe Ratio"
    return df_medidas
