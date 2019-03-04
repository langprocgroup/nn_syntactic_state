import os
import sys

import pandas as pd

conditions = {
    'noblocker_short_nocomma': ['Start', 'Filler', 'Filler II', 'Embedded Verb', 'NP/Z', 'Verb'],
    'noblocker_long_nocomma': ['Start', 'Filler', 'Embedded Verb', 'NP/Z', 'Extension', 'Verb'],
    'noblocker_verylong_nocomma': ['Start', 'Embedded Verb', 'NP/Z', 'Extension', 'Extension II', 'Verb'],
    'blocker_short_nocomma': ['Start', 'Filler', 'Filler II', 'Embedded Verb', 'Object', 'NP/Z', 'Verb'],
    'blocker_long_nocomma': ['Start', 'Filler', 'Embedded Verb', 'Object', 'NP/Z', 'Extension', 'Verb'],
    'blocker_verylong_nocomma': ['Start', 'Embedded Verb', 'Object', 'NP/Z', 'Extension', 'Extension II', 'Verb'],

    'noblocker_short_comma': ['Start', 'Filler', 'Filler II', 'Embedded Verb', 'Comma', 'NP/Z', 'Verb'],
    'noblocker_long_comma': ['Start', 'Filler', 'Embedded Verb', 'Comma', 'NP/Z', 'Extension', 'Verb'],
    'noblocker_verylong_comma': ['Start', 'Embedded Verb', 'Comma', 'NP/Z', 'Extension', 'Extension II', 'Verb'],
    'blocker_short_comma': ['Start', 'Filler', 'Filler II', 'Embedded Verb', 'Object', 'Comma', 'NP/Z', 'Verb'],
    'blocker_long_comma': ['Start', 'Filler', 'Embedded Verb', 'Object', 'Comma', 'NP/Z', 'Extension', 'Verb'],
    'blocker_verylong_comma': ['Start', 'Embedded Verb', 'Object', 'Comma', 'NP/Z', 'Extension', 'Extension II', 'Verb'],    
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

