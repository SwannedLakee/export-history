from unittest import TestCase
import unittest
import export_history

class exportTest(TestCase):

    def test_getcursor(self):
        cursor=export_history.get_cursor("confidentialtest.sqlite")
        cursor.execute('''SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch'), moz_places.url FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id''')
        allmatches=cursor.fetchall()
        self.assertEqual(len(allmatches),13126)



if __name__=="__main__":
    unittest.main()
