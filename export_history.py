#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urlparse
import sqlite3
import datetime
import urllib

# Todo
# (A) Put up for code eview 

def get_history_from_database(filename, browser):
    cursor = sqlite3.connect(filename).cursor()
    if browser == "firefox": 
        cursor.execute('''SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch'), moz_places.url, title FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id''')
    elif browser == "safari":
        cursor.execute("SELECT datetime(visit_time + 978307200, 'unixepoch', 'localtime') AS human_readable_time, url, title FROM history_visits INNER JOIN history_items ON history_items.id = history_visits.history_item;")
    else: 
        raise ValueError("Only supports 'firefox' or 'safari' as the browser argument")
    return cursor.fetchall()

def filter_by_date(matches, text):
    return [x for x in matches if str(text) in str(x[0])]

def domain_filter(matches):
    return_me=[]
    whitelist=open('whitelist.txt').read().split("\n")
    for row in matches:
	domain=urlparse.urlparse(row[1])[1]
	if domain not in whitelist:	
	    return_me.append((row[0],domain))
	else:
            ascii_title=""
            if row[2]:
                ascii_title = row[2].encode('ascii','ignore')

	    return_me.append((row[0],"{} ({})".format(row[1],ascii_title)))
            print row

    return_me2=[]
    last_row=["a","b"]
    for row in return_me: 
        print "{} {}".format( row[0][:16] , last_row[0][:16])
        if row[0][:16] == last_row[0][:16]:
            if row[1] == last_row[1]:
                print row 
                continue 
        return_me2.append(row)
        last_row=row
		
    return return_me2

from collections import Counter

def Most_Common(lst): #from https://stackoverflow.com/a/20872750/170243
    data = Counter(lst)
    return_me="<h3> Most common sites</h3>\nWith number of accesses/minutes in parentheses<ol>"
    for row in data.most_common():
        return_me+="<li>{} ({})</li>\n".format(row[0],row[1])
    return return_me+"</ol>"


def writelist(data,name,html_file):
            #html_file.write("<H3>"+name+"<H3>\n<ul>")
            common_domains=[row[1] for row in domain_filter(data)]
            html_file.write(Most_Common(common_domains))
            html_file.write("<H3> Sites and times</H3>")
            for row in domain_filter(data):
                outstring="<li> "+row[0][11:-3]+" "+row[1]+"\n"
                print outstring
                html_file.write(outstring)
            html_file.write("</ul>")

if __name__=="__main__":
    firefox_data=sorted(get_history_from_database('databases/firefox.sqlite','firefox'))
    safari_data={} 
#sorted(get_history_from_database('databases/safari.db','safari'))
    with open("history.html","w") as html_file:
        startdate=datetime.date(2018,12,10)
        for i in reversed(range((datetime.date.today()-startdate).days+1)):
                html_file.write("<H2>{}<H2>".format(startdate+datetime.timedelta(i)))
                writelist(filter_by_date(firefox_data, startdate+datetime.timedelta(i)),"Firefox",html_file)
#                writelist(filter_by_date(safari_data,startdate+datetime.timedelta(i)),"Safari (almost all iPhone)",html_file)
