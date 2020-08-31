
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project:                                                                                            -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: israecastilloh                                                                              -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/israelcastilloh/myst_if708348_lab1                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import os
import csv
from datetime import datetime

def file_walker(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                files.append(os.path.join(file))
    return files

def clean_dates(str):
    str = str.replace("ene", "01")
    str = str.replace("feb", "02")
    str = str.replace("mar", "03")
    str = str.replace("abr", "04")
    str = str.replace("may", "05")
    str = str.replace("jun", "06")
    str = str.replace("jul", "07")
    str = str.replace("ago", "08")
    str = str.replace("sep", "09")
    str = str.replace("oct", "10")
    str = str.replace("nov", "11")
    str = str.replace("dic", "12")
    return str

def order_Dates_dict(data_dict):
    sorted_dict = sorted(data_dict.items(),key = lambda x:datetime.strptime(x[0], '%d-%m-%Y'), reverse=False)
    sorted_dict = [(sorted_dict[i]) for i in range(len(sorted_dict))]
    sort_cleaned_dict={}
    for data in sorted_dict: sort_cleaned_dict[data[0]] = data[1]
    return sort_cleaned_dict

def clean_tickers(data_dict, file):
    data_dict[file]["Ticker"] = data_dict[file]["Ticker"].str.replace('*','')+".MX"
    data_dict[file]["Ticker"] = data_dict[file]["Ticker"].str.replace('GFREGIOO', 'RA')
    data_dict[file]["Ticker"] = data_dict[file]["Ticker"].str.replace('KOFL', 'MXN')
    data_dict[file]["Ticker"] = data_dict[file]["Ticker"].str.replace('BSMXB', 'MXN')
    data_dict[file]["Ticker"] = data_dict[file]["Ticker"].str.replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX')
    data_dict[file]["Ticker"] = data_dict[file]["Ticker"].str.replace('MEXCHEM.MX', 'ORBIA.MX')
    data_dict[file]["Ticker"] = data_dict[file]["Ticker"].str.replace('MXN.MX', 'MXN CASH')
    data_dict[file]["Ticker"] = data_dict[file]["Ticker"].str.replace('USD.MX', 'USD CASH')
    return data_dict[file]["Ticker"]
