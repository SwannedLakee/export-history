import sqlite3


def get_cursor(url):
    return sqlite3.connect(url).cursor()

db = sqlite3.connect('/Users/josephreddington/Library/Application Support/Firefox/Profiles/datm9h3r.default-1541155689776/places.sqlite')
cursor=db.cursor()
cursor.execute('''SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch'), moz_places.url FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id''')
print "here"
for row in cursor:
    print row
