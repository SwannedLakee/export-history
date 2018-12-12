#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urlparse
import sqlite3
import datetime
import urllib

def get_cursor(url):
    return sqlite3.connect(url).cursor()



def get_all_firefox():
    cursor = sqlite3.connect('firefox.sqlite').cursor()
    cursor.execute('''SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch'), moz_places.url FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id''')
    return cursor.fetchall()


def get_all_safari():
    cursor = sqlite3.connect('safari.db').cursor()
    cursor.execute('''SELECT 
  datetime(visit_time + 978307200, 'unixepoch', 'localtime')
    AS human_readable_time, url, title
FROM 
  history_visits
INNER JOIN 
  history_items ON
    history_items.id = history_visits.history_item;
''')
    return cursor.fetchall()


def filter_by_date(matches, text):
    return_me=[]
    for row in matches:
        if text in str(row[0]):
            return_me.append(row)
    return return_me
            

def privacy_morph(row, text,newtext=None):
      if newtext==None:
        newtext=text
      if row[1]==None:
        row=(row[0],"",row[2])
      if text in row[1]:
        return (row[0], newtext)
      else:
        return row


def googlecheck(row):
    if "oogle" in row[1]:
        o=urlparse.urlparse(row[1]) 
        query= urlparse.parse_qs(o[4])
        if 'q' in query:
            return (row[0], "Google: \""+query['q'][0]+"\"")
    return row

def remove_arguments(row):
    newstring=row[1].split("?")[0]
    return (row[0],newstring)

def domain_filter(matches):
    return_me=[]
    for row in matches: 
        o=urlparse.urlparse(row[1])
        newrow=(row[0],o[1])
        return_me.append(newrow)
    
    return return_me

def privacy_filter(matches):
    return_me=[]
    for row in matches: 
            newrow=row
            newrow=googlecheck(newrow)
            newrow=remove_arguments(newrow)
            newrow=privacy_morph(newrow,"https://m.facebook.com")
            newrow=privacy_morph(newrow,"https://www.linkedin.com")
            newrow=privacy_morph(newrow,"https://www.google.com/maps")
            newrow=privacy_morph(newrow,"http://designs.theopenvoicefactory.org")
            newrow=privacy_morph(newrow,"https://www.facebook.com")
            newrow=privacy_morph(newrow,"https://www.instagram.com")
            newrow=privacy_morph(newrow,"https://www.dropbox.com")
            newrow=privacy_morph(newrow,"https://accounts.google.com")
            newrow=privacy_morph(newrow,"https://mail.google.com")
            return_me.append(newrow)
    
    return return_me


def writelist(data,name,html_file):
            html_file.write("<H3>"+name+"<H3>")
            html_file.write("<ul>")
            for row in filter_by_date(domain_filter(data),date):
                outstring="<li> "+row[0][11:-3]+" "+row[1]
                html_file.write(outstring)
            html_file.write("</ul>")

if __name__=="__main__":
    with open("index.html","w") as html_file:
        number_of_days_to_go_back=10
        safari_data=sorted(get_all_safari())
        firefox_data=sorted(get_all_firefox())
        for i in range(number_of_days_to_go_back+1):
                date= str(datetime.date.today()-datetime.timedelta(number_of_days_to_go_back-i))
                html_file.write("<H2>{}<H2>".format(date))
                writelist(firefox_data,"Firefox",html_file)
                writelist(safari_data,"Safari (almost all iPhone)",html_file)



