
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

path = '/Users/israelcastillo/Documents/m_st/myst_if708348_lab1/files/NAFTRAC_holdings'

def file_walker():
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                files.append(os.path.join(file))
    return files

def read_csv():
    files = file_walker()
    data_dict = {}
    date_dict = {}
    for file in files:
        local_path = path+"/"+file
        date_dict = pd.read_csv(local_path, usecols=[1], nrows=0)
        data_dict[file] = pd.read_csv(local_path, usecols=[0,1,3,4], skiprows=[0, 1])
        data_dict[file] = data_dict[file].replace(',','', regex=True)
    #print(data_dict)
    return data_dict

def calculate_returns():
    capital = 1000000
    data_dict = read_csv()
    price_weight = {}
    for file in data_dict:
        data_df = data_dict[file]
        price_weight[file] = data_df[["Peso (%)", "Precio"]].dropna().apply(pd.to_numeric)
        #print(price_weight[file])
        price_weight[file]["Peso (%)"] = price_weight[file]["Peso (%)"].div(100)
        price_weight[file]["Peso Ponderado"] = price_weight[file]["Peso (%)"] * price_weight[file]["Precio"]
        price_weight[file] = price_weight[file].sum()
        print(price_weight[file])
