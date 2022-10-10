import unittest
import export_history

def get_content(infilename):
        with open(infilename) as f:
                content = f.readlines()
        return content

class historyTest(unittest.TestCase):

    def test_hello(self):
        data=sorted(export_history.get_history_from_database('testinputs/testprofile/places.sqlite','firefox'))
        print(data)
        self.assertTrue("08:15" in data[0][0])

    def test_first_milseconds(self):
        data=sorted(export_history.get_history_from_database('testinputs/testprofile/places.sqlite','firefox'))
        self.assertEqual(1535962538426000,data[0][3])
        self.assertTrue("14:14" in data[0][0])

    def test_first_milseconds(self):
        data=sorted(export_history.get_history_from_database('testinputs/testprofile/places.sqlite','firefox'))
        self.assertEqual(1661091271297047,data[0][3])


if __name__=="__main__":
    unittest.main()
