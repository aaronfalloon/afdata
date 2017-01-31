import unittest
import afdata.pattern_mining as pattern_mining

transactions = [
    ['milk', 'bread'],
    ['butter'],
    ['beer', 'diapers'],
    ['milk', 'bread', 'butter'],
    ['bread'],
    ['butter', 'bread', 'jam'],
    ['butter', 'bread', 'jam']
]

class PatternMining(unittest.TestCase):
    def test_returns_support_for_itemset_milk_bread(self):
        support = pattern_mining.support(['milk', 'bread'], transactions)

        self.assertEqual(support, 2 / 7)

    def test_returns_support_for_itemset_bread(self):
        support = pattern_mining.support(['bread'], transactions)

        self.assertEqual(support, 5 / 7)

    def test_returns_confidence_for_rule_if_milk_then_bread(self):
        confidence = pattern_mining.confidence(['milk'], ['bread'], transactions)

        self.assertEqual(confidence, (2 / 7) / (2 / 7))

    def test_returns_confidence_for_rule_if_bread_then_butter_jam(self):
        confidence = pattern_mining.confidence(['bread'], ['butter', 'jam'], transactions)

        self.assertEqual(confidence, (2 / 7) / (5 / 7))

    def test_returns_rules_with_min_support(self):
        pass
