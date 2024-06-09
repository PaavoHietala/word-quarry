import pandas as pd

df = pd.read_csv('finwords.csv', delimiter = '\t')

# Drop all words with less than 3 characters
df = df[df['Hakusana'].str.len() >= 3]

# Drop all compound words with a dash
df = df[df.Hakusana.str.contains('^[a-zA-Z][a-zA-Z]*$')]

# Drop all interjections
df = df[df.Sanaluokka != 'interjektio']

# Drop all abverbials
df = df[df.Sanaluokka != 'adverbi']

# Drop all compound words
#for index, row in df.iterrows():
#    df = df[~df.Hakusana.str.contains(row['Hakusana'])]

df['Hakusana'].to_csv('finwords_clean.txt', header = False, index = False)