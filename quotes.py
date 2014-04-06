import urllib
from ctypes import *
import re
import datetime
import sys
import os

RED = 12
GREEN = 10
YELLOW = 14
BLUE = 1
DEFAULT = 15

month_to_int = {
    'Jan':1,
    'Feb':2,
    'Mar':3,
    'Apr':4,
    'May':5,
    'Jun':6,
    'Jul':7,
    'Aug':8,
    'Sep':9,
    'Oct':10,
    'Nov':11,
    'Dec':12
}
def set_color(color):
	#mac or linux
	if os.name == "posix":
		pass
	#windows
	else:
		windll.Kernel32.GetStdHandle.restype = c_ulong
		h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))
		windll.Kernel32.SetConsoleTextAttribute(h, color)

class Symbol:
    def __init__(self, symbol):
        self.symbol = symbol
        self.price = None
        self.change = None
    def print_color(self):
        #for i in range(16):
        #    set_color(i)
        #    print i
        today = datetime.datetime.today()
        date_today = datetime.datetime(today.year, today.month, today.day)
        if self.date == 'N/A':
            set_color(YELLOW)
        elif self.date < date_today:
            set_color(BLUE)
        else:
            if self.change == "N/A":
                set_color(BLUE)
            elif float(self.change[:-1]) < 0:
                set_color(RED)
            else:
                set_color(GREEN)
        print self
        set_color(DEFAULT)
        
    def parse_date(self, date_str):
        
        fields = re.split(' +', date_str)
        if len(fields) == 1:
            today = datetime.datetime.today()
            
            self.date = datetime.datetime(today.year, today.month, today.day)
        else:
            today = datetime.datetime.today()
            self.date = datetime.datetime(today.year, month_to_int[fields[0]], int(fields[1]))


    def __unicode__(self):
        return self.symbol + "\t" + self.price + "\t" + self.change
    def __str__(self):
        return self.symbol + "\t" + self.price + "\t" + self.change + "\t" + str(self.date)
        
def get_price(symbol):
    try:
        if(symbol == '^DJI'):
            page = urllib.urlopen('http://download.finance.yahoo.com/q?s=^DJI')
        else:
            page = urllib.urlopen('http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=cl' % (symbol))
        text = page.read()
    
    except:
        #print sys.exc_info()[0]
        s = Symbol(symbol + ' -- error retreiving quote')
        s.change = 'N/A'
        s.price = 'N/A'
        s.date = 'N/A'
        return s
    try:
        s = Symbol(symbol)
        fields = re.split(',', text)

        s.change = re.split(' - ', fields[0])[1][:-1]
        s.price = re.search("<b>.*</b>", fields[1]).group(0)[3:-4]
        date_field = re.split(" - ", fields[1])[0][1:]
        s.price = "%.2f" % (float(s.price))
        s.parse_date(date_field)
    except :
        print sys.exc_info()[0]
        s = Symbol(symbol + ' -- parsing error: ' + text)
        
        s.change = 'N/A'
        s.price = 'N/A'
        s.date = 'N/A'
        
    return s

get_price('EXWAX').print_color()
get_price('PRWCX').print_color()
get_price('QQQ').print_color()
get_price('INFA').print_color()
get_price('^GSPC').print_color()
get_price('FB').print_color()
get_price('SSNI').print_color()
get_price('AAPL').print_color()
get_price('^VIX').print_color()


#check for other quotes
print
print "Press Enter to exit"
print "Enter another symbol and press Enter to get quote"
while True:
    input = raw_input()
    if input:
        q = get_price(input)
        q.print_color()
    else:
        exit()


