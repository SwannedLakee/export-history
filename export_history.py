#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.parse
import sqlite3
import datetime
import urllib.request, urllib.parse, urllib.error
from collections import Counter


def get_history_from_database(filename, browser="firefox", start=0,end=0):
    cursor = sqlite3.connect(filename).cursor()
    if browser == "firefox": 
        if start==0:
            cursor.execute('''SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch'), moz_places.url, title , visit_date FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id''')
        else:  
            cursor.execute('''SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch'), moz_places.url, title , visit_date FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id and visit_date>{} and visit_date<{}'''.format(start,end))
    elif browser == "safari":
        cursor.execute("SELECT datetime(visit_time + 978307200, 'unixepoch', 'localtime') AS human_readable_time, url, title FROM history_visits INNER JOIN history_items ON history_items.id = history_visits.history_item;")
    else: 
        raise ValueError("Only supports 'firefox' or 'safari' as the browser argument")
    return cursor.fetchall()


def filter_by_date(matches, text): 
    return [x for x in matches if str(text) in str(x[0])]

def domain_filter(matches,use_blacklist=False):
    return_me=[]
    whitelist=open('whitelist.txt').read().split("\n")
    blacklist=open('blacklist.txt').read().split("\n")
    for row in matches:
        domain=urllib.parse.urlparse(row[1])[1]
        remove_path=True
        if use_blacklist:
           if domain not in blacklist:
                remove_path=False 
        else:
            if domain in whitelist: 
                remove_path=False 
        
        if remove_path:
            return_me.append((row[0],domain))
        else:
                ascii_title=""
                if row[2]:
                    ascii_title = row[2]

                return_me.append((row[0],"<a href=\"{}\">{}</a>".format(row[1],ascii_title)))

    return_me2=[]
    last_row=["a","b"]
    for row in return_me: 
        if row[0][:16] == last_row[0][:16]:
            if row[1] == last_row[1]:
                continue 
        return_me2.append(row)
        last_row=row
        
    return return_me2


def most_Common(lst): #from https://stackoverflow.com/a/20872750/170243
    data = Counter(lst)
    return_me="<h3> Most common sites</h3>\nWith number of accesses/minutes in parentheses<ol>"
    for row in data.most_common()[:30]:
        return_me+="<li>{} ({})</li>\n".format(row[0],row[1])
    return return_me+"</ol>"

def recent_domains(data):
    dic_domains={}
    for row in data:
        time=convert_to_time_zone(row[0])
        timestamp=time.strftime("%d/%m/%y %H:%M")
        domain=urllib.parse.urlparse(row[1])[1].replace("www.","").replace("mobile.","")
        dic_domains[domain]=timestamp
    return_me=
    for key in ['bbc.co.uk','twitter.com','facebook.com','linkedin.com']:
        print("{}: {}".format(key,dic_domains[key]))
    return ""


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
        writelist(data, html_file)

def writelist(data,html_file,name=""):
            common_domains=[row[1] for row in domain_filter(data)]
            html_file.write(most_Common(common_domains))
            html_file.write(recent_domains(data))
            html_file.write("<H3> Sites and times</H3>")
            last_annouced_date_string="xxx"
            for row in reversed(domain_filter(data)):
                time=convert_to_time_zone(row[0])
                time_string=time.strftime("%H:%M")
                date_string=time.strftime("%d/%m/%y")
                if last_annouced_date_string not in date_string:
                    html_file.write("<H3>{}</H3>".format(date_string))
                    last_annouced_date_string=date_string 
                print(date_string)
                outstring="<li> "+time_string+" "+row[1]+"\n"
                print(outstring)
                html_file.write(outstring)
            html_file.write("</ul>")

if __name__=="__main__":
    output_data(get_data_from_database())
