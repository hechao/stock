from bs4 import BeautifulSoup
from urllib2 import urlopen
import string

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from html import HTML

stock_data = {}

import json

def get_date():
    # get time
    utc_time = datetime.utcnow()

    date = utc_time + timedelta(hours=8)

    return date
    
def read_stocklist(stocks_path):
    # read stocks data in file
    f = open(stocks_path)
    lines = f.readlines()
    custom_stocklist = {}
    #print lines
    for line in lines:
        if line != '\n':
            #print line
            line_edit = line.split('-')
            if line_edit[0] == '1':
                custom_stocklist[line_edit[1]] = (line_edit[2], line_edit[3], line_edit[4])
    return custom_stocklist

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
    
def get_current_stock_value(stock_id):
    # get current value of stock
    page = urlopen('https://www.google.com/finance?q=%s' % (stock_id))
    soup = BeautifulSoup(page, 'lxml')
    tr = soup.find_all('span')
    tr_8 = tr[8].find_all('span')
    realtime_str_value = tr_8[0].string
    realtime_value = float(string.replace(realtime_str_value, ',','',1))
    return realtime_value
    
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
    
    #print "total cal days %s" % cal_days
    level_data = round(((current_value - L_value) / (H_value - L_value)) *100,1)
    valuelevel_str = str(level_data)+'%'
    
    return L_value, H_value, valuelevel_str, cal_days
    
    
def output(date, bias, cid, name, stock_id, zone, yr):
    print bias
    s_end_date = date - relativedelta(days=bias)
    s_start_date = date - relativedelta(years=yr)
    
    fmt = "%b"
    
    s_end_date_month_f = s_end_date.strftime(fmt)
    s_start_date_month_f = s_start_date.strftime(fmt)
    
    #print s_end_date, s_start_date
    
    startdate = '%s+%s+%s' % (s_start_date_month_f, s_start_date.day, s_start_date.year)
    enddate = '%s+%s+%s' % (s_end_date_month_f, s_end_date.day, s_end_date.year)
    #print "URL using date end %s, start %s" % (enddate, startdate)
    
    num = '200'
    pg = ['0', '200', '400', '600', '800', '1000']
    url_list = []
    stock_pg_datalist = {}
    
    for i in range(yr+1):
        url_list.append('https://www.google.com/finance/historical?cid=%s&startdate=%s&enddate=%s&num=%s&start=%s' % (cid, startdate, enddate, num, pg[i]))
        
    #print url_list
    
    for i in url_list:
        stock_pg_datalist.update(stock_pg_data(i))
    
    current_value = get_current_stock_value(stock_id)
    
    cal_data = calculate_data(current_value, stock_pg_datalist, date)
    
    stock_data[name] = (cid, cal_data[0], cal_data[1], cal_data[2], current_value, zone, stock_id, cal_data[3])


def bias_output(date, stock_arry, yr):

    for k in stock_arry:
        if stock_arry[k][0] == 'CN':
            #for i in stock_arry.keys():
            output(date, 1, stock_arry[k][1], stock_arry[k][2], k, stock_arry[k][0], yr)
        else:
            output(date, 3, stock_arry[k][1], stock_arry[k][2], k, stock_arry[k][0], yr)
            
'''def dump(stock_data):
    data_string = json.dumps(stock_data)
    print "ENCODED:",data_string
    myfile = open(file_path, 'w')
    myfile.writelines(data_string)    
    myfile.close()'''
    
def html(stock_data):
    h = HTML()
    h.p('STOCK!')
    p = h.p
    p.br
    p.text('This is a stock test!')

    t = h.table(border='2px', width ='100%')
    t.th('name')
    t.th('CID Code')
    t.th('Lowest')
    t.th('Highest')
    t.th('Level')
    t.th('Current')
    t.th('Country')
    t.th('Code')
    t.th('Total Days')
    
    for k in stock_data:    
        r = t.tr
        r.td(k)
        r.td(stock_data[k][0])
        r.td(str(stock_data[k][1]))
        r.td(str(stock_data[k][2]))
        r.td(str(stock_data[k][3]))
        r.td(str(stock_data[k][4]))
        r.td(str(stock_data[k][5]))
        r.td(str(stock_data[k][6]))
        r.td(str(stock_data[k][7]))
        
                
    print h
    myfile = open(html_path, 'w')
    myfile.writelines(h)    
    myfile.close()

if __name__ == "__main__":

    yr = 2
    html_path = '/srv/www/idehe.com/stock/index.html'
    file_path = '/srv/www/idehe.com/stock/json.json'
    stocks_path = '/srv/www/idehe.com/stock/data/stock_hc.txt'
    
    date = get_date()
    
    #init(file_path, date, yr)
    
    custom_stocklist = read_stocklist(stocks_path)
    #print stock_arry
    
    bias_output(date, custom_stocklist, yr)
    #dump(stock_data)
    html(stock_data)
    