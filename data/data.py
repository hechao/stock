# coding: utf-8

#from bs4 import BeautifulSoup
#from urllib2 import urlopen
#import string

#from datetime import datetime, timedelta
#from dateutil.relativedelta import relativedelta

from csv_handle import data_read, csv_write
from get_stock_data import get_date, stock_pg_data, get_current_stock_value, calculate_data, group_output_dict
from html_handle import html

#import json


    
if __name__ == "__main__":

    yr = 4
    
    date = get_date()
    str
    html_path = '/srv/www/idehe.com/stock/index.html'
    csv_path = '/srv/www/idehe.com/stock/data/stock_csv/stock%s.csv' % (date.strftime('%Y-%m-%d'))
    csv_dlpath = 'http://www.idehe.com/stock/data/stock_csv/stock%s.csv' % (date.strftime('%Y-%m-%d'))
    stock_data_path = '/srv/www/idehe.com/stock/data/hc.csv'
    
    #file_path = '/srv/www/idehe.com/stock/json.json'
    #stocks_path = '/srv/www/idehe.com/stock/data/stock_hc.txt'
    #dump(stock_data)
    
    date = get_date()
    
    stocklist = data_read(stock_data_path)
    
    stock_data_dict = group_output_dict(date, stocklist, yr)
    
    csv_write(stock_data_dict, csv_path)
    html(stock_data_dict, date, html_path, csv_dlpath)
    
    
    