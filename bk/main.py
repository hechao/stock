#! /usr/bin/python
#-*- encoding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib2 import urlopen
import string

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

stock_data = {}

import json

def get_date():
    # get time
    utc_time = datetime.utcnow()

    date = utc_time + timedelta(hours=8)

    return date
    
def init(file_path, detail_date, yr):
    #init html
    myfile = open(file_path, 'w')
    myfile.writelines('\n')    
    myfile.close()
    
    myfile = open(file_path, 'a')             # open for output (creates)
    myfile.writelines('<!DOCTYPE HTML>')
    myfile.writelines('<html lang="en-US">')
    myfile.writelines('<head>')
    myfile.writelines('	<meta charset="UTF-8">')
    myfile.writelines('<title>GET FINANCE DATA</title>')
    myfile.writelines('</head>')
    
    myfile.writelines("Current date is: " + str(detail_date) + "<br>\n")
    myfile.writelines('Get google finance data, get value of each stock in %s years and compare, find the percentage level between the highest and lowest value<br>\n' % yr)
    myfile.close()
    
def realtime_data(stock_id):
    # get current value of stock
    page = urlopen('https://www.google.com/finance?q=%s' % (stock_id))
    soup = BeautifulSoup(page, 'lxml')
    tr = soup.find_all('span')
    tr_8 = tr[8].find_all('span')
    realtime_str_value = tr_8[0].string
    realtime_value = float(string.replace(realtime_str_value, ',','',1))
    return realtime_value

def stock_pg_data(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'lxml')
    tr = soup.find_all('tr')
    trn = tr[5:] 
    stk_data_arry = {}
    
    for td in trn:
        tditem = td.find_all('td')
        
        r_date = str(tditem[0].string)
        his_date = r_date.strip()
        
        r_value = tditem[4].string
        his_value = float(string.replace(r_value, ',','',1))
        
        stk_data_arry[his_date] = his_value

    
    return stk_data_arry
        
    
def calculate_data(current_value, stock_pg_datalist,date):

    
    L_value = min(stock_pg_datalist.values())
    H_value = max(stock_pg_datalist.values())
    
    fmt = "%b %d, %Y"
    fmt2 = "%d"
    cal_days = 0

    for i in stock_pg_datalist.keys():
        hist_date = datetime.strptime(i, fmt)
        tframe = int((date-hist_date).days)

        if tframe >= cal_days:
            cal_days = tframe
    
    print "total cal days %s" % cal_days

    level_data = round(((current_value - L_value) / (H_value - L_value)) *100,1)
    valuelevel_str = str(level_data)+'%'
    
    return L_value, H_value, valuelevel_str, cal_days
    
def write_data(name, cid, L_value, H_value, valuelevel_str, current_value, bias, stock_id, cal_days):
    #write data into file
    stock_data[name] = (bias, stock_id, cid, L_value, H_value, current_value)
    
    line1 = '%s: %s (%s, %s) -- L_value is : %s, H_value is %s, current value is %s' % (bias, name, stock_id, cid, L_value, H_value, current_value)
    print line1
    
    line2 = 'Current level of this stock is: %s ... Total calculated days are %s' % (valuelevel_str, cal_days)
    print line2
    
    myfile = open(file_path, 'a')             # open for output (creates)
    myfile.writelines('<br>\n')
    myfile.writelines('* '+line1)        # write a line of text
    myfile.writelines('<br>\n')   
    myfile.writelines(line2)        # write a line of text
    myfile.writelines('<br>\n')
    myfile.close()
    
    
def output(date, file_path, bias, cid, name, stock_id, zone, yr):
    s_end_date = date - relativedelta(days=bias)
    s_start_date = date - relativedelta(years=yr)
    
    fmt = "%b"
    
    s_end_date_month_f = s_end_date.strftime(fmt)
    s_start_date_month_f = s_start_date.strftime(fmt)
    
    #print s_end_date, s_start_date
    
    startdate = '%s+%s+%s' % (s_start_date_month_f, s_start_date.day, s_start_date.year)
    enddate = '%s+%s+%s' % (s_end_date_month_f, s_end_date.day, s_end_date.year)
    print "URL using date end %s, start %s" % (enddate, startdate)
    
    num = '200'
    pg = ['0', '200', '400', '600', '800', '1000']
    url_list = []
    stock_pg_datalist = {}
    
    for i in range(yr+1):
        url_list.append('https://www.google.com/finance/historical?cid=%s&startdate=%s&enddate=%s&num=%s&start=%s' % (cid, startdate, enddate, num, pg[i]))
        
    #print url_list
    
    for i in url_list:
        stock_pg_datalist.update(stock_pg_data(i))
    
    current_value = realtime_data(stock_id)
    
    cal_data = calculate_data(current_value, stock_pg_datalist, date)
    
    write_data(name, cid, cal_data[0], cal_data[1], cal_data[2], current_value, zone, stock_id, cal_data[3])

def output2(date, file_path, stock_arry, yr):
    # group outputs
    
    for k in stock_arry:
        if stock_arry[k][0] == 'CN':
            bias = 1
        else: 
            bias = 3

    for k in stock_arry:
        if stock_arry[k][0] == 'CN':
            #for i in stock_arry.keys():
            output(date, file_path, bias, stock_arry[k][1], stock_arry[k][2], k, stock_arry[k][0], yr)

    for k in stock_arry:
        if stock_arry[k][0] == 'EU':
            #for i in stock_arry.keys():
            output(date, file_path, bias, stock_arry[k][1], stock_arry[k][2], k, stock_arry[k][0], yr)
            
    for k in stock_arry:
        if stock_arry[k][0] == 'AMERICAS':
            #for i in stock_arry.keys():
            output(date, file_path, bias, stock_arry[k][1], stock_arry[k][2], k, stock_arry[k][0], yr)
            
    for k in stock_arry:
        if stock_arry[k][0] == 'US/Topic':
            #for i in stock_arry.keys():
            output(date, file_path, bias, stock_arry[k][1], stock_arry[k][2], k, stock_arry[k][0], yr) 
            
    for k in stock_arry:
        if stock_arry[k][0] == 'AP':
            #for i in stock_arry.keys():
            output(date, file_path, bias, stock_arry[k][1], stock_arry[k][2], k, stock_arry[k][0], yr)
            
def read_stocks(stocks_path):
    # read stocks data in file
    f = open(stocks_path)
    lines = f.readlines()
    stock_dict = {}
    #print lines
    for line in lines:
        if line != '\n':
            #print line
            line_edit = line.split('-')
            if line_edit[0] == '1':
                stock_dict[line_edit[1]] = (line_edit[2], line_edit[3], line_edit[4])
    return stock_dict

if __name__ == "__main__":

    yr = 2
    file_path = '/srv/www/idehe.com/stock/index.html'
    stocks_path = '/srv/www/idehe.com/stock/test.txt'
    
    
    date = get_date()
    
    init(file_path, date, yr)
    
    stock_arry = read_stocks(stocks_path)
    #print stock_arry
    output2(date, file_path, stock_arry, yr)
    
    data_string = json.dumps(stock_data)
    print "ENCODED:",data_string
    