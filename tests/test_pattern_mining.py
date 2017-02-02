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

"""Asserts that all the expected itemsets and their supports exist.

The order of the itemsets and supports doesn't matter. What matters is that each
itemset and its support has the same list index.

Parameters
----------
itemsets : list of frozenset
supports : list of float
expected : list of tuple
    First item in tuple is itemset and second is its support.

Returns
-------
bool
"""
def assert_expected_itemsets_supports(itemsets, supports, expected):
    for itemset in expected:
        index = itemsets.index(itemset[0])
        if supports[index] != itemset[1]:
            raise Exception('Expected itemset and support doesn\'t exist')


class PatternMining(unittest.TestCase):
    def test_returns_support_for_itemset_milk_bread(self):
        supports = pattern_mining.support([
            frozenset(['milk', 'bread'])
        ], transactions)

        self.assertEqual(supports[frozenset(['milk', 'bread'])], 2 / 7)

    def test_returns_support_for_itemset_bread(self):
        supports = pattern_mining.support([
            frozenset(['bread'])
        ], transactions)

        self.assertEqual(supports[frozenset(['bread'])], 5 / 7)

    def test_returns_support_for_itemsets_bread_and_milk_bread_and_bread_butter_jam(self):
        supports = pattern_mining.support([
            frozenset(['bread']),
            frozenset(['milk', 'bread']),
            frozenset(['bread', 'butter', 'jam'])
        ], transactions)

        self.assertEqual(supports[frozenset(['bread'])], 5 / 7),
        self.assertEqual(supports[frozenset(['milk', 'bread'])], 2 / 7),
        self.assertEqual(supports[frozenset(['bread', 'butter', 'jam'])], 2 / 7)

    def test_returns_0_for_support_when_itemset_not_in_transactions(self):
        supports = pattern_mining.support([frozenset(['bread', 'tea'])], transactions)

        self.assertEqual(supports[frozenset(['bread', 'tea'])], 0)

    def test_returns_confidence_for_rule_if_milk_then_bread(self):
        confidence = pattern_mining.confidence(
            frozenset(['milk']),
            frozenset(['bread']),
            transactions
        )

        self.assertEqual(confidence, (2 / 7) / (2 / 7))

    def test_returns_confidence_for_rule_if_bread_then_butter_jam(self):
        confidence = pattern_mining.confidence(
            frozenset(['bread']),
            frozenset(['butter', 'jam']),
            transactions
        )

        self.assertEqual(confidence, (2 / 7) / (5 / 7))

    def test_returns_0_confidence_when_union_of_itemsets_has_0_support(self):
        confidence = pattern_mining.confidence(
            frozenset(['bread']),
            frozenset(['butter', 'jam', 'tea']),
            transactions
        )

        self.assertEqual(confidence, 0)

    def test_returns_0_for_confidence_when_itemset_a_has_0_support(self):
        confidence = pattern_mining.confidence(
            frozenset(['bread', 'tea']),
            frozenset(['butter', 'jam']),
            transactions
        )

        self.assertEqual(confidence, 0)

    def test_returns_frequent_length_k_itemsets_and_supports(self):
        frequent_itemsets, supports = \
            pattern_mining.get_frequent_length_k_itemsets(transactions)

        assert_expected_itemsets_supports(frequent_itemsets, supports, [
            (frozenset(['milk']), 2 / 7),
            (frozenset(['bread']), 5 / 7),
            (frozenset(['butter']), 4 / 7),
            (frozenset(['jam']), 2 / 7)
        ])

    def test_returns_frequent_length_2_itemsets_and_supports(self):
        frequent_itemsets, supports = \
            pattern_mining.get_frequent_length_k_itemsets(transactions, k=2)

        assert_expected_itemsets_supports(frequent_itemsets, supports, [
            (frozenset(['milk', 'bread']), 2 / 7),
            (frozenset(['bread', 'butter']), 3 / 7),
            (frozenset(['bread', 'jam']), 2 / 7),
            (frozenset(['butter', 'jam']), 2 / 7)
        ])

    def test_returns_frequent_length_3_itemsets_and_supports(self):
        frequent_itemsets, supports = \
            pattern_mining.get_frequent_length_k_itemsets(transactions, k=3)

        assert_expected_itemsets_supports(frequent_itemsets, supports, [
            (frozenset(['bread', 'butter', 'jam']), 2 / 7)
        ])

    def test_returns_frequent_length_2_itemsets_and_supports_with_min_support_0_4(self):
        frequent_itemsets, supports = \
            pattern_mining.get_frequent_length_k_itemsets(
                transactions,
                min_support=0.4,
                k=2
            )

        assert_expected_itemsets_supports(frequent_itemsets, supports, [
            (frozenset(['bread', 'butter']), 3 / 7)
        ])

    def test_considers_only_frequent_itemsets_that_have_frequent_sub_itemsets(self):
        frequent_itemsets_1, supports_1 = \
            pattern_mining.get_frequent_length_k_itemsets(
                transactions,
                k=2,
                frequent_sub_itemsets=frozenset([
                    frozenset(['milk']),
                    frozenset(['bread'])
                ])
            )
        frequent_itemsets_2, supports_2 = \
            pattern_mining.get_frequent_length_k_itemsets(
                transactions,
                k=2,
                frequent_sub_itemsets=frozenset([
                    frozenset(['bread']),
                    frozenset(['jam'])
                ])
            )

        assert_expected_itemsets_supports(frequent_itemsets_1, supports_1, [
            (frozenset(['milk', 'bread']), 2 / 7)
        ])
        assert_expected_itemsets_supports(frequent_itemsets_2, supports_2, [
            (frozenset(['bread', 'jam']), 2 / 7)
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

    def test_returns_frequent_itemsets_and_supports(self):
        frequent_itemsets, supports = \
            pattern_mining.get_frequent_itemsets(transactions)

        assert_expected_itemsets_supports(frequent_itemsets, supports, [
            (frozenset(['milk']), 2 / 7),
            (frozenset(['bread']), 5 / 7),
            (frozenset(['butter']), 4 / 7),
            (frozenset(['jam']), 2 / 7),
            (frozenset(['milk', 'bread']), 2 / 7),
            (frozenset(['bread', 'butter']), 3 / 7),
            (frozenset(['bread', 'jam']), 2 / 7),
            (frozenset(['butter', 'jam']), 2 / 7),
            (frozenset(['bread', 'butter', 'jam']), 2 / 7)
        ])

    def test_returns_frequent_itemsets_and_supports_for_min_support_0_5(self):
        frequent_itemsets, supports = pattern_mining.get_frequent_itemsets(
            transactions,
            min_support=0.5
        )

        assert_expected_itemsets_supports(frequent_itemsets, supports, [
            (frozenset(['bread']), 5 / 7),
            (frozenset(['butter']), 4 / 7)
        ])

    def test_returns_frequent_itemsets_and_supports_for_min_support_0_6(self):
        frequent_itemsets, supports = pattern_mining.get_frequent_itemsets(
            transactions,
            min_support=0.6
        )

        assert_expected_itemsets_supports(frequent_itemsets, supports, [
            (frozenset(['bread']), 5 / 7)
        ])
