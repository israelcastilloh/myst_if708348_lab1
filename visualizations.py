
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
from main import *
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objects as go

fig_active_pasive = go.Figure(data=[
go.Scatter(x=df_activa.reset_index()['index'], y=df_activa['capital'], name="Inv Activa $"),
go.Scatter(x=df_pasiva.reset_index()['timestamp'], y=df_pasiva['capital'], name="Inv Pasiva $"),
])

fig_active_pasive_return = go.Figure(data=[
go.Scatter(x=df_activa.reset_index()['index'], y=df_activa['rend_acum'], name="Inv Activa %"),
go.Scatter(x=df_pasiva.reset_index()['timestamp'], y=df_pasiva['rend_acum'], name="Inv Pasiva %"),
])

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "Notebook Lab.1"
app.layout = html.Div(children=[

    dbc.Row([html.Img(src=
            "http://oci02.img.iteso.mx/identidad_de_instancia_2018/ITESO/Logos%20ITESO/Logo-ITESO-Principal.jpg",
            className="image")]),

    dbc.Row([
        html.H1("Ingeniería Financiera", className = "text1")]),
    dbc.Row([
        html.H1("ITE1731 - Microestructura y Sistemas de Trading", className = "text1")]),
    dbc.Row([
        html.H1("I.F. Israel Castillo-Herrera", className = "text1")]),
    dbc.Row([
        html.H2("Septiembre 2020", className = "text1")]),
    dbc.Row([
        html.A("GitHub Repo", href= "https://github.com/israelcastilloh/myst_if708348_lab1" , className = "text1")]),
    dbc.Row([
        html.H1("Laboratorio 1", className = "text1")]),
    dbc.Row([
        html.H2("Inversión de Capital", className = "text1")]),

    dbc.Row([html.Img(src=
            "https://cdn-3.expansion.mx/dims4/default/299d7f5/2147483647/strip/true/crop/1200x675+0+0/resize/1800x1013!/quality/90/?url=https%3A%2F%2Fcdn-3.expansion.mx%2F79%2F1d%2F765452624ce7bacea969565ee9d1%2Fxpa-web-bolsa-mexicana-de-valores-ja-004-1.jpg",
            className="image2")]),


    dbc.Row([
        html.H1("Abstract", className = "subtext_medium")]),

    dbc.Row([
        html.P("Este documento fue elaborado por  Israel Castillo-Herrera, como un trabajo parcial para la materia de Microestructura y \
         Sistemas de Trading - ITE1731, la cual es parte del curriculum de la licenciatura en Ingeniería Financiera, ofertada por la universidad ITESO. En el presente trabajo se plantea la respuesta a la siguiente pregutna: ¿Qué estrategia de inversión propondrías si tu trabajo fuera administrar 1 Millón de pesos?",
        className = "small-text")]),

    dbc.Row([
        html.H1("0. Librerías y Dependencias", className = "subtext_medium")]),

    dbc.Row([
        html.H2("0.1 Librerías", className = "subtext")]),

    dbc.Row([
        html.P(" Para correr este notebook es necesario tener instaladas y/o en el archivo requirements.txt las siguientes librerías :",
        className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        * dash==1.14.0
        * pandas==1.0.5
        * numpy>=1.19.1
        * yfinance>=0.1.54
        '''
        ,className = "small-text")]),

    dbc.Row([
        html.H2("0.2 Dependencias", className = "subtext")]),
    dbc.Row([
        html.P(" Para correr este notebook es necesario contar con los siguientes archivos y dependencias externas:",
        className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        * /files/NAFTRAC_holdings
        * /files/NAFTRAC_holdings.zip
        '''
        ,className = "small-text")]),

    dbc.Row([
        html.H1("1. Introducción", className = "subtext_medium")]),

    dbc.Row([
        html.P("NAFTRAC fue creado en el año 2002 por Nacional Financiera, \
        una Sociedad Nacional de Crédito, que promueve el ahorro y la inversión,\
        el objetivo principal de listarlo era posicionarlo como un referente del mercado mexicano a nivel global.\
        De esta manera se nos permite replicar el comportamiento del mercado Mexicano. \
        Cada una de las empresas listadas que forman parte \
        del Índice tiene una ponderación que generan un correspondiente retorno acumulado para el índice. \
        El resultado de rendimiento ponderado de cada emisora en conjunto conlleva un rendimiento diversificado del mercado. \
        ",
        className = "small-text")]),

    dbc.Row([
        html.H1("2. Objetivos", className = "subtext_medium")]),

    dbc.Row([
        html.P("El objetivo de este proyecto era el crear de  manera programática una estrategia que \
        pudiera servir de referencia para evaluar los rendimientos de inversión a través del tiempo \
        usando dos alocaciones de activos diferentes. En una, que nombramos pasivos, alocamos las ponderaciones de los activos \
        de la misma forma en la que están compuestos en el NAFTRAC, tomando los pesos de una primera fecha para armar nuestro portafolio. \
        La otra forma que se hizo, fue la que nombramos la inversión activa. En esta, tomamos como referencia el activo con mayor peso de alocación \
        y le restamos la mitad de su alocación de capital a la mitad, para posteriormente ir comprando más titulos, dependiendo de \
        una parametrización de cambios de precio durante el tiempo del NAFTRAC (si bajaba 1% o más el día anterior era señal de compra). \
        Con el objetivo de evaluar que hacer con $1,000,000 MXN. Como invertirlos. Ver que opciones son las mejores y como se compara la inversión de manejo activo vs. pasivo.\
        ",
        className = "small-text")]),

    dbc.Row([
        html.H1("3. Datos", className = "subtext_medium")]),

    dbc.Row([
        html.P("Dentro de la carpeta de /files/NAFTRAC_holdings, se alocan todos los archivos \
        de datos de ponderaciones de cada mes desde el 31-01-2018 hasta el 21-08-2020. Obtenidos de la página oficial de BlackRock. \
        En formato Excel. Estos documentos contienen las ponderaciones de rebalanceos del NAFTRAC y los precios dados a cada emisora en el momento de la fecha de rebalanceo. \
        Esta información es importante ya que queremos saber que % darle a cada emisora para invertir nuestro capital. Lo que se hizo fue leer cada archivos CSV de manera recursiva y comenzar a guardar todo en diccionarios y dataframes. \
        ",
        className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
        from data import *

        ###### CSV READER ######
        data_dict = read_csv_files()

        ###### DATA FROM CSV FIXED AND PATCHED ######
        normalized_data_dict = normalized_data(data_dict)
        '''
        ,className = "code-block")]),

    dbc.Row([
        html.P("Donde: ",
        className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
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

        '''
        ,className = "code-block")]),


    dbc.Row([
        html.P("Este manejo de datos nos permite obtener la correspondiente tabla como DataFrame, de manera ordenada cronológicamente. Y ajustada al estilo datetime. \
        ",
        className = "small-text")]),

    dbc.Container(
        dbc.Table.from_dataframe(compiled_norm.round(2), striped=True, bordered=True, hover=True),
        style={'height': '500px', 'overflowY': 'auto'}, className="table"),

    dbc.Row([
        html.P("Siguiente, quise obtener las FECHAS en donde ocurren los REBALANCEOS. Como marcadores de inversión, y tambien para el manejo de precios a través de los meses. \
        ",
        className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
        # DATES NAFTRAC REBALANCES ######
        rebalance_date_values = get_rebalance_dates(normalized_data_dict)
        $
        ['2018-01-31', '2018-02-28', '2018-03-28', '2018-04-30', '2018-05-31' [...]
        '2020-04-30', '2020-05-29', '2020-06-30', '2020-07-31', '2020-08-21']
        '''
        ,className = "code-block")]),

    dbc.Row([
        html.P("Donde:  \
        ",
        className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
        def get_rebalance_dates(normalized_data_dict):
            date_values = list(normalized_data_dict.keys())
            for i in range(len(date_values)):
                date_values[i]=str(datetime.strptime(date_values[i], '%d-%m-%Y').strftime('%Y-%m-%d'))
            return date_values
        '''
        ,className = "code-block")]),


    dbc.Row([
        html.H1("4. Proceso", className = "subtext_medium")]),

    dbc.Row([
        html.H2("4.1 Inversión Pasiva", className = "subtext")]),

    dbc.Row([
        html.P("La inversión pasiva consideramos la ponderación y los TICKERS de cada emisora del primer mes  \
        de la lista de rebalanceos obtenidos de los CSV. Que sería el ['2018-01-31']. \
        Con esto fue como decidimos alocar nuestro $1,000,000 y dejar el portafolio\
        evaluarse durante el periodo de estudio. Sin hacer modificaciones extra.\
        ",
        className = "small-text")]),

    dbc.Row([
        html.P("Las emisoras, o TICKERS, del primer mes son como tal:  \
        ",
        className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
        ###### PASSIVE INVESTMENT ######
        first_tickers = get_first_tickers(normalized_data_dict)

        $ ['AC.MX', 'ALFAA.MX', 'ALPEKA.MX', 'ALSEA.MX', 'AMXL.MX', 'ASURB.MX' [...] 'VOLARA.MX', 'WALMEX.MX']
        '''
        ,className = "code-block")]),

    dbc.Row([
        html.P("Donde:  \
        ",
        className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
        def get_first_tickers(normalized_data_dict):
            first_tickers = list(normalized_data_dict.values())[0]["Ticker"].tolist()
            first_tickers.remove('MXN CASH')
            first_tickers.remove('MXN CASH')
            first_tickers.remove('MXN CASH')
            return first_tickers
        '''
        ,className = "code-block")]),

    dbc.Row([
        html.P("Se obtienen del primer rebalanceo que surge de la lista de CSV's.  \
        Dentro de esta selección de nuestro PORTAFOLIO INICIAL, fue considerado prudente remover los tickers de las emisoras de\
        BANCO SANTANDER B, COCA-COLA FEMSA CLASS L y modificar el de BANREGIO GRUPO FINANCIERO.\
        Ya fuera porque dejaron de estar listadas en la Bolsa, o porque cambiaron de nombre. El punto era facilitarme la extracción de \
        datos de históricos de las fuentes de Yahoo Finance. Y es claro que estas emisoras tendrían conflicto con el desarollo. \
        El capital supuesto de las empresas removidas, fue considerado como CASH.\
        ",
        className = "small-text")]),

    dbc.Container(
        dbc.Table.from_dataframe(normalized_data_dict['31-01-2018'].round(2), striped=True, bordered=True, hover=True),
        style={'height': '500px', 'overflowY': 'auto'}, className="table"),

    dbc.Row([
        html.P(" Con los tickers correspondientes para formar el portafolio, descargamos los datos de nuestra fuente Yahoo Finance, mediante la\
        paquetería yfinance de Python. Desde la fecha del primer rebalanceo, hasta la última '2018-01-31' --> '2020-08-21'\
        ",
        className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
        data_yf = yf_downloader(first_tickers, '2018-01-31', '2020-08-24')
        passive_investment_historical_prices  = data_passive_investment(first_tickers, rebalance_date_values)
        '''
        ,className = "code-block")]),

    dbc.Row([
        html.P("Donde:\
        ",
        className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
        def yf_downloader(first_tickers, first_date, last_date):
            yf_data = {}
            print(first_tickers)
            for tickers in first_tickers:
                print(tickers)
                yf_data[tickers] = yf.download(tickers, start=first_date, end=last_date, actions=False, interval = "1d",auto_adjust = False, prepost = False)
                route = str(tickers)
                yf_data[tickers].to_pickle(("/Users/israelcastillo/Documents/m_st/myst_if708348_lab1/files/"+route+".pkl"))

        def data_passive_investment(ticker_to_yf, rebalance_date_values):
            data_yf={}
            rebalance_dates_prices={}
            condensed_df = []
            for ticker in ticker_to_yf:
                route = str(ticker)
                #data_yf[ticker]=  yf.download(ticker, start='2018-01-31', end='2020-08-24', actions=False, \
                interval = "1d", auto_adjust = False, prepost = False)
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
        '''
        ,className = "code-block")]),


    dbc.Row([
        html.P(" Dentro de la función yf_downloader, guardamos a formato pickle los datos descargados.\
        Cuando se guardan en datos pickle el manejo de datos es más rápido porque ya queda la información guardad de manera local.\
        Con la función > passive_investment_historical_prices, buscamos leer los pickle y generar un condensado de todos los precios de las emisoras tomadas para nuestro portafolio\
        inicial, y así poder tener el valor de nuestro PORTAFOLIO a través del TIEMPO, dependiendo del cambio del PRECIO de sus ACTIVOS. \
        ",
        className = "small-text")]),


    dbc.Row([
        html.P(" En esta función ya IGUALAMOS las fechas de rebalanceos para que solamente nos mostraran los PRECIOS de cada emisora (ordenadas alfabéticamente) en las fechas CORRESPONDIENTES provenientes de yfinance.\
        ",
        className = "small-text")]),

    dbc.Container(
        dbc.Table.from_dataframe(passive_investment_historical_prices.reset_index().round(2), striped=True, bordered=True, hover=True),
        style={'height': '500px', 'overflowY': 'auto'}, className="table"),

    dbc.Row([
        html.P(" Una vez obteniendo la información histórica de los PRECIOS, y ya teniendo tambien la información de los pesos.\
        Fuimos haciendo el calculo de la postura tomada, con el capital disponible para CADA EMISORA, con su ponderación de nuestro\
        $1,000,000. Y así obtener el número de TÍTULOS, COMISIÓN y la POSTURA correspondiente en CAPITAL. Esto se ve en el PRIMER MES como:\
        ",
        className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
        first_month_weightprice = first_month_weightprice_calc(normalized_data_dict, passive_investment_historical_prices)
        '''
        ,className = "code-block")]),

    dbc.Row([
        html.P(" Donde:\
        ",
        className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
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
            first_month_weightprice['Comisión'] = ((first_month_weightprice['Capital Ponderado']/first_month_weightprice.iloc[:,1]).apply(np.floor)*first_month_weightprice.iloc[:,1] * 0.00125)
            first_month_weightprice.loc['MXN CASH']['Comisión'] = 0
            first_month_weightprice['Capital - Comision'] = (first_month_weightprice['Capital Ponderado'] - first_month_weightprice['Comisión'])
            first_month_weightprice['Títulos P.'] = (first_month_weightprice['Capital - Comision']/first_month_weightprice.iloc[:,1]).apply(np.floor)
            first_month_weightprice.loc['MXN CASH']['Títulos P.'] = first_month_weightprice.loc['MXN CASH']['Peso (%)']*1000000
            first_month_weightprice['Postura.'] = (first_month_weightprice['Títulos P.']*first_month_weightprice.iloc[:,1])
            return first_month_weightprice
        '''
        ,className = "code-block")]),


    dbc.Container(
        dbc.Table.from_dataframe(first_month_weightprice.reset_index().round(2), striped=True, bordered=True, hover=True),
        style={'height': '500px', 'overflowY': 'auto'}, className="table"),


    dbc.Row([
        html.P(" Ya obteniendo la cantidad de TITULOS que compramos una vez cobrada nuestra COMISIÓN, es más sencillo\
        entender el valor de nuestro portafolio como el resultado de multiplicar la postura inicial en TÍTULOS con el PRECIO correspondiente de cada\
        emisora, o TICKER. [TITULOS * PRECIO]. Esto durante cada mes, y se obtiene con la suma el valor total del PORTAFOLIO, a través del TIEMPO.\
        ",
        className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
        Capital Ponderado = 1,000,000 / Peso (%)
        Titulos = Capital Ponderado / Precio
        Comision = Titulos * Precio * 0.00125
        Titulos P = (Capital - Comision) / Precio
        Postura = Titulos P * Precio
        '''
        ,className = "code-block")]),

    dbc.Row([
        html.H2("4.2 Inversión Activa", className = "subtext")]),

    dbc.Row([
        html.P(" Ahora evaluemos la inversión activa. En este caso consideramos al activo de mayor peso, AMXL.MX\
        y le quitamos la mitad de su ponderación para asignarla en CASH. Partiendo de esto, vamos reajustando la cantidad de títulos\
        que debemos asignar a esta emisora, en base a una estrategia en especifico que se desenvuelve a través del tiempo, en consideración de los rendimientos de este, AMXL.MX\
        En esta tabla ya estamos considerando el rebalanceo del 50% para AMXL.MX\
        ",
        className = "small-text")]),


    dbc.Row([
        dcc.Markdown('''
        ```py
        ###### ACTIVE INVESTMENT ######
        first_month_weightprice_active = active_initializer(first_month_weightprice)
        '''
        ,className = "code-block")]),

    dbc.Row([
        html.P("Donde:\
        ",
        className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
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
        '''
        ,className = "code-block")]),


    dbc.Container(
        dbc.Table.from_dataframe(first_month_weightprice_active.reset_index().round(2), striped=True, bordered=True, hover=True),
        style={'height': '500px', 'overflowY': 'auto'}, className="table"),

    dbc.Row([
        html.P("Estoy considerando que habrá un cambio de títulos con las señales dadas por el precio de AMXL.MX.\
        Cuando el precio del activo disminuya más de 1% dentro de un mismo día, es decir CLOSE/OPEN -1 sea mayor que -1%\
        entonces consideramos que es necesario comprar el 10% de lo que tenemos disponible en CASH al precio que debe estar el activo.\
        Las señales quedan como tal. Esto es día a día, si se cumple la señal entonces se aumentan los títulos y se disminuye el CASH.",
        className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
        signal_dates = signal_dates(first_month_weightprice_active, rebalance_date_values)
        '''
        ,className = "code-block")]),

    dbc.Row([
        html.P("Donde, de manera más breve se simplifica como:\
        ",
        className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
        def signal_dates_redux(data):
            data = data[["titulos_t", "titulos_c", "precio", "comision", "c_acum", "Cash"]]
            data["comision"] = data["comision"].round(2)
            data["c_acum"] = data["c_acum"].round(2)
            data["titulos_c"] = data["titulos_c"].apply(np.floor)
            data["titulos_t"] = data["titulos_t"].apply(np.floor)
            return data
        '''
        ,className = "code-block")]),

    dbc.Container(
        dbc.Table.from_dataframe(signal_dates_redux.reset_index().round(), striped=True, bordered=True, hover=True),
        style={'height': '500px', 'overflowY': 'auto'}, className="table"),

    dbc.Row([
        html.P("Demostremos en la siguiente tabla solamente las operaciones tomadas a través del tiempo al comprar los títulos, con su FECHA, COMISIÓN y CANTIDAD DE TÍTULOS."
        ,className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
        df_operaciones = df_operaciones(signal_dates)
        '''
        ,className = "code-block")]),

    dbc.Row([
        html.P("Donde: "
        ,className = "small-text")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
        def df_operaciones(data):
            data = signal_dates_redux(data)
            df_operaciones = pd.DataFrame()
            for i in range(0, len(data)):
                if data.iloc[i, 2] != 0:
                    df_operaciones = df_operaciones.append(data.iloc[i, :])
            return df_operaciones
        '''
        ,className = "code-block")]),

    dbc.Container(
        dbc.Table.from_dataframe(df_operaciones.reset_index().round(), striped=True, bordered=True, hover=True),
        style={'height': '500px', 'overflowY': 'auto'}, className="table"),

    dbc.Row([
        html.H2("4.3 Inversión Pasiva vs. Activa", className = "subtext")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
        df_pasiva = portfolio_value_pas(rebalance_date_values, first_month_weightprice, passive_investment_historical_prices)
        '''
        ,className = "code-block")]),

    dbc.Container(
        dbc.Table.from_dataframe(df_pasiva, striped=True, bordered=True, hover=True),
        style={'height': '500px', 'overflowY': 'auto'}, className="table"),

    dbc.Row([
        dcc.Markdown('''
        ```py
        df_activa = portfolio_value_active(rebalance_date_values, first_month_weightprice_active, passive_investment_historical_prices, signal_dates)
        '''
        ,className = "code-block")]),

    dbc.Container(
        dbc.Table.from_dataframe(df_activa, striped=True, bordered=True, hover=True),
        style={'height': '500px', 'overflowY': 'auto'}, className="table"),


    dbc.Container(
    dcc.Graph(
            figure=fig_active_pasive
        )),

    dbc.Container(
    dcc.Graph(
            figure=fig_active_pasive_return
        )),

    dbc.Row([
        html.H2("4.4 Medidas de Desempeño", className = "subtext")]),


    dbc.Row([
        dcc.Markdown('''
        ```py
        df_medidas = market_benchmarks(df_pasiva, df_activa)
        '''
        ,className = "code-block")]),


    dbc.Row([
        html.P("Donde: "
        ,className = "small-text")]),


    dbc.Row([
        dcc.Markdown('''
        ```py
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
        '''
        ,className = "code-block")]),

    dbc.Container(
        dbc.Table.from_dataframe(df_medidas, striped=True, bordered=True, hover=True),
        style={'height': '250px', 'overflowY': 'auto'}, className="table"),

    dbc.Row([html.Img(src=
            "https://study.com/cimages/multimages/16/sharpe-ratio.png",
            className="image_sharpe")]),

    dbc.Row([
        html.P("Las medidas de atribución al desemepeño son las formas en las que evaluamos \
        qué tanta efectividad ha tenido nuestra alocación de portafolio.\
        Cuanto mayor es el Sharpe Ratio, mejor es la rentabilidad del fondo en relación a la cantidad de riesgo que se ha tomado en la inversión.\
        El Sharpe Ratio es un buen método para medir la desviación estandar de la rentabilidad de cualquier fondo individualmente y compararla con otros.\
        La ratio de Sharpe se utiliza para mostrar hasta qué punto el rendimiento de una inversión compensa al inversor por asumir riesgo en su inversión.\
        "
        ,className = "small-text")]),

    dbc.Row([
        html.P("Para sacar estas medidas fue necesario tener los históricos de rendimientos \
        de ambos portafolios. Asi obtuvimos tambien el promedio mensual de retorno, y el acumulado a través de todo \
        el periodo de estudio. De esta manera podemos ver el rendimiento promedio al mes, el total de retorno al final del periodo que estudiamos, \
        y finalmente, que tanto riesgo asumimos por lo que obtuvimos, a forma de el ratio de Sharpe.\
        "
        ,className = "small-text")]),

    dbc.Row([
        html.H1("5. Conclusiones", className = "subtext_medium")]),

    dbc.Row([
        html.P("Al observar los desempeños de ambas alocaciones, tanto pasiva como activa podemos reconocer que mientras estén de manera directa relacionadas al índice, sus retornos tenderán a ser similares.\
        Es importante reconocer que la gestión activa de un portafolio no es necesariamente mejor que la de la pasiva. Aunque si genera una ligera ventaja sobre dejar tu capital de manera igualada al mercado, \
        tambien te expones a la estructuración de una estrategia que puede que sea contraproducente a tu portafolio, y que además conlleva costos de comisión mayores. \
        Es bien conocido que una estrategia excelente es apegarse al mercado y seguir la tendencia de un índice general. Este caso es el NAFTRAC. Por lo que alocar tu dinero de esta manera si pudiera probar ser efectiva\
        para tus rendimientos. Sin embargo, tambien hay que tener en mente que hay una gran exposición macroeconómica de riesgo del mercado al que estás invirtiendo. \
        Para este caso en particular si fueron malos resultados provenientes del terrible desempeño general de la economía Mexicana, reflejada en este índice,\
        por lo que tanto invirtiendo de manera pasiva, como activa, resulto en pérdidas considerables de 20% - 21% de nuestro capital. Y ratios de Sharpe terribles. \
        "
        ,className = "small-text")]),

    dbc.Row([
        html.P("Creo que el aprendizaje de manejar datos y adminsitrar un proyecto de Python fue bien dado Y permitió elaborar en detalles mucho más específicos del mercado, y de invertir en este: como COMISIONES, cambios de POSTURAS, compra de TITULOS .\
        Y SEÑALES de inversión para cambiar nuestras ALOCACIONES de PORTAFOLIO.\
        "
        ,className = "small-text")]),

    dbc.Row([
        html.H1("main.py", className = "subtext_medium")]),

    dbc.Row([
        dcc.Markdown('''
        ```py
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
        compiled_norm = compiled_norm(normalized_data_dict)

        ###### ALL TICKERS ON THE PERIOD STUDIES WITHIN THE NAFTRACK ######
        global_tickers = get_global_tickers(normalized_data_dict)

        # DATES NAFTRAC REBALANCES ######
        rebalance_date_values = get_rebalance_dates(normalized_data_dict)

        ###### PASSIVE INVESTMENT ######
        first_tickers = get_first_tickers(normalized_data_dict)
        # data_yf = yf_downloader(first_tickers, '2018-01-31', '2020-08-24')
        passive_investment_historical_prices  = data_passive_investment(first_tickers, rebalance_date_values)
        first_month_weightprice = first_month_weightprice_calc(normalized_data_dict, passive_investment_historical_prices)
        df_pasiva = portfolio_value_pas(rebalance_date_values, first_month_weightprice, passive_investment_historical_prices)

        ###### ACTIVE INVESTMENT ######
        first_month_weightprice_active = active_initializer(first_month_weightprice)
        signal_dates = signal_dates(first_month_weightprice_active, rebalance_date_values)
        signal_dates_redux = signal_dates_redux(signal_dates)
        df_operaciones = df_operaciones(signal_dates)
        df_activa = portfolio_value_active(rebalance_date_values, first_month_weightprice_active, passive_investment_historical_prices, signal_dates)

        ###### MARKET BENCHMARKS  ######
        df_medidas = market_benchmarks(df_pasiva, df_activa)
        '''
        ,className = "code-block")]),


])

if __name__ == "__main__":
    app.run_server(dev_tools_hot_reload=True, debug=True, dev_tools_hot_reload_interval=1000)
