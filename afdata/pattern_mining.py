def support(itemset, transactions):
    """Returns the percentage of transactions that contain the itemset.

    Parameters
    ----------
    itemset : list
    transactions : list of list

    Returns
    -------
    float
        Percentage of transactions that contain the itemset
    """
    contains_itemset = 0
    itemset = set(itemset)
    for transaction in transactions:
        if itemset.issubset(transaction):
            contains_itemset += 1
    return contains_itemset / len(transactions)


def confidence(itemset_a, itemset_b, transactions):
    """Returns the percentage of transactions that contain both itemset_a and
    itemset_b.

    Parameters
    ----------
    itemset_a : list
    itemset_b : list
    transactions : list of list

    Returns
    -------
    float
        Percentage of transactions that contain both itemset_a and itemset_b
    """
    itemset_a = set(itemset_a)
    itemset_a_support = support(itemset_a, transactions)
    if itemset_a_support == 0:
        return 0
    return support(itemset_a.union(itemset_b), transactions) \
        / itemset_a_support

def get_frequent_k_length_itemsets(transactions, min_support=0.2, k=1):
    """Returns all the k-length itemsets, from the transactions, that satisfy
    min_support.

    Parameters
    ----------
    transactions : list of list
    min_support : float, optional
        From 0.0 to 1.0. Percentage of transactions that should contain an
        itemset for it to be considered frequent.
    k : int
        Length that the frequent itemsets should be

    Returns
    -------
    list of dict
        Each dict contains itemset and support keys. itemset is type set and
        support is type float.

    """
    all_items = set()
    for transaction in transactions:
        all_items = all_items.union(transaction)
    k_length_itemsets = frozenset(map(lambda item: frozenset([item]), all_items))
    results = []
    for itemset in k_length_itemsets:
        itemset_support = support(itemset, transactions)
        if itemset_support >= min_support:
            results.append({
                'itemset': itemset,
                'support': itemset_support
            })
    return results

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
    list of dict
        Each dict contains itemset and support keys. itemset is type set and
        support is type float.

    """
    print(get_frequent_k_length_itemsets(transactions))
