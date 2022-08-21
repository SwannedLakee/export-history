import unittest
import export_history

def get_content(infilename):
        with open(infilename) as f:
                content = f.readlines()
        return content

class historyTest(unittest.TestCase):

    def test_hello(self):
        data=sorted(export_history.get_history_from_database('testinputs/testprofile/places.sqlite','firefox'))
        print(data[1])
        self.assertTrue("14:52" in data[1][0])

    def test_first_milseconds(self):
        data=sorted(export_history.get_history_from_database('testinputs/testprofile/places.sqlite','firefox'))
        print(data[1])
        self.assertEqual(1482159174330000,data[1][3])

    def test_todays_internet(self):
        data=export_history.get_history_from_database('testinputs/testprofile/places.sqlite','firefox', 1614334237000000)
        for record in data:
            print(record)

if __name__=="__main__":
    unittest.main()
