import pattern_mining

with open('tests/reviews-sample.txt', 'r') as reviews:
    transactions = []

    for review in reviews:
        transaction = []
        for word in review.split():
            transaction.append(frozenset([word]))
        transactions.append(transaction)

    frequent_sequences, supports = \
        pattern_mining.get_frequent_sequences_2(
            transactions,
            min_support=100
        )

    with open('tests/results.txt', 'w') as results:
        for i, frequent_sequence in enumerate(frequent_sequences):
            elements = ''
            for item in frequent_sequence[0]:
                elements += item
            for element in frequent_sequence[1:]:
                for item in element:
                    elements += ';' + item
            results.write('{0}:{1}'.format(supports[i], elements))
            if i < (len(frequent_sequences) - 1):
                results.write('\n')
