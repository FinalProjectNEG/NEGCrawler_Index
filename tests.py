import unittest

from pymongo import MongoClient

from DB import checkRepeatURL


class MyTestCase(unittest.TestCase):
    def test_repeatURL(self):
        cluster = MongoClient("mongodb://localhost:27017")
        db = cluster["NEG"]
        collection = db["facebook"]
        self.assertEqual(checkRepeatURL(collection, "https://facebook.com/"), True)


if __name__ == '__main__':
    unittest.main()
