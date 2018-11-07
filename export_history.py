import sqlite3


def get_cursor(url):
    return sqlite3.connect(url).cursor()


def get_all():
    cursor = sqlite3.connect('/Users/josephreddington/Library/Application Support/Firefox/Profiles/datm9h3r.default-1541155689776/places.sqlite').cursor()
    cursor.execute('''SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch'), moz_places.url FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id''')
    return cursor.fetchall()


def filter_by_date(matches, text):
    return_me=[]
    for row in matches:
        if text in row[0]:
            return_me.append(row)
    return return_me
            

if __name__=="__main__":
    for row in get_all():
        print row

