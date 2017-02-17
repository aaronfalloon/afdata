import unittest
import afdata.pattern_mining as pattern_mining

transactions = [
    ['milk', 'bread'],
    ['butter'],
    ['beer', 'diapers'],
    ['milk', 'bread', 'butter'],
    ['bread'],
    ['butter', 'bread', 'jam'],
    ['butter', 'bread', 'jam'],
]

sequence_transactions = [
    [['the'], ['service', 'to', 'be', 'honest'], ['was'], ['kind', 'of'],
        ['poor']],
    [['the'], ['service'], ['was'], ['OK']],
    [['the'], ['service'], ['was'], ['terrible']],
    [['pity'], ['about'], ['the'], ['service']],
    [['9'], ['out'], ['of'], ['10'], ['for'], ['the'], ['pizza']],
    [['the'], ['pizza'], ['is'], ['so'], ['good']],
    [['seriously'], ['good'], ['pizza']],
    [['the'], ['pizza'], ['was'], ['awesome'], ['shame'], ['about'], ['the'],
        ['terrible', 'poor', 'service']],
    [['I'], ['will'], ['be'], ['back']],
    [['burritos'], ['burritos']],
]


def assert_expected_itemsets_supports(itemsets, supports, expected):
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
    for itemset in expected:
        index = itemsets.index(itemset[0])
        if supports[index] != itemset[1]:
            raise Exception('Expected itemset and support doesn\'t exist')


def assert_expected_sequences_supports(sequences, supports, expected):
    """Asserts that all the expected sequences and their supports exist.

    The order of the sequences and supports doesn't matter. What matters is that
    each
    itemset and its support has the same list index.

    Parameters
    ----------
    sequences : list of tuple of frozenset
    supports : list of float
    expected : list of tuple
        First item in the tuple is the sequence (tuple of frozenset) and the
        second is its support.

    Returns
    -------
    bool
    """
    for sequence, support in expected:
        index = itemsets.index(sequence[0])
        if supports[index] != support:
            raise Exception('Expected sequence and support doesn\'t exist')


class PatternMining(unittest.TestCase):
    def test_returns_support_for_itemset_milk_bread(self):
        supports = pattern_mining.support(transactions, [
            frozenset(['milk', 'bread']),
        ])

        self.assertEqual(supports[frozenset(['milk', 'bread'])], 2 / 7)

    def test_returns_support_for_itemset_bread(self):
        supports = pattern_mining.support(transactions, [
            frozenset(['bread']),
        ])

        self.assertEqual(supports[frozenset(['bread'])], 5 / 7)

    def test_returns_support_for_itemsets_bread_and_milk_bread_and_bread_butter_jam(self):
        supports = pattern_mining.support(transactions, [
            frozenset(['bread']),
            frozenset(['milk', 'bread']),
            frozenset(['bread', 'butter', 'jam']),
        ])

        self.assertEqual(supports[frozenset(['bread'])], 5 / 7),
        self.assertEqual(supports[frozenset(['milk', 'bread'])], 2 / 7),
        self.assertEqual(supports[frozenset(['bread', 'butter', 'jam'])], 2 / 7)

    def test_returns_0_for_support_when_itemset_not_in_transactions(self):
        supports = pattern_mining.support(transactions, [frozenset(['bread', 'tea'])])

        self.assertEqual(supports[frozenset(['bread', 'tea'])], 0)

    def test_returns_true_when_candidate_is_subsequence(self):
        sequence = [frozenset(itemset) for itemset in sequence_transactions[0]]

        self.assertTrue(pattern_mining.is_subsequence(sequence, (
            frozenset(['kind', 'of']),
            frozenset(['poor']),
        )))
        self.assertTrue(pattern_mining.is_subsequence(sequence, (
            frozenset(['honest']),
            frozenset(['was']),
            frozenset(['of']),
            frozenset(['poor']),
        )))
        self.assertTrue(pattern_mining.is_subsequence(sequence, (
            frozenset(['the']),
            frozenset(['service']),
            frozenset(['was']),
            frozenset([]),
            frozenset(['poor']),
        )))

    def test_returns_true_when_candidate_is_subsequence_even_with_false_start(self):
        # This sequence has two instances of "the". Hence, the notion of a false
        # start.
        sequence = [frozenset(itemset) for itemset in sequence_transactions[7]]

        self.assertTrue(pattern_mining.is_subsequence(sequence, (
            frozenset(['the']),
            frozenset(['terrible', 'service']),
        )))

    def test_returns_true_as_soon_as_candidate_determined_to_be_subsequence(self):
        sequence = [frozenset(itemset) for itemset in sequence_transactions[7]]

        self.assertTrue(pattern_mining.is_subsequence(sequence, (
            frozenset(['the']),
            frozenset(['pizza']),
        )))

    def test_returns_false_when_candidate_is_not_subsequence(self):
        sequence = [frozenset(itemset) for itemset in sequence_transactions[0]]

        self.assertFalse(pattern_mining.is_subsequence(sequence, (
            frozenset(['was']),
            frozenset(['kind', 'of']),
            frozenset(['great']),
        )))

        self.assertFalse(pattern_mining.is_subsequence(sequence, (
            frozenset(['awesome']),
        )))

    def test_returns_false_when_candidate_starts_to_match_but_too_long(self):
        sequence = [frozenset(itemset) for itemset in sequence_transactions[0]]

        self.assertFalse(pattern_mining.is_subsequence(sequence, (
            frozenset(['the']),
            frozenset(['service']),
            frozenset(['was']),
            frozenset(['poor']),
            frozenset(['many']),
            frozenset(['ways']),
            frozenset(['to']),
            frozenset(['improve']),
        )))

    def test_returns_support_for_sequence_the_pizza(self):
        sequence = (frozenset(['the']), frozenset(['pizza']))

        supports = pattern_mining.sequence_support(sequence_transactions, [
            sequence,
        ])

        self.assertEqual(supports[sequence], 3 / 10)

    def test_returns_support_for_sequence_the_service_was_poor(self):
        sequence = (
            frozenset(['the']),
            frozenset(['service']),
            frozenset(['was']),
            frozenset(['kind', 'of']),
            frozenset(['poor']),
        )

        supports = pattern_mining.sequence_support(sequence_transactions, [
            sequence,
        ])

        self.assertEqual(supports[sequence], 1 / 10)

    def test_returns_support_for_sequence_that_appears_twice_in_one_transaction(self):
        sequence = (
            frozenset(['burritos']),
        )

        supports = pattern_mining.sequence_support(sequence_transactions, [
            sequence,
        ])

        self.assertEqual(supports[sequence], 1 / 10)

    def test_returns_support_for_sequences(self):
        sequence_1 = (
            frozenset(['9']),
            frozenset(['out']),
            frozenset(['of']),
            frozenset(['10']),
        )
        sequence_2 = (
            frozenset(['the']),
            frozenset(['pizza']),
        )

        supports = pattern_mining.sequence_support(sequence_transactions, [
            sequence_1,
            sequence_2,
        ])

        self.assertEqual(supports[sequence_1], 1 / 10)
        self.assertEqual(supports[sequence_2], 3 / 10)

    def test_returns_support_when_sequence_not_in_transactions(self):
        sequence = (
            frozenset(['top']),
            frozenset(['curry']),
        )

        supports = pattern_mining.sequence_support(sequence_transactions, [
            sequence,
        ])

        self.assertEqual(supports[sequence], 0)

    def test_returns_confidence_for_rule_if_milk_then_bread(self):
        confidence = pattern_mining.confidence(
            transactions,
            frozenset(['milk']),
            frozenset(['bread']),
        )

        self.assertEqual(confidence, (2 / 7) / (2 / 7))

    def test_returns_confidence_for_rule_if_bread_then_butter_jam(self):
        confidence = pattern_mining.confidence(
            transactions,
            frozenset(['bread']),
            frozenset(['butter', 'jam']),
        )

        self.assertEqual(confidence, (2 / 7) / (5 / 7))

    def test_returns_0_confidence_when_union_of_itemsets_has_0_support(self):
        confidence = pattern_mining.confidence(
            transactions,
            frozenset(['bread']),
            frozenset(['butter', 'jam', 'tea']),
        )

        self.assertEqual(confidence, 0)

    def test_returns_0_for_confidence_when_itemset_a_has_0_support(self):
        confidence = pattern_mining.confidence(
            transactions,
            frozenset(['bread', 'tea']),
            frozenset(['butter', 'jam']),
        )

        self.assertEqual(confidence, 0)

    def test_returns_frequent_length_k_itemsets_and_supports(self):
        frequent_itemsets, supports = \
            pattern_mining.get_frequent_length_k_itemsets(transactions)

        assert_expected_itemsets_supports(frequent_itemsets, supports, [
            (frozenset(['milk']), 2 / 7),
            (frozenset(['bread']), 5 / 7),
            (frozenset(['butter']), 4 / 7),
            (frozenset(['jam']), 2 / 7),
        ])

    def test_returns_frequent_length_2_itemsets_and_supports(self):
        frequent_itemsets, supports = \
            pattern_mining.get_frequent_length_k_itemsets(transactions, k=2)

        assert_expected_itemsets_supports(frequent_itemsets, supports, [
            (frozenset(['milk', 'bread']), 2 / 7),
            (frozenset(['bread', 'butter']), 3 / 7),
            (frozenset(['bread', 'jam']), 2 / 7),
            (frozenset(['butter', 'jam']), 2 / 7),
        ])

    def test_returns_frequent_length_3_itemsets_and_supports(self):
        frequent_itemsets, supports = \
            pattern_mining.get_frequent_length_k_itemsets(transactions, k=3)

        assert_expected_itemsets_supports(frequent_itemsets, supports, [
            (frozenset(['bread', 'butter', 'jam']), 2 / 7),
        ])

    def test_returns_frequent_length_2_itemsets_and_supports_with_min_support_0_4(self):
        frequent_itemsets, supports = \
            pattern_mining.get_frequent_length_k_itemsets(
                transactions,
                min_support=0.4,
                k=2
            )

        assert_expected_itemsets_supports(frequent_itemsets, supports, [
            (frozenset(['bread', 'butter']), 3 / 7),
        ])

    def test_considers_only_frequent_itemsets_that_have_frequent_sub_itemsets(self):
        frequent_itemsets_1, supports_1 = \
            pattern_mining.get_frequent_length_k_itemsets(
                transactions,
                k=2,
                frequent_sub_itemsets=frozenset([
                    frozenset(['milk']),
                    frozenset(['bread']),
                ])
            )
        frequent_itemsets_2, supports_2 = \
            pattern_mining.get_frequent_length_k_itemsets(
                transactions,
                k=2,
                frequent_sub_itemsets=frozenset([
                    frozenset(['bread']),
                    frozenset(['jam']),
                ])
            )

        assert_expected_itemsets_supports(frequent_itemsets_1, supports_1, [
            (frozenset(['milk', 'bread']), 2 / 7),
        ])
        assert_expected_itemsets_supports(frequent_itemsets_2, supports_2, [
            (frozenset(['bread', 'jam']), 2 / 7),
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
            (frozenset(['bread', 'butter', 'jam']), 2 / 7),
        ])

    def test_returns_frequent_itemsets_and_supports_for_min_support_0_5(self):
        frequent_itemsets, supports = pattern_mining.get_frequent_itemsets(
            transactions,
            min_support=0.5
        )

        assert_expected_itemsets_supports(frequent_itemsets, supports, [
            (frozenset(['bread']), 5 / 7),
            (frozenset(['butter']), 4 / 7),
        ])

    def test_returns_frequent_itemsets_and_supports_for_min_support_0_6(self):
        frequent_itemsets, supports = pattern_mining.get_frequent_itemsets(
            transactions,
            min_support=0.6
        )

        assert_expected_itemsets_supports(frequent_itemsets, supports, [
            (frozenset(['bread']), 5 / 7),
        ])

    def test_returns_frequent_length_1_sequences_and_supports(self):
        frequent_sequences, supports = \
            pattern_mining.get_frequent_length_k_sequences(
                sequence_transactions,
                k=1
            )

        assert_expected_sequences_supports(frequent_sequences, supports, [
            ((frozenset(['the']), ), 7 / 10),
            ((frozenset(['service']), ), 5 / 10),
            ((frozenset(['be']), ), 2 / 10),
            ((frozenset(['was']), ), 4 / 10),
            ((frozenset(['of']), ), 2 / 10),
            ((frozenset(['poor']), ), 2 / 10),
            ((frozenset(['terrible']), ), 2 / 10),
            ((frozenset(['about']), ), 2 / 10),
            ((frozenset(['pizza']), ), 4 / 10),
            ((frozenset(['good']), ), 2 / 10),
        ])

    def test_returns_frequent_sequences_and_supports(self):
        frequent_sequences, supports = pattern_mining.get_frequent_sequences(
            sequence_transactions
        )

        self.assertCountEqual(frequent_sequences, [
            (frozenset(['the'])),
            (frozenset(['service'])),
            (frozenset(['be'])),
            (frozenset(['was'])),
            (frozenset(['of'])),
            (frozenset(['poor'])),
            (frozenset(['terrible'])),
            (frozenset(['about'])),
            (frozenset(['pizza'])),
            (frozenset(['good'])),
            (frozenset(['the']), frozenset(['service'])),
            (frozenset(['service']), frozenset(['was'])),
            (frozenset(['service']), frozenset(['was'])),
            (frozenset(['the']), frozenset(['pizza'])),
            (frozenset(['the']), frozenset(['pizza'])),
            (frozenset(['the']), frozenset(['service']), frozenset(['was']))
        ])
        self.assertCountEqual(frequent_sequences, [
            7 / 10,
            5 / 10,
            2 / 10,
            4 / 10,
            2 / 10,
            2 / 10,
            2 / 10,
            2 / 10,
            4 / 10,
            2 / 10,
            4 / 10,
            3 / 10,
            3 / 10,
            2 / 10,
            2 / 10,
            3 / 10,
        ])
