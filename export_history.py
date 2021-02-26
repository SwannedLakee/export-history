#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.parse
import sqlite3
import datetime
import urllib.request, urllib.parse, urllib.error
from collections import Counter

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
        domain=urllib.parse.urlparse(row[1])[1]
        if domain not in whitelist: 
            return_me.append((row[0],domain))
        else:
                ascii_title=""
                if row[2]:
                    ascii_title = row[2].encode('ascii','ignore')

                return_me.append((row[0],"{} ({})".format(row[1],ascii_title)))
                print(row)

    return_me2=[]
    last_row=["a","b"]
    for row in return_me: 
        print("{} {}".format( row[0][:16] , last_row[0][:16]))
        if row[0][:16] == last_row[0][:16]:
            if row[1] == last_row[1]:
                print(row) 
                continue 
        return_me2.append(row)
        last_row=row
        
    return return_me2


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
                print(row) 
                time=convert_to_time_zone(row[0])
                time_string=time.strftime("%H:%M")
                outstring="<li> "+time_string+" "+row[1]+"\n"
                print(outstring)
                html_file.write(outstring)
            html_file.write("</ul>")


def convert_to_time_zone(time,zone='Europe/London'): 
#convert_to_time_zone("2020-07-25 20:19:07","London") 
    from datetime import datetime
    import pytz
    date = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    date = pytz.utc.localize(date)
    return  date.astimezone(pytz.timezone(zone))


def get_data_from_database():
    return sorted(get_history_from_database('databases/firefox.sqlite','firefox'))

def output_data(data):
    with open("history.html","w") as html_file:
        writelist(data,"", html_file)

if __name__=="__main__":
    firefox_data=get_data_from_database()
    output_data(firefox_data)
