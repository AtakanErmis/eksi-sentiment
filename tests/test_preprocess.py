import unittest

from eksi import preprocess


class PreprocessTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_remove_links(self):
        entry = \
            "beyler https://github.com/toprakozturk/eksi-sentiment diye bir " \
            "repo buldum super!"
        expected = \
            "beyler diye bir repo buldum super!"
        product = preprocess.remove_links(entry)
        self.assertEqual(expected, product)

    def test_remove_bkzs(self):
        entry = "lorem ipsum (bkz: dolor) sit amet"
        expected = "lorem ipsum sit amet"
        product = preprocess.remove_bkzs(entry)
        self.assertEqual(expected, product)

    def test_get_bkzs(self):
        entry = "(bkz: lorem ipsum) dolor sit (bkz: amet)"
        expected = ["lorem ipsum", "dolor"]
        product = preprocess.get_bkzs(entry)
        self.assertEqual(expected, product)

    def test_remove_numeric(self):
        entry = "lorem 12387 ipsum dolor sit 07 amet"
        expected = "lorem ipsum dolor sit amet"
        product = preprocess.remove_numeric(entry)
        self.assertEqual(expected, product)

    def test_stem(self):
        entry = "tabii bu sefer loremi ipsumu kullanamıyoruz"
        expected = "tabii bu sefer lorem ipsum kullan"
        product = preprocess.stem(entry)
        self.assertEqual(expected, product)

    def test_remove_stop_word(self):
        entry = "ben inanılmaz bir kod yazdım"
        expected = "inanılmaz kod yazdım"
        product = preprocess.remove_stop_words(entry)
        self.assertEqual(expected, product)
