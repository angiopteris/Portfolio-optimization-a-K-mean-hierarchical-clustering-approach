import bs4 as bs4
import pickle
import requests
import datetime as datetime
import os
import pandas as pandas
pandas.core.common.is_list_like = pandas.api.types.is_list_like
import pandas_datareader.data as data


# save standard & poor's 500 ticker list

def save_sp500_tickers():
    response = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs4.BeautifulSoup(response.text, "lxml")
    table = soup.find("table", {"class": "wikitable sortable"})
    tickers = []
    for row in table.findAll("tr")[1:]:
        ticker = row.findAll("td")[0].text
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as file:
        pickle.dump(tickers, file)

    print(tickers)

    return tickers


#save_sp500_tickers()


# fetching sp500

def morning_star():

    if not os.path.exists("stock_dfs"):
        os.makedirs("stock_dfs")

    with open("sp500tickers.pickle", "rb") as file:
        tickers = pickle.load(file)

    start = datetime.datetime(2000, 1, 1)
    end = datetime.datetime(2012, 12, 31)

    count = 0
    count_e = 0
    no_such_tickers = []
    for ticker in tickers:
        count += 1
        print(str(count) + ". " + ticker)

        if not os.path.exists("stock_dfs/{}.csv".format(ticker)):
            while True:
                try:
                    data_frame = data.DataReader(ticker, "morningstar", start, end)

                    if str(data_frame.head()):
                        data_frame.to_csv("stock_dfs/{}.csv".format(ticker))
                        count_e = 0
                        break
                except Exception as e:
                    count_e += 1
                    print(str(count_e) + ". " + ticker + " " + str(e))

##                    no_such_tickers = ['ANDV', 'BKNG', 'BHF', 'CBRE', 'DWDP', 'DXC', 'EVRG',
##                     'JEF', 'TPR', 'UAA', 'WELL', 'MMM']
                    if count_e >= 10:
                        no_such_tickers.append(ticker)
                        print(no_such_tickers)
                        count_e = 0
                        break
        else:
            print("already have {}".format(ticker))


# morning_star()


## merge sp500

def merge_data():
    no_such_tickers = ['ANDV', 'BKNG', 'BHF', 'CBRE', 'DWDP', 'DXC', 'EVRG',
                       'JEF', 'TPR', 'UAA', 'WELL', 'MMM']

    merged_data_frame = pandas.DataFrame()

    with open("sp500tickers.pickle", "rb") as file:
        tickers = pickle.load(file)

    for i, ticker in enumerate(tickers):
        if ticker in no_such_tickers:
            continue
        data_frame = pandas.read_csv("stock_dfs/{}.csv".format(ticker))
        data_frame.set_index("Date", inplace=True)
        data_frame.rename(columns={"Close": ticker}, inplace=True)
        data_frame.drop(["Symbol", "Open", "High", "Low", "Volume"], 1, inplace=True)

        if merged_data_frame.empty:
            merged_data_frame = data_frame
        else:
            merged_data_frame = merged_data_frame.join(data_frame, how="outer")

        if i % 10 == 0:
            print(i)

    print(merged_data_frame.head())
    merged_data_frame.to_csv('sp500_joined_closes.csv')


merge_data()

