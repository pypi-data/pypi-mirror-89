import unittest

from hanlp_trie import TrieDict


class TestTrieDict(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.text = '第一个词语很重要，第二个词语也很重要'
        self.trie_dict = TrieDict({'重要': 'important'})

    def test_tokenize(self):
        self.assertEqual([(6, 8, 'important'), (16, 18, 'important')], self.trie_dict.tokenize(self.text))

    def test_split_batch(self):
        data = [self.text]
        new_data, new_data_belongs, parts = self.trie_dict.split_batch(data)
        predictions = [list(x) for x in new_data]
        print(self.trie_dict.merge_batch(data, predictions, new_data_belongs, parts))

    def test_tokenize_2(self):
        t = TrieDict({'次世代', '生产环境'})
        print(t.tokenize('2021年HanLPv2.1为生产环境带来次世代最先进的多语种NLP技术。'))


if __name__ == '__main__':
    unittest.main()
