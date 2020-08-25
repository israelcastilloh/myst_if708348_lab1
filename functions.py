
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
import pandas as pd
import xlrd
from collections import OrderedDict
from datetime import datetime

path = '/Users/israelcastillo/Documents/m_st/myst_if708348_lab1/files/NAFTRAC_holdings'

def file_walker():
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

def read_csv():
    files = file_walker()
    data_dict = {}
    for file in files:
        local_path = path+"/"+file
        date_dict = pd.read_csv(local_path, usecols=[1], nrows=1, header=None)
        date_dict = clean_dates(str(date_dict.iloc[0,0]))
        data_dict[date_dict] = pd.read_csv(local_path, usecols=[0,1,3,4], skiprows=[0, 1]).replace(',','', regex=True)
    data_dict = order_Dates_dict(data_dict)
    return data_dict

def calculate_returns():
    data_dict = read_csv()
    price_weight = {}
    for file in data_dict:
        data_df = data_dict[file]
        price_weight[file] = data_df[["Peso (%)", "Precio"]].dropna().apply(pd.to_numeric)
        price_weight[file]["Peso (%)"] = price_weight[file]["Peso (%)"].div(100)
        price_weight[file]["Peso Ponderado"] = price_weight[file]["Peso (%)"] * price_weight[file]["Precio"]
        price_weight[file] = price_weight[file].sum()
        print(price_weight[file])
