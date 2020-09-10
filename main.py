
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Lab 1                                                                                      -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: israecastilloh                                                                              -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/israelcastilloh/myst_if708348_lab1                                                                    -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
from data import *

###### CSV READER ######
data_dict = read_csv_files()

###### DATA FROM CSV FIXED AND PATCHED ######
normalized_data_dict = normalized_data(data_dict)

###### ALL TICKERS ON THE PERIOD STUDIES WITHIN THE NAFTRACK ######
global_tickers = get_global_tickers(normalized_data_dict)

# DATES NAFTRAC REBALANCES ######
rebalance_date_values = get_rebalance_dates(normalized_data_dict)

###### PASSIVE INVESTMENT ######
first_tickers = get_first_tickers(normalized_data_dict)
# data_yf = yf_downloader(first_tickers, '2018-01-31', '2020-08-24')
passive_investment_historical_prices  = data_passive_investment(first_tickers, rebalance_date_values)
first_month_weightprice = first_month_weightprice_calc(normalized_data_dict, passive_investment_historical_prices)
df_pasiva = portfolio_value(rebalance_date_values, first_month_weightprice, passive_investment_historical_prices)

###### ACTIVE INVESTMENT ######
first_month_weightprice_active = active_initializer(first_month_weightprice)
df_operaciones = signal_dates(first_month_weightprice_active, rebalance_date_values)
df_activa = portfolio_value_active(rebalance_date_values, first_month_weightprice_active, passive_investment_historical_prices, df_operaciones)
