import pandas as pd
import os
import time
from datetime import datetime
import re
import urllib
import quandl

from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style

style.use("dark_background")

#change this path to wherever this intraquarterfile is
intraQuarter_path = "/Users/xavier/Programming/Python/SVM/intraQuarter"


# quandl.ApiConfig.api_key = "jk6Dsp3Em-Y9n54znX9e"
# data = quandl.get("YALE/SPCOMP", authtoken="jk6Dsp3Em-Y9n54znX9e", start_date = "2005-1-1", end_date="2019-12-31")

def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = intraQuarter_path + '/_KeyStats'
    # get the root for every traversal
    # OS.WALK is a tree traversal
    stock_list = [x[0] for x in os.walk(statspath)]
    # If the stock's percent change is less than the S&P 500, then the stock is and under-performing stock. If the
    # percentage change is more, than the label is out-perform.
    df = pd.DataFrame(
        columns=['Date', 'Unix', 'Ticker', 'DE Ratio', 'Price', 'stock_p_change', 'SP500', 'sp500_p_change',
                 'Difference'])
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
                    try:
                        value = float(source.split(gather + ':</td>')[1].split('<td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    except Exception as e:
                        value = (source.split(gather + ':</td>\n')[1].split('<td class="yfnc_tabledata1">')[1].split('</td>')[0])
                        print(str(e), ticker, file)
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

                    df = df.append({'Date': date_stamp, 'Unix': unix_time, 'Ticker': ticker, 'DE Ratio': value,
                                    'Price': stock_price, 'SP500': sp500_value, 'sp500_p_change': sp500_p_change,
                                    'Difference': (difference), 'Status': status}, ignore_index=True)
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
    df.to_csv(save)


Key_Stats()
