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

    def test_returns_0_for_support_when_itemset_not_in_transactions(self):
        support = pattern_mining.support(['bread', 'tea'], transactions)

        self.assertEqual(support, 0)

    def test_returns_confidence_for_rule_if_milk_then_bread(self):
        confidence = pattern_mining.confidence(
            ['milk'], ['bread'],
            transactions
        )

        self.assertEqual(confidence, (2 / 7) / (2 / 7))

    def test_returns_confidence_for_rule_if_bread_then_butter_jam(self):
        confidence = pattern_mining.confidence(
            ['bread'],
            ['butter', 'jam'],
            transactions
        )

        self.assertEqual(confidence, (2 / 7) / (5 / 7))

    def test_returns_0_confidence_when_union_of_itemsets_has_0_support(self):
        confidence = pattern_mining.confidence(
            ['bread'],
            ['butter', 'jam', 'tea'],
            transactions
        )

        self.assertEqual(confidence, 0)

    def test_returns_0_for_confidence_when_itemset_a_has_0_support(self):
        confidence = pattern_mining.confidence(
            ['bread', 'tea'],
            ['butter', 'jam'],
            transactions
        )

        self.assertEqual(confidence, 0)

    def test_returns_frequent_length_k_itemsets(self):
        frequent_itemsets = \
            pattern_mining.get_frequent_length_k_itemsets(transactions)

        self.assertCountEqual(frequent_itemsets, [
            {
                'itemset': frozenset(['milk']),
                'support': 2 / 7
            },
            {
                'itemset': frozenset(['bread']),
                'support': 5 / 7
            },
            {
                'itemset': frozenset(['butter']),
                'support': 4 / 7
            },
            {
                'itemset': frozenset(['jam']),
                'support': 2 / 7
            }
        ])

    def test_returns_frequent_length_2_itemsets(self):
        frequent_itemsets = \
            pattern_mining.get_frequent_length_k_itemsets(transactions, k=2)

        self.assertCountEqual(frequent_itemsets, [
            {
                'itemset': set(['milk', 'bread']),
                'support': 2 / 7
            },
            {
                'itemset': set(['bread', 'butter']),
                'support': 3 / 7
            },
            {
                'itemset': set(['bread', 'jam']),
                'support': 2 / 7
            },
            {
                'itemset': set(['butter', 'jam']),
                'support': 2 / 7
            }
        ])

    def test_returns_frequent_length_3_itemsets(self):
        frequent_itemsets = \
            pattern_mining.get_frequent_length_k_itemsets(transactions, k=3)

        self.assertCountEqual(frequent_itemsets, [
            {
                'itemset': set(['bread', 'butter', 'jam']),
                'support': 2 / 7
            }
        ])

    def test_returns_frequent_length_2_itemsets_with_min_support_0_4(self):
        frequent_itemsets = \
            pattern_mining.get_frequent_length_k_itemsets(
                transactions,
                min_support=0.4,
                k=2
            )

        self.assertCountEqual(frequent_itemsets, [
            {
                'itemset': set(['bread', 'butter']),
                'support': 3 / 7
            }
        ])

    def test_raises_exception_when_k_set_to_0(self):
        with self.assertRaisesRegex(ValueError, 'k must be greater than 0'):
            pattern_mining.get_frequent_length_k_itemsets(transactions, k=0)

    def test_raises_exception_when_min_support_less_than_0(self):
        with self.assertRaisesRegex(ValueError, 'min_support must be greater than 0 and less than or equal to 1.0'):
            pattern_mining.get_frequent_length_k_itemsets(transactions, min_support=-0.1)

    def test_raises_exception_when_min_support_equals_0(self):
        with self.assertRaisesRegex(ValueError, 'min_support must be greater than 0 and less than or equal to 1.0'):
            pattern_mining.get_frequent_length_k_itemsets(transactions, min_support=0)

    def test_raises_exception_when_min_support_greater_than_0(self):
        with self.assertRaisesRegex(ValueError, 'min_support must be greater than 0 and less than or equal to 1.0'):
            pattern_mining.get_frequent_length_k_itemsets(transactions, min_support=1.7)

    def test_returns_frequent_itemsets(self):
        frequent_itemsets = pattern_mining.get_frequent_itemsets(transactions)

        self.assertEquals(frequent_itemsets, [
            {
                'itemset': set(['milk']),
                'support': 2 / 7
            },
            {
                'itemset': set(['bread']),
                'support': 5 / 7
            },
            {
                'itemset': set(['butter']),
                'support': 4 / 7
            },
            {
                'itemset': set(['jam']),
                'support': 2 / 7
            },
            {
                'itemset': set(['milk', 'bread']),
                'support': 2 / 7
            },
            {
                'itemset': set(['bread', 'butter']),
                'support': 3 / 7
            },
            {
                'itemset': set(['bread', 'jam']),
                'support': 2 / 7
            },
            {
                'itemset': set(['butter', 'jam']),
                'support': 2 / 7
            },
            {
                'itemset': set(['bread', 'butter', 'jam']),
                'support': 2 / 7
            }
        ])

    def test_returns_frequent_itemsets_for_min_support_0_1(self):
        pass
