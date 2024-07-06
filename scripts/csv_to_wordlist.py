import pandas as pd

def is_compound(word, memo, wordset):
    '''
    Check recursively if a word is a compound word.

    This function should be called from a wrapper function, which handles the
    <word>, <memo> and <wordset> variables.

    Parameters
    ----------
    word : str
        A word to be checked for compound wordiness
    memo : dict of str : bool
        List of pre-checked words and whether they are compound words to speed
        up the search / avoid checking the same words many times
    wordset : set
        Words to be checked, the set also naturally includes the words that
        might be a part of a compound word.

    Returns
    -------
    bool
        True if a word is a compound word, False otherwise
    '''

    if word in memo:
        return memo[word]
    
    word_length = len(word)

    for i in range(1, word_length):
        first_part = word[:i]
        second_part = word[i:]
        if first_part in wordset:
            if second_part in wordset or is_compound(second_part, memo, wordset):
                memo[word] = True
                return True

    memo[word] = False
    return False

def find_closed_compounds(wordlist):
    '''
    Find all closed compound words from <wordlist>

    Parameters
    ----------
    wordlist : list of str
        List of words to check

    Returns
    -------
    list of str
        List of closed compound words in given <wordlist>
    '''

    wordset = set(wordlist)
    compound_words = []
    memo = {}

    for word in wordlist:
        if is_compound(word, memo, wordset):
            compound_words.append(word)

    return compound_words

# Open the wordlist
df = pd.read_csv('finwords.csv', delimiter = '\t')

# Drop all words with less than 3 characters
df = df[df['Hakusana'].str.len() >= 3]

# Drop all compound words with a dash
df = df[df.Hakusana.str.contains('^[a-zA-Z][a-zA-Z]*$')]

# Drop all interjections
df = df[df.Sanaluokka != 'interjektio']

# Drop all abverbials
df = df[df.Sanaluokka != 'adverbi']

# Drop all closed compound words
wordlist = df["Hakusana"].to_list()

compound_words = find_closed_compounds(wordlist)
no_compounds = [word for word in wordlist if word not in compound_words]

# Write a file with a word, len(word) pair per line
with open('finwords_noCompounds.txt', 'w') as f:
    f.write('word,length\n')
    for word in no_compounds[:-1]:
        f.write(f'{word},{len(word)}\n')
    f.write(f'{no_compounds[-1]},{len(no_compounds[-1])}')
