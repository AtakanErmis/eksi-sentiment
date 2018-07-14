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
        self.assertTrue(isinstance(entry['fav'], int))
        self.assertEqual(entry['date'], datetime(1999, 2, 15))
    
    def test_get_entry_by_topic(self):
        entries = api.get_entries_by_topic('toprak')
        self.assertGreater(len(entries), 130)  # bu baslikta 132 entry var
