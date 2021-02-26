import unittest
import export_history

def get_content(infilename):
        with open(infilename) as f:
                content = f.readlines()
        return content

class historyTest(unittest.TestCase):

    def test_hello(self):
        data=sorted(export_history.get_history_from_database('databases/firefox.sqlite','firefox'))
        print(data[1])
        self.assertTrue("14:52" in data[1][0])

if __name__=="__main__":
    unittest.main()
