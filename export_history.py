import sqlite3
import datetime


def get_cursor(url):
    return sqlite3.connect(url).cursor()


def get_all():
    cursor = sqlite3.connect('/Users/josephreddington/Library/Application Support/Firefox/Profiles/datm9h3r.default-1541155689776/places.sqlite').cursor()
    cursor.execute('''SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch'), moz_places.url FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id''')
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
    if text in row[1]:
        return (row[0], newtext)
    else:
        return row



def privacy_filter(matches):
    return_me=[]
    for row in matches: 
            newrow=row
            newrow=privacy_morph(newrow,"https://www.linkedin.com")
            newrow=privacy_morph(newrow,"http://designs.theopenvoicefactory.org")
            newrow=privacy_morph(newrow,"https://www.facebook.com")
            newrow=privacy_morph(newrow,"https://www.dropbox.com")
            newrow=privacy_morph(newrow,"https://accounts.google.com")
            newrow=privacy_morph(newrow,"https://mail.google.com")
            return_me.append(newrow)
    
    return return_me

if __name__=="__main__":
    with open("index.html","w") as html_file:
        number_of_days_to_go_back=10
        for i in range(number_of_days_to_go_back+1):
                date= str(datetime.date.today()-datetime.timedelta(number_of_days_to_go_back-i))
                html_file.write("<H2>{}<H2><br>".format(date))
                html_file.write("<ul>")
                for row in filter_by_date(privacy_filter(get_all()),date):
                    html_file.write("<li> {}, {}".format(row[0][11:-3],row[1]))
                html_file.write("</ul>")



