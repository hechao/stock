# coding: utf-8

from bs4 import BeautifulSoup
from urllib2 import urlopen
import string

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def get_date():
    # get time
    utc_time = datetime.utcnow()

    date = utc_time + timedelta(hours=8)

    return date
    
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
    cal_data = {}
    
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
    
    cal_data['L_value'] = L_value
    cal_data['H_value'] = H_value
    cal_data['Level'] = valuelevel_str
    cal_data['Days'] = cal_days
    return cal_data
    
    
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
    
    cal_data['Current_value'] = current_value
    
    return cal_data

def group_output_dict(date, stocklist, yr):
    stock_data_list = []
    
    for k in stocklist:
        if k['Exchange'] == 'SHA':
            stock_data_output = output(date, 1, k['CID'], k['Name'], k['Code'], k['Exchange'], yr)
            k.update(stock_data_output)
            stock_data_list.append(k)
            
        elif k['Exchange'] == 'SHE':
            stock_data_output = output(date, 1, k['CID'], k['Name'], k['Code'], k['Exchange'], yr)
            k.update(stock_data_output)
            stock_data_list.append(k)
            
        elif k['Exchange'] == 'CN/Topic':
            stock_data_output = output(date, 1, k['CID'], k['Name'], k['Code'], k['Exchange'], yr)
            k.update(stock_data_output)
            stock_data_list.append(k)
            
        else:
            stock_data_output = output(date, 3, k['CID'], k['Name'], k['Code'], k['Exchange'], yr)
            k.update(stock_data_output)
            stock_data_list.append(k)

            
    #print stock_data_list
    return stock_data_list
    

    
'''def dump(stock_data):
    data_string = json.dumps(stock_data)
    print "ENCODED:",data_string
    myfile = open(file_path, 'w')
    myfile.writelines(data_string)    
    myfile.close()'''
    
if __name__ == "__main__":
    
    yr = 2
    date = get_date()
    
    group_output_lis(date, stock_arry, yr)
    