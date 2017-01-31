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
    print(support(itemset_a.union(itemset_b), transactions))
    return support(itemset_a.union(itemset_b), transactions) / support(itemset_a, transactions)

def apriori():
    pass
