# coding: utf-8

import csv

def data_read(stock_data_path):
    data_list = []
    with open(stock_data_path) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='-',)
        for row in reader:
            data_list.append(row)
    
    #print data_list        
    return data_list
    
def csv_write(stock_data_list, csv_path):
    
    headers = stock_data_list[0].keys()
    #print headers
    
    with open(csv_path,'wb') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(stock_data_list)
        

if __name__ == "__main__":
    
    stock_data_path = '/srv/www/idehe.com/stock/data/test.csv'
    data_read(stock_data_path)