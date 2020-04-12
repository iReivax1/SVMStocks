import os
import time
from datetime import datetime
import re
import urllib
import quandl

from time import mktime
from sklearn import svm, preprocessing
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
style.use("dark_background")


#change this path to wherever this intraquarterfile is
intraQuarter_path = "/Users/xavier/Programming/Python/SVM/intraQuarter"

auth_token = quandl.ApiConfig.api_key = "jk6Dsp3Em-Y9n54znX9e"
# data = quandl.get("YALE/SPCOMP", authtoken="jk6Dsp3Em-Y9n54znX9e", start_date = "2005-1-1", end_date="2019-12-31")
FEATURES =  ['DE Ratio',
             'Trailing P/E',
             'Price/Sales',
             'Price/Book',
             'Profit Margin',
             'Operating Margin',
             'Return on Assets',
             'Return on Equity',
             'Revenue Per Share',
             'Market Cap',
             'Enterprise Value',
             'Forward P/E',
             'PEG Ratio',
             'Enterprise Value/Revenue',
             'Enterprise Value/EBITDA',
             'Revenue',
             'Gross Profit',
             'EBITDA',
             'Net Income Avl to Common ',
             'Diluted EPS',
             'Earnings Growth',
             'Revenue Growth',
             'Total Cash',
             'Total Cash Per Share',
             'Total Debt',
             'Current Ratio',
             'Book Value Per Share',
             'Cash Flow',
             'Beta',
             'Held by Insiders',
             'Held by Institutions',
             'Shares Short (as of',
             'Short Ratio',
             'Short % of Float',
             'Shares Short (prior ']


def Build_Data_Set():
    data_df = pd.DataFrame.from_csv("key_stats.csv")

    data_df = data_df.reindex(np.random.permutation(data_df.index))

    X = np.array(data_df[FEATURES].values)  # .tolist())

    y = (data_df["Status"]
         .replace("underperform", 0)
         .replace("outperform", 1)
         .values.tolist())

    X = preprocessing.scale(X)

    return X, y


def Analysis():
    test_size = 1000
    X, y = Build_Data_Set()
    print(len(X))

    clf = svm.SVC(kernel="linear", C=1.0)
    clf.fit(X[:-test_size], y[:-test_size])

    correct_count = 0

    for x in range(1, test_size + 1):
        if clf.predict(X[-x])[0] == y[-x]:
            correct_count += 1

    print("Accuracy:", (correct_count / test_size) * 100.00)

#need to randomize data set if not the training set is going to be monotonic as our files are in alphabetical order
def Randomizing():
    df = pd.DataFrame({"D1":range(5), "D2":range(5)})
    print(df)
    df2 = df.reindex(np.random.permutation(df.index))
    print(df2)

def Stock_Prices():
    df = pd.DataFrame()

    statspath = intraQuarter_path+'/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]

    print(stock_list)

    for each_dir in stock_list[1:]:
        try:
            ticker = each_dir.split("\\")[1]
            print(ticker)
            name = "WIKI/"+ticker.upper()
            data = quandl.get(name,
                              trim_start = "2000-12-12",
                              trim_end = "2014-12-30",
                              authtoken=auth_token)
            data[ticker.upper()] = data["Adj. Close"]
            df = pd.concat([df, data[ticker.upper()]], axis = 1)
        except Exception as e:
            print(str(e))
            time.sleep(10)
        try:
            ticker = each_dir.split("\\")[1]
            print(ticker)
            name = "WIKI/"+ticker.upper()
            data = Quandl.get(name,
                              trim_start = "2000-12-12",
                              trim_end = "2014-12-30",
                              authtoken=auth_tok)
            data[ticker.upper()] = data["Adj. Close"]
            df = pd.concat([df, data[ticker.upper()]], axis = 1)
        except Exception as e:
            print(str(e))
    df.to_csv("stock_prices.csv")

def Key_Stats(gather=None):
    if gather is None:
        #features
        gather = ["Total Debt/Equity",
                  'Trailing P/E',
                  'Price/Sales',
                  'Price/Book',
                  'Profit Margin',
                  'Operating Margin',
                  'Return on Assets',
                  'Return on Equity',
                  'Revenue Per Share',
                  'Market Cap',
                  'Enterprise Value',
                  'Forward P/E',
                  'PEG Ratio',
                  'Enterprise Value/Revenue',
                  'Enterprise Value/EBITDA',
                  'Revenue',
                  'Gross Profit',
                  'EBITDA',
                  'Net Income Avl to Common ',
                  'Diluted EPS',
                  'Earnings Growth',
                  'Revenue Growth',
                  'Total Cash',
                  'Total Cash Per Share',
                  'Total Debt',
                  'Current Ratio',
                  'Book Value Per Share',
                  'Cash Flow',
                  'Beta',
                  'Held by Insiders',
                  'Held by Institutions',
                  'Shares Short (as of',
                  'Short Ratio',
                  'Short % of Float',
                  'Shares Short (prior ']
    statspath = intraQuarter_path + '/_KeyStats'
    # get the root for every traversal
    # OS.WALK is a tree traversal
    stock_list = [x[0] for x in os.walk(statspath)]
    # If the stock's percent change is less than the S&P 500, then the stock is and under-performing stock. If the
    # percentage change is more, than the label is out-perform.
    df = pd.DataFrame(
        columns=['Date',
                 'Unix',
                 'Ticker',
                 'Price',
                 'stock_p_change',
                 'SP500',
                 'sp500_p_change',
                 'Difference',
                 'DE Ratio',
                 'Trailing P/E',
                 'Price/Sales',
                 'Price/Book',
                 'Profit Margin',
                 'Operating Margin',
                 'Return on Assets',
                 'Return on Equity',
                 'Revenue Per Share',
                 'Market Cap',
                 'Enterprise Value',
                 'Forward P/E',
                 'PEG Ratio',
                 'Enterprise Value/Revenue',
                 'Enterprise Value/EBITDA',
                 'Revenue',
                 'Gross Profit',
                 'EBITDA',
                 'Net Income Avl to Common ',
                 'Diluted EPS',
                 'Earnings Growth',
                 'Revenue Growth',
                 'Total Cash',
                 'Total Cash Per Share',
                 'Total Debt',
                 'Current Ratio',
                 'Book Value Per Share',
                 'Cash Flow',
                 'Beta',
                 'Held by Insiders',
                 'Held by Institutions',
                 'Shares Short (as of',
                 'Short Ratio',
                 'Short % of Float',
                 'Shares Short (prior ',
                 'Status'])

    sp500_df = pd.read_csv("/Users/xavier/Programming/Python/SVM/YAHOO-INDEX_GSPC.csv")
    ticker_list = []
    # ignore the first director i.e. /Users/xavier/Downloads/intraQuarter/_KeyStats
    for each_dir in stock_list[1:25] :
        each_file = os.listdir(each_dir)
        # for mac use this
        ticker = each_dir.split(statspath + '/')[1]
        ticker_list.append(ticker)

        starting_stock_value = False
        starting_sp500_value = False
        # ticker = each_dir.split("\\")[1]
        # sanity check for non-existent data
        if len(each_file) > 0:
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                full_file_path = each_dir + '/' + file
                # source would usually be request(url), if getting from webpage
                source = open(full_file_path, 'r').read()
                # want the second element from the list note: split argument is the string that you want it to
                # separate and then  the first element from the second split this split is not perfect yet
                try:
                    value_list = []
                    for each_data in gather:
                        try:
                            #.*? captures almost anything.. ? is optional
                            #The backslash is a metacharacter in regular expressions, and is used to escape other metacharacters. The regex \\ matches a single backslash. \d is a single token
                            # print re.escape("Hello 123 .?!@ World")
                            # OUTPUT:
                            # Hello\ 123\ \.\?\!\@\ World
                            regex = re.escape(each_data) + r'.*?(\d{1,8}\.\d{1,8}M?B?|N/A)%?</td>'
                            value = re.search(regex, source)
                            value = (value.group(1))

                            if "B" in value:
                                value = float(value.replace("B", '')) * 1000000000

                            elif "M" in value:
                                value = float(value.replace("M", '')) * 1000000

                            value_list.append(value)
                        except Exception as e:
                            value = "N/A"
                            value_list.append(value)
                    # taking out the dates of where there is no trading activity like sat and sun
                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[sp500_df["Date"] == sp500_date]
                        sp500_value = float(row["Adj Close"])
                    except:
                        # QUICK HACK : 259200 seconds  = 3days -> get out of some holidays and weekends
                        sp500_date = datetime.fromtimestamp(unix_time - 259200).strftime('%Y-%m-%d')
                        row = sp500_df[sp500_df["Date"] == sp500_date]
                        sp500_value = float(row["Adj Close"])
                    #get stock price through splitting first then regex for complex cases
                    try:
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                    except Exception as e:
                        #split is not working , use regex instead to find the number
                        #i.e in '<span id="yfs_l10_px">101.96</span>'
                        try:
                            stock_price = (source.split('</small><big><b>')[1].split('</b></big>')[0])
                            #regex 1 to 8 digits then a . then 1 to 8 digits, find a number
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                            stock_price = float(stock_price.group(1))
                            # print("small big regex", str(e), ticker, file)
                        except Exception as e:
                            try:
                                stock_price = (source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0])
                                # print(stock_price, "after split")
                                stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                                # print(stock_price, "after regex")
                                stock_price = float(stock_price.group(1))
                                # print("span class regex", str(e), ticker, file)
                            except Exception as e:
                                try:
                                    stock_price = (source.split('<span id="yfs_l10_vz">')[1].split('</span>')[0])
                                    stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                                    stock_price = float(stock_price.group(1))
                                    # print('span id Stock price', stock_price, str(e))
                                except:
                                    time.sleep(15)

                    # start over with the % change each time the stock itself changes
                    if not starting_stock_value:
                        starting_stock_value = stock_price
                    if not starting_sp500_value:
                        starting_sp500_value = sp500_value

                    # calculate percentage change
                    stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100
                    sp500_p_change = ((sp500_value - starting_sp500_value) / starting_sp500_value) * 100

                    location = len(df['Date'])

                    difference = stock_p_change-sp500_p_change

                    if difference > 0:
                        status = "outperform"
                    else :
                        status = "underperform"

                    if value_list.count("N/A") > (0):
                        pass
                    else:
                        try:
                            df = df.append({'Date': date_stamp,
                                            'Unix': unix_time,
                                            'Ticker': ticker,
                                            'Price': stock_price,
                                            'stock_p_change': stock_p_change,
                                            'SP500': sp500_value,
                                            'sp500_p_change': sp500_p_change,
                                            'Difference': difference,
                                            'DE Ratio': value_list[0],
                                            # 'Market Cap':value_list[1],
                                            'Trailing P/E': value_list[1],
                                            'Price/Sales': value_list[2],
                                            'Price/Book': value_list[3],
                                            'Profit Margin': value_list[4],
                                            'Operating Margin': value_list[5],
                                            'Return on Assets': value_list[6],
                                            'Return on Equity': value_list[7],
                                            'Revenue Per Share': value_list[8],
                                            'Market Cap': value_list[9],
                                            'Enterprise Value': value_list[10],
                                            'Forward P/E': value_list[11],
                                            'PEG Ratio': value_list[12],
                                            'Enterprise Value/Revenue': value_list[13],
                                            'Enterprise Value/EBITDA': value_list[14],
                                            'Revenue': value_list[15],
                                            'Gross Profit': value_list[16],
                                            'EBITDA': value_list[17],
                                            'Net Income Avl to Common ': value_list[18],
                                            'Diluted EPS': value_list[19],
                                            'Earnings Growth': value_list[20],
                                            'Revenue Growth': value_list[21],
                                            'Total Cash': value_list[22],
                                            'Total Cash Per Share': value_list[23],
                                            'Total Debt': value_list[24],
                                            'Current Ratio': value_list[25],
                                            'Book Value Per Share': value_list[26],
                                            'Cash Flow': value_list[27],
                                            'Beta': value_list[28],
                                            'Held by Insiders': value_list[29],
                                            'Held by Institutions': value_list[30],
                                            'Shares Short (as of': value_list[31],
                                            'Short Ratio': value_list[32],
                                            'Short % of Float': value_list[33],
                                            'Shares Short (prior ': value_list[34],
                                            'Status': status},
                                           ignore_index=True)

                        except Exception as e:
                            print(str(e), 'df creation')
                            time.sleep(15)

                except Exception as e:
                    pass



    for each_ticker in ticker_list:
        try:
            plot_df = df[(df['Ticker'] == each_ticker)]

            plot_df = plot_df.set_index(['Date'])

            if plot_df['Status'][-1] == 'underperform':
                color = 'r'
            else:
                color = 'g'

            plot_df['Difference'].plot(label=each_ticker, color=color)
            plt.legend()
        except Exception as e:
            print(str(e))
    plt.show()
    # saving the values into a csv file
    save = gather.replace(' ', '').replace(')', '').replace('(', '').replace('/', '') + ('.csv')
    print(save)
    df.to_csv("key_stats.csv")


Key_Stats()
