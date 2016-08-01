from html import HTML
import csv

                    
def html(stock_data_dict, date, html_path, csv_path):
    level_set = '15'
    title = 'GET ALL STOCK!'
    h = HTML()
    h.p(title)
    p = h.p
    p.br
    p.text('This is a stock test, get all the index value and see what is below %s %%' % level_set)
    p.br
    l = h.ol
    l.li('Record time is: ' + date.strftime('%Y-%m-%d %H:%M:%S'), 'date update every half an hour')
    l.li('Contact me if you have any suggestions, qq 2013986, email formblackt@gmail.com, or xueqiu hechao')
    l.li('first table will be the world index, second table focuses on domestic index')
    l.li('SHA is shanghai exchange, SHE is shenzhen exchange, AP is asia pacific, etc..')
    l.a(href=csv_path).li('Get the CSV file to download here!')

    t = h.table(border='2px', width ='70%', klass ='table table-bordered')
    t.th('Code')
    t.th('Name')
    t.th('Level')
    t.th('Exchange')
    t.th('CID')
    t.th('Note')
    t.th('L_value')
    t.th('Current_value')
    t.th('H_value')
    t.th('Days')
    
    group = ['SHA', 'SHE', 'CN/Topic', 'AP', 'AMERICAS', 'US/Topic', 'EU']
    for x in group:   
        for k in stock_data_dict:
            if k['Exchange'] == x:
                r = t.tr
                r.td(k['Code'])
                r.td(k['Name'])
                
                if float(k['Level'][:-1]) <= int(level_set):
                    r.td.b("***" + str(k['Level']))
                else:
                    r.td(str(k['Level']))
                    
                r.td(str(k['Exchange']))
                r.td(str(k['CID']))
                r.td(str(k['Note']))
                r.td(str(k['L_value']))
                r.td(str(k['Current_value']))
                r.td(str(k['H_value']))
                r.td(str(k['Days']))
                
    #print h
    myfile = open(html_path, 'w')
    #myfile.write
    
    html_file = '''
    <!DOCTYPE html>
    <html>
    <head>
    <title>GET ALL STOCK!</title>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
    <script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
    </head>
    <body>
    %s
    </body>
    </html>
    ''' % (h)
    
    myfile.writelines(html_file) 
    myfile.close()

