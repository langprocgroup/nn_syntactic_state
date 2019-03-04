import os
import sys

import pandas as pd

conditions = {
    'transitive_short_nocomma_noblocker': ['Start', 'Transitive Verb', 'NP/Z', 'Verb', 'Rest'],
    'transitive_long_nocomma_noblocker': ['Start', 'Transitive Verb', 'NP/Z', 'Extension', 'Verb', 'Rest'],
    'intransitive_short_nocomma_noblocker': ['Start', 'Intransitive Verb', 'NP/Z', 'Verb', 'Rest'],
    'intransitive_long_nocomma_noblocker': ['Start', 'Intransitive Verb', 'NP/Z', 'Extension', 'Verb', 'Rest'],
    
    'transitive_short_comma_noblocker': ['Start', 'Transitive Verb', 'Comma', 'NP/Z', 'Verb', 'Rest'],
    'transitive_long_comma_noblocker': ['Start', 'Transitive Verb', 'Comma', 'NP/Z', 'Extension', 'Verb', 'Rest'],
    'intransitive_short_comma_noblocker': ['Start', 'Intransitive Verb', 'Comma', 'NP/Z', 'Verb', 'Rest'],
    'intransitive_long_comma_noblocker': ['Start', 'Intransitive Verb', 'Comma', 'NP/Z', 'Extension', 'Verb', 'Rest'],

    'transitive_short_nocomma_blocker': ['Start', 'Transitive Verb', 'Blocker', 'NP/Z', 'Verb', 'Rest'],
    'transitive_long_nocomma_blocker': ['Start', 'Transitive Verb', 'Blocker', 'NP/Z', 'Extension', 'Verb', 'Rest'],
    'intransitive_short_nocomma_blocker': ['Start', 'Intransitive Verb', 'Blocker', 'NP/Z', 'Verb', 'Rest'],
    'intransitive_long_nocomma_blocker': ['Start', 'Intransitive Verb', 'Blocker', 'NP/Z', 'Extension', 'Verb', 'Rest'],
    
    'transitive_short_comma_blocker': ['Start', 'Transitive Verb', 'Blocker', 'Comma', 'NP/Z', 'Verb', 'Rest'],
    'transitive_long_comma_blocker': ['Start', 'Transitive Verb', 'Blocker', 'Comma', 'NP/Z', 'Extension', 'Verb', 'Rest'],
    'intransitive_short_comma_blocker': ['Start', 'Intransitive Verb', 'Blocker', 'Comma', 'NP/Z', 'Verb', 'Rest'],
    'intransitive_long_comma_blocker': ['Start', 'Intransitive Verb', 'Blocker', 'Comma', 'NP/Z', 'Extension', 'Verb', 'Rest'],
}

add_end_region = True
autocaps = False

def expand_items(df):
    output_df = pd.DataFrame(rows(df))
    output_df.columns = ['sent_index', 'word_index', 'word', 'region', 'condition']
    return output_df

def rows(df):
    for condition in conditions:
        for sent_index, row in df.iterrows():
            word_index = 0
            for region in conditions[condition]:
                for word in row[region].split():
                    if autocaps and word_index == 0:
                        word = word.title()
                    yield sent_index, word_index, word, region, condition
                    word_index += 1
            if add_end_region:
                yield sent_index, word_index + 1, ".", "End", condition
                yield sent_index, word_index + 2, "<eos>", "End", condition
            
def main(filename):
    input_df = pd.read_excel(filename)
    output_df = expand_items(input_df)
    try:
        os.mkdir("tests")
    except FileExistsError:
        pass
    output_df.to_csv("tests/items.tsv", sep="\t")

if __name__ == "__main__":
    main(*sys.argv[1:])

