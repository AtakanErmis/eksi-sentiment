import unittest

from eksi import api


class APITestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_get_entry_by_id(self):
        from datetime import datetime
        entry = api.get_entry_by_id(1)
        self.assertEqual(entry['id'], 1)
        self.assertEqual(entry['owner'], 'ssg')
        self.assertEqual(entry['topic'], 'pena')
        self.assertIn('nesne', entry['body'])
        self.assertGreater(entry['fav'], 8000)
        self.assertEqual(entry['date'], datetime(1999, 2, 15))
    
    def test_get_entry_by_topic(self):
        entries = api.get_entries_by_topic('tupfraq')
        self.assertGreater(len(entries), 4)  # bu baslikta 5 entry var

        self.assertGreater(entries[0]['fav'], 3)
