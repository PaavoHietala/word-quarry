def find_closed_compound_words_optimized(word_list):
    word_set = set(word_list)
    compound_words = []
    memo = {}

    def is_compound(word):
        if word in memo:
            return memo[word]
        word_length = len(word)
        for i in range(1, word_length):
            first_part = word[:i]
            second_part = word[i:]
            if first_part in word_set:
                if second_part in word_set or is_compound(second_part):
                    memo[word] = True
                    return True
        memo[word] = False
        return False

    for word in word_list:
        if is_compound(word):
            compound_words.append(word)

    return compound_words

# Example usage
with open('finwords_clean.txt', 'r', encoding='utf-8') as f:
    word_list = f.read().split()

compound_words = find_closed_compound_words_optimized(word_list)
no_compounds = [word for word in word_list if word not in compound_words]

with open('finwords_noCompounds.txt', 'w') as f:
    f.write('word,length\n')
    for word in no_compounds[:-1]:
        f.write(f'{word},{len(word)}\n')
    f.write(f'{no_compounds[-1]},{len(no_compounds[-1])}')