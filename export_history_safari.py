#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urlparse
import sqlite3
import datetime
import urllib

# Todo
# (A) Put up for code review 

def get_history_from_database(filename, browser):
    cursor = sqlite3.connect(filename).cursor()
    if browser == "firefox": 
        cursor.execute('''SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch'), moz_places.url FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id''')
    elif browser == "safari":
        cursor.execute("SELECT datetime(visit_time + 978307200, 'unixepoch', 'localtime') AS human_readable_time, url, title FROM history_visits INNER JOIN history_items ON history_items.id = history_visits.history_item;")
    else: 
        raise ValueError("Only supports 'firefox' or 'safari' as the browser argument")
    return cursor.fetchall()

def filter_by_date(matches, text):
    return [x for x in matches if str(text) in str(x[0])]

def domain_filter(matches):
    return [(row[0],urlparse.urlparse(row[1])[1]) for row in matches]

def writelist(data,name,html_file):
            html_file.write("<H3>"+name+"<H3>\n<ul>")
            for row in domain_filter(data):
                outstring="<li> "+row[0][11:-3]+" "+row[1]+"\n"
                html_file.write(outstring)
            html_file.write("</ul>")

if __name__=="__main__":
    firefox_data=sorted(get_history_from_database('firefox.sqlite','firefox'))
    safari_data=sorted(get_history_from_database('safari.db','safari'))
    with open("index.html","w") as html_file:
        startdate=datetime.date(2018,12,10)
        for i in range((datetime.date.today()-startdate).days+1):
                html_file.write("<H2>{}<H2>".format(startdate+datetime.timedelta(i)))
                writelist(filter_by_date(firefox_data, startdate+datetime.timedelta(i)),"Firefox",html_file)
                writelist(filter_by_date(safari_data,startdate+datetime.timedelta(i)),"Safari (almost all iPhone)",html_file)
