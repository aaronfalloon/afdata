import itertools
import operator
import time


def support(transactions, itemsets):
    """Returns the percentages of transactions that contain the itemsets.

    Parameters
    ----------
    transactions : list of list
    itemsets : list of frozenset

    Returns
    -------
    dict
        Key of each item is the itemset and the value is the itemset's support
    """
    counts = {}
    for itemset in itemsets:
        counts[itemset] = 0
    for transaction in transactions:
        for itemset in itemsets:
            if itemset.issubset(transaction):
                counts[itemset] += 1
    supports = {}
    total_transactions = len(transactions)
    for itemset, count in counts.items():
        supports[itemset] = count / total_transactions
    return supports


def is_subsequence(sequence, candidate):
    """Returns true when the candidate is a subsequence of the sequence.

    Parameters
    ----------
    sequence : tuple of frozenset
    subsequence : tuple of frozenset

    Returns
    -------
    bool
    """
    if sequence_len(candidate) == 1:
        item = set(candidate[0]).pop()
        for itemset in sequence:
            if item in itemset:
                return True
    elif sequence_len(candidate) == 2:
        item_1 = set(candidate[0]).pop()
        item_2 = set(candidate[1]).pop()
        for i, itemset in enumerate(sequence):
            if item_1 in itemset:
                if i + 1 < len(sequence):
                    if item_2 in sequence[i + 1]:
                        return True
    else:
        for i, itemset in enumerate(sequence):
            if candidate[0].issubset(itemset):
                candidate_tail = candidate[1:]
                # Subtract 1 because the ith element has already been matched
                sequence_tail_length = len(sequence) - i - 1
                if not len(candidate_tail) > sequence_tail_length:
                    is_subsequence = True
                    # Check for the rest of the candidate sequence
                    for j, candidate_itemset in enumerate(candidate_tail):
                        if not candidate_itemset.issubset(sequence[i + (j + 1)]):
                            is_subsequence = False
                            break
                    if is_subsequence:
                        return True
    return False


def sequence_support(transactions, sequences):
    """Returns the percentages of transactions that contain the sequences.

    Parameters
    ----------
    transactions : list of list of list
    sequences : list of tuple of frozenset
        Each sequence is an ordered list of itemsets

    Returns
    -------
    dict
        Key of each item is the sequence (represented by a tuple) and the value
        is the sequence's support
    """
    counts = {}
    total_transactions = len(transactions)
    for sequence in sequences:
        counts[tuple(sequence)] = 0
    for i, transaction in enumerate(transactions):
        for sequence in sequences:
            if is_subsequence(transaction, sequence):
                counts[tuple(sequence)] += 1
    return counts


def confidence(transactions, itemset_a, itemset_b):
    """Returns the percentage of transactions that contain both itemset_a and
    itemset_b.

    Parameters
    ----------
    transactions : list of list
    itemset_a : frozenset
    itemset_b : frozenset

    Returns
    -------
    float
        Percentage of transactions that contain both itemset_a and itemset_b
    """
    itemset_a_support = support(transactions, [itemset_a])[itemset_a]
    if itemset_a_support == 0:
        return 0
    itemset_a_union_b = itemset_a.union(itemset_b)
    return support(transactions, [itemset_a_union_b])[itemset_a_union_b] \
        / itemset_a_support


def get_frequent_length_k_itemsets(transactions, min_support=0.2, k=1, frequent_sub_itemsets=None):
    """Returns all the length-k itemsets, from the transactions, that satisfy
    min_support.

    Parameters
    ----------
    transactions : list of list
    min_support : float, optional
        From 0.0 to 1.0. Percentage of transactions that should contain an
        itemset for it to be considered frequent.
    k : int, optional
        Length that the frequent itemsets should be
    frequent_sub_itemsets : frozenset of frozenset, optional
        Facilitates candidate pruning by the Apriori property. Length-k itemset
        candidates that aren't supersets of at least 1 frequent sub-itemset are
        pruned.

    Returns
    -------
    list of frozenset
    list of float
    """
    if min_support <= 0 or min_support > 1:
        raise ValueError('min_support must be greater than 0 and less than or equal to 1.0')
    if k <= 0:
        raise ValueError('k must be greater than 0')
    all_items = set()
    if frequent_sub_itemsets:
        for sub_itemset in frequent_sub_itemsets:
            all_items = all_items.union(sub_itemset)
    else:
        for transaction in transactions:
            all_items = all_items.union(transaction)
    all_length_k_itemsets = itertools.product(all_items, repeat=k)
    all_length_k_itemsets = frozenset(frozenset(itemset) for itemset in all_length_k_itemsets)
    all_length_k_itemsets = frozenset(filter(lambda itemset: len(itemset) == k, all_length_k_itemsets))
    # Remove itemsets that don't have a frequent sub-itemset to take advantage
    # of the Apriori property
    pruned_length_k_itemsets = all_length_k_itemsets
    if frequent_sub_itemsets:
        pruned_length_k_itemsets = set()
        for itemset in all_length_k_itemsets:
            has_frequent_sub_itemset = False
            for sub_itemset in frequent_sub_itemsets:
                if sub_itemset.issubset(itemset):
                    has_frequent_sub_itemset = True
            if has_frequent_sub_itemset:
                pruned_length_k_itemsets.add(itemset)
    frequent_itemsets = []
    frequent_supports = []
    supports = support(transactions, pruned_length_k_itemsets)
    for itemset, itemset_support in supports.items():
        if itemset_support >= min_support:
            frequent_itemsets.append(itemset)
            frequent_supports.append(itemset_support)
    return frequent_itemsets, frequent_supports


def get_frequent_itemsets(transactions, min_support=0.2):
    """Returns all the itemsets, from the transactions, that satisfy
    min_support.

    Uses the Apriori algorithm.

    Parameters
    ----------
    transactions : list of list
    min_support : float, optional
        From 0.0 to 1.0. Percentage of transactions that should contain an
        itemset for it to be considered frequent.

    Returns
    -------
    list of frozenset
    list of float
    """
    k = 1
    length_k_frequent_itemsets, length_k_supports = get_frequent_length_k_itemsets(
        transactions,
        min_support=min_support,
        k=k
    )
    frequent_itemsets = length_k_frequent_itemsets
    supports = length_k_supports
    while len(length_k_frequent_itemsets) > 0:
        k += 1
        length_k_frequent_itemsets, length_k_supports = get_frequent_length_k_itemsets(
            transactions,
            min_support=min_support,
            k=k,
            frequent_sub_itemsets=length_k_frequent_itemsets
        )
        frequent_itemsets += length_k_frequent_itemsets
        supports += length_k_supports
    return frequent_itemsets, supports


def sequence_len(sequence):
    """Returns the length of a sequence.

    Parameters
    ----------
    sequence : tuple of frozenset

    Returns
    -------
    int
    """
    total_len = 0
    for element in sequence:
        total_len += len(element)
    return total_len


def generate_candidate_sequences(length_k_sequences):
    """Generates length k + 1 candidate sequences from the length k sequences.

    Parameters
    ----------
    length_k_sequences : frozenset of tuple of frozenset

    Returns
    -------
    frozenset of tuple of frozenset
        Each tuple is a candidate sequence
    """
    example_len = sequence_len(next(iter(length_k_sequences)))
    for length_k_sequence in length_k_sequences:
        if sequence_len(length_k_sequence) != example_len:
            raise ValueError('k_length_sequences must all be the same length')
    candidates = set()
    for sequence in length_k_sequences:
        sequences_to_join_with = length_k_sequences.difference([sequence])
        for sequence_to_join_with in sequences_to_join_with:
            candidates.add(sequence + sequence_to_join_with)
    #if example_len == 1:
    #    for sequence in length_k_sequences:
    #        sequences_to_join_with = length_k_sequences.difference([sequence])
    #        for sequence_to_join_with in sequences_to_join_with:
    #            for element in sequence:
    #                for element_from_sequence_to_join_with in sequence_to_join_with:
    #                    candidates.add((frozenset(set(element).union(element_from_sequence_to_join_with)), ))
    return frozenset(candidates)


def get_frequent_length_k_sequences(transactions, min_support=0.2, k=1, frequent_sub_sequences=None):
    """Returns all the sequences, from the transactions, that satisfy
    min_support.

    Parameters
    ----------
    transactions : list of list of list
    min_support : float, optional
        From 0.0 to 1.0. Percentage of transactions that should contain a
        sequence for it to be considered frequent.
    k : int, optional
        Length that the frequent sequences should be
    frequent_sub_sequences : frozenset of tuple of frozenset, optional
        Facilitates candidate pruning by the Apriori property. Length-k sequence
        candidates that aren't supersets of at least 1 frequent sub-sequences
        are pruned.

    Returns
    -------
    list of frozenset
    list of float
    """
    items = set()
    for transaction in transactions:
        for itemset in transaction:
            items = items.union(itemset)
    sequences = []
    for item in items:
        sequences.append((frozenset([item]), ))
    supports = sequence_support(transactions, sequences)
    frequent_length_k_sequences = []
    frequent_supports = []
    for sequence, support in supports.items():
        if support >= 0.2:
            frequent_length_k_sequences.append(sequence)
            frequent_supports.append(support)
    return frequent_length_k_sequences, frequent_supports


def get_frequent_sequences(transactions, min_support=0.2):
    # Get frequent length-1 sequences
    items = []
    for transaction in transactions:
        for itemset in transaction:
            for item in itemset:
                items.append(item[0])
    items = frozenset(items)
    print('total items', len(items))
    sequences = []
    for item in items:
        sequences.append((frozenset([item]), ))
    supports = sequence_support(transactions, sequences)
    frequent_length_1_sequences = []
    frequent_length_1_supports = []
    for sequence, support in supports.items():
        if support >= min_support:
            frequent_length_1_sequences.append(sequence)
            frequent_length_1_supports.append(support)
    # Get frequent length-2 sequences
    print(len(frequent_length_1_sequences))
    candidates = generate_candidate_sequences(frozenset(frequent_length_1_sequences))
    print(len(candidates))
    supports = sequence_support(transactions, candidates)
    frequent_length_2_sequences = []
    frequent_length_2_supports = []
    for sequence, support in supports.items():
        if support >= min_support:
            frequent_length_2_sequences.append(sequence)
            frequent_length_2_supports.append(support)
    # Combine length-1 and length-2 sequences
    frequent_sequences = frequent_length_1_sequences + frequent_length_2_sequences
    frequent_supports = frequent_length_1_supports + frequent_length_2_supports
    return frequent_sequences, frequent_supports

def is_prefix(alpha, beta):
    n = sequence_len(alpha) - 1
    m = sequence_len(beta) - 1

    if m > n:
        return False, None

    for i in range(m):
        if beta[i] != alpha[i]:
            return False, None

    if not beta[m].issubset(alpha[m]):
        return False, None

    return True, m

def get_suffix(alpha, beta):
    result, m = is_prefix(alpha, beta)
    if not result:
        return None
    alpha = list(alpha)
    gamma = alpha[(m + 1):]
    return gamma

def get_projected_transactions(transactions, prefix):
    projected_transactions = []
    for transaction in transactions:
        for i in range(0, len(transaction)):
            result, m = is_prefix(transaction[i:], prefix)
            if result:
                suffix = get_suffix(transaction[i:], prefix)
                if sequence_len(suffix) > 0:
                    projected_transactions.append(suffix)
                    break;
    return projected_transactions

def get_frequent_sequences_2(transactions, min_support=100, prefix=[]):
    print('prefix', prefix)
    transactions_with_prefix = []
    items = []
    for transaction in transactions:
        transactions_with_prefix.append(prefix + transaction)
        for itemset in transaction:
            for item in itemset:
                items.append(item)
    items = frozenset(items)
    sequences_with_prefix = []
    for item in items:
        sequences_with_prefix.append(prefix + [frozenset([item])])
    supports = sequence_support(transactions_with_prefix, sequences_with_prefix)
    frequent_sequences = []
    frequent_supports = []
    for sequence, support in supports.items():
        if support >= min_support:
            frequent_sequences.append(list(sequence))
            frequent_supports.append(support)
    for frequent_sequence in frequent_sequences:
        projected_database = get_projected_transactions(transactions_with_prefix, frequent_sequence)
        frequent_sequences_from_projected, frequent_supports_from_projected = \
            get_frequent_sequences_2(projected_database, min_support=min_support, prefix=frequent_sequence)
        frequent_sequences += frequent_sequences_from_projected
        frequent_supports += frequent_supports_from_projected
    return frequent_sequences, frequent_supports
