import unittest
import export_history

def get_content(infilename):
        with open(infilename) as f:
                content = f.readlines()
        return content

class historyTest(unittest.TestCase):
# 
#     def test_hello(self):
#         data=sorted(export_history.get_history_from_database('1k2elc2y.Test/places.sqlite','firefox'))
#         print(data)
#         self.assertTrue("11:35" in data[0][0])
# 
#     def test_first_milseconds(self):
#         data=sorted(export_history.get_history_from_database('1k2elc2y.Test/places.sqlite','firefox'))
#         self.assertEqual(1665401723897728,data[0][3])
# 
#     def test_first_milseconds2(self):
#         data=sorted(export_history.get_history_from_database('1k2elc2y.Test/places.sqlite','firefox'))
#         self.assertEqual(1665401723897728,data[0][3])


if __name__=="__main__":
    unittest.main()
