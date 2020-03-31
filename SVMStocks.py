import pandas as pd
import os
import time
from datetime import datetime
import quandl


path = "/Users/xavier/Downloads/intraQuarter"
# quandl.ApiConfig.api_key = "jk6Dsp3Em-Y9n54znX9e"
# data = quandl.get("YALE/SPCOMP", authtoken="jk6Dsp3Em-Y9n54znX9e", start_date = "2005-1-1", end_date="2019-12-31")

def Key_Stats(gather = "Total Debt/Equity (mrq)"):
    statspath = path+'/_KeyStats'
    #get the root for every traversal
    #OS.WALK is a tree traversal
    stock_list = [x[0] for x in os.walk(statspath)]
    df = pd.DataFrame(columns = ['Date', 'Unix', 'Ticker', 'DE Ratio'])
    sp500_df = pd.read_csv("/Users/xavier/Programming/Python/SVM/YAHOO-INDEX_GSPC.csv")
    #ignore the first director i.e. /Users/xavier/Downloads/intraQuarter/_KeyStats
    #from 1 to 5
    for each_dir in stock_list[1:25]:
        each_file = os.listdir(each_dir)
        #for mac use this
        ticker = each_dir.split(statspath+'/')[1]
        #ticker = each_dir.split("\\")[1]
        #sanitycheck for non-existent data
        if len(each_file) > 0 :
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                full_file_path = each_dir+'/'+file
                #source would usually be request(url), if getting from webpage
                source = open(full_file_path, 'r').read()
                #want the second element from the list
                # note: split argument is the string that you want it to seperate and then  the first element from the second split
                # this split is not perfect yet
                try:
                    if gather + ':</td>' in source:
                        value = float(source.split(gather + ':</td>')[1].split('<td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    else:
                        value = "N/A"
                    # taking out the dates of where there is no trading activity like sat and sun
                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[sp500_df["Date"] == sp500_date]
                        sp500_value = float(row["Adj Close"])
                    except:
                        #QUICK HACK : 259200 seconds  = 3days -> get out of some holidays and weekends
                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                        row = sp500_df[sp500_df["Date"] == sp500_date]
                        sp500_value = float(row["Adj Close"])

                    stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                    df = df.append({'Date':date_stamp, 'Unix': unix_time, 'Ticker': ticker, 'DE Ratio': value, 'Price': stock_price, 'SP500': sp500_value }, ignore_index=True)
                except Exception as e:
                    pass

        #saving the values into a csv file
    save = gather.replace(' ', '').replace(')','').replace('(', '').replace('/', '') + ('.csv')
    print(save)
    df.to_csv(save)


Key_Stats()