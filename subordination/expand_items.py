import os
import sys

import pandas as pd

conditions = {
    'no-sub_1sc0_2sc0_no-matrix': ['Subordinate clause 1', 'Subordinate clause 2', 'Conclusion'],
    'no-sub_1sc0_2sc0_matrix': ['Subordinate clause 1', 'Subordinate clause 2', 'Main clause', 'Conclusion'],
    'sub_1sc0_2sc0_no-matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause 2', 'Conclusion'],
    'sub_1sc0_2sc0_matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause 2', 'Main clause', 'Conclusion'],
    'no-sub_1sc1_2sc0_no-matrix': ['Subordinate clause 1', 'Subordinate clause PP 1', 'Subordinate clause 2', 'Conclusion'],
    'no-sub_1sc1_2sc0_matrix': ['Subordinate clause 1', 'Subordinate clause PP 1', 'Subordinate clause 2', 'Main clause', 'Conclusion'],
    'sub_1sc1_2sc0_no-matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause PP 1', 'Subordinate clause 2', 'Conclusion'],
    'sub_1sc1_2sc0_matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause PP 1', 'Subordinate clause 2', 'Main clause', 'Conclusion'],
    'no-sub_1sc2_2sc0_no-matrix': ['Subordinate clause 1', 'Subordinate clause SRC 1', 'Subordinate clause 2', 'Conclusion'],
    'no-sub_1sc2_2sc0_matrix': ['Subordinate clause 1', 'Subordinate clause SRC 1', 'Subordinate clause 2', 'Main clause', 'Conclusion'],
    'sub_1sc2_2sc0_no-matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause SRC 1', 'Subordinate clause 2', 'Conclusion'],
    'sub_1sc2_2sc0_matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause SRC 1', 'Subordinate clause 2', 'Main clause', 'Conclusion'],    
    'no-sub_1sc3_2sc0_no-matrix': ['Subordinate clause 1', 'Subordinate clause ORC 1', 'Subordinate clause 2', 'Conclusion'],
    'no-sub_1sc3_2sc0_matrix': ['Subordinate clause 1', 'Subordinate clause ORC 1', 'Subordinate clause 2', 'Main clause', 'Conclusion'],
    'sub_1sc3_2sc0_no-matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause ORC 1', 'Subordinate clause 2', 'Conclusion'],
    'sub_1sc3_2sc0_matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause ORC 1', 'Subordinate clause 2', 'Main clause', 'Conclusion'],

    'no-sub_1sc0_2sc1_no-matrix': ['Subordinate clause 1', 'Subordinate clause 2', 'Subordinate clause PP 2', 'Conclusion'],
    'no-sub_1sc0_2sc1_matrix': ['Subordinate clause 1', 'Subordinate clause 2', 'Subordinate clause PP 2', 'Main clause', 'Conclusion'],
    'sub_1sc0_2sc1_no-matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause 2', 'Subordinate clause PP 2','Conclusion'],
    'sub_1sc0_2sc1_matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause 2', 'Subordinate clause PP 2','Main clause', 'Conclusion'],
    'no-sub_1sc1_2sc1_no-matrix': ['Subordinate clause 1', 'Subordinate clause PP 1', 'Subordinate clause 2', 'Subordinate clause PP 2', 'Conclusion'],
    'no-sub_1sc1_2sc1_matrix': ['Subordinate clause 1', 'Subordinate clause PP 1', 'Subordinate clause 2', 'Subordinate clause PP 2', 'Main clause', 'Conclusion'],
    'sub_1sc1_2sc1_no-matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause PP 1', 'Subordinate clause 2', 'Subordinate clause PP 2', 'Conclusion'],
    'sub_1sc1_2sc1_matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause PP 1', 'Subordinate clause 2', 'Subordinate clause PP 2','Main clause', 'Conclusion'],
    'no-sub_1sc2_2sc1_no-matrix': ['Subordinate clause 1', 'Subordinate clause SRC 1', 'Subordinate clause 2', 'Subordinate clause PP 2', 'Conclusion'],
    'no-sub_1sc2_2sc1_matrix': ['Subordinate clause 1', 'Subordinate clause SRC 1', 'Subordinate clause 2', 'Subordinate clause PP 2', 'Main clause', 'Conclusion'],
    'sub_1sc2_2sc1_no-matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause SRC 1', 'Subordinate clause 2', 'Subordinate clause PP 2', 'Conclusion'],
    'sub_1sc2_2sc1_matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause SRC 1', 'Subordinate clause 2', 'Subordinate clause PP 2', 'Main clause', 'Conclusion'],    
    'no-sub_1sc3_2sc1_no-matrix': ['Subordinate clause 1', 'Subordinate clause ORC 1', 'Subordinate clause 2', 'Subordinate clause PP 2', 'Conclusion'],
    'no-sub_1sc3_2sc1_matrix': ['Subordinate clause 1', 'Subordinate clause ORC 1', 'Subordinate clause 2', 'Subordinate clause PP 2', 'Main clause', 'Conclusion'],
    'sub_1sc3_2sc1_no-matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause ORC 1', 'Subordinate clause 2', 'Subordinate clause PP 2', 'Conclusion'],
    'sub_1sc3_2sc1_matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause ORC 1', 'Subordinate clause 2', 'Subordinate clause PP 2', 'Main clause', 'Conclusion'],

    'no-sub_1sc0_2sc2_no-matrix': ['Subordinate clause 1', 'Subordinate clause 2', 'Subordinate clause SRC 2', 'Conclusion'],
    'no-sub_1sc0_2sc2_matrix': ['Subordinate clause 1', 'Subordinate clause 2', 'Subordinate clause SRC 2', 'Main clause', 'Conclusion'],
    'sub_1sc0_2sc2_no-matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause 2', 'Subordinate clause SRC 2','Conclusion'],
    'sub_1sc0_2sc2_matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause 2', 'Subordinate clause SRC 2','Main clause', 'Conclusion'],
    'no-sub_1sc1_2sc2_no-matrix': ['Subordinate clause 1', 'Subordinate clause PP 1', 'Subordinate clause 2', 'Subordinate clause SRC 2', 'Conclusion'],
    'no-sub_1sc1_2sc2_matrix': ['Subordinate clause 1', 'Subordinate clause PP 1', 'Subordinate clause 2', 'Subordinate clause SRC 2', 'Main clause', 'Conclusion'],
    'sub_1sc1_2sc2_no-matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause PP 1', 'Subordinate clause 2', 'Subordinate clause SRC 2', 'Conclusion'],
    'sub_1sc1_2sc2_matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause PP 1', 'Subordinate clause 2', 'Subordinate clause SRC 2','Main clause', 'Conclusion'],
    'no-sub_1sc2_2sc2_no-matrix': ['Subordinate clause 1', 'Subordinate clause SRC 1', 'Subordinate clause 2', 'Subordinate clause SRC 2', 'Conclusion'],
    'no-sub_1sc2_2sc2_matrix': ['Subordinate clause 1', 'Subordinate clause SRC 1', 'Subordinate clause 2', 'Subordinate clause SRC 2', 'Main clause', 'Conclusion'],
    'sub_1sc2_2sc2_no-matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause SRC 1', 'Subordinate clause 2', 'Subordinate clause SRC 2', 'Conclusion'],
    'sub_1sc2_2sc2_matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause SRC 1', 'Subordinate clause 2', 'Subordinate clause SRC 2', 'Main clause', 'Conclusion'],    
    'no-sub_1sc3_2sc2_no-matrix': ['Subordinate clause 1', 'Subordinate clause ORC 1', 'Subordinate clause 2', 'Subordinate clause SRC 2', 'Conclusion'],
    'no-sub_1sc3_2sc2_matrix': ['Subordinate clause 1', 'Subordinate clause ORC 1', 'Subordinate clause 2', 'Subordinate clause SRC 2', 'Main clause', 'Conclusion'],
    'sub_1sc3_2sc2_no-matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause ORC 1', 'Subordinate clause 2', 'Subordinate clause SRC 2', 'Conclusion'],
    'sub_1sc3_2sc2_matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause ORC 1', 'Subordinate clause 2', 'Subordinate clause SRC 2', 'Main clause', 'Conclusion'],

    'no-sub_1sc0_2sc3_no-matrix': ['Subordinate clause 1', 'Subordinate clause 2', 'Subordinate clause ORC 2', 'Conclusion'],
    'no-sub_1sc0_2sc3_matrix': ['Subordinate clause 1', 'Subordinate clause 2', 'Subordinate clause ORC 2', 'Main clause', 'Conclusion'],
    'sub_1sc0_2sc3_no-matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause 2', 'Subordinate clause ORC 2','Conclusion'],
    'sub_1sc0_2sc3_matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause 2', 'Subordinate clause ORC 2','Main clause', 'Conclusion'],
    'no-sub_1sc1_2sc3_no-matrix': ['Subordinate clause 1', 'Subordinate clause PP 1', 'Subordinate clause 2', 'Subordinate clause ORC 2', 'Conclusion'],
    'no-sub_1sc1_2sc3_matrix': ['Subordinate clause 1', 'Subordinate clause PP 1', 'Subordinate clause 2', 'Subordinate clause ORC 2', 'Main clause', 'Conclusion'],
    'sub_1sc1_2sc3_no-matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause PP 1', 'Subordinate clause 2', 'Subordinate clause ORC 2', 'Conclusion'],
    'sub_1sc1_2sc3_matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause PP 1', 'Subordinate clause 2', 'Subordinate clause ORC 2','Main clause', 'Conclusion'],
    'no-sub_1sc2_2sc3_no-matrix': ['Subordinate clause 1', 'Subordinate clause SRC 1', 'Subordinate clause 2', 'Subordinate clause ORC 2', 'Conclusion'],
    'no-sub_1sc2_2sc3_matrix': ['Subordinate clause 1', 'Subordinate clause SRC 1', 'Subordinate clause 2', 'Subordinate clause ORC 2', 'Main clause', 'Conclusion'],
    'sub_1sc2_2sc3_no-matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause SRC 1', 'Subordinate clause 2', 'Subordinate clause ORC 2', 'Conclusion'],
    'sub_1sc2_2sc3_matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause SRC 1', 'Subordinate clause 2', 'Subordinate clause ORC 2', 'Main clause', 'Conclusion'],    
    'no-sub_1sc3_2sc3_no-matrix': ['Subordinate clause 1', 'Subordinate clause ORC 1', 'Subordinate clause 2', 'Subordinate clause ORC 2', 'Conclusion'],
    'no-sub_1sc3_2sc3_matrix': ['Subordinate clause 1', 'Subordinate clause ORC 1', 'Subordinate clause 2', 'Subordinate clause ORC 2', 'Main clause', 'Conclusion'],
    'sub_1sc3_2sc3_no-matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause ORC 1', 'Subordinate clause 2', 'Subordinate clause ORC 2', 'Conclusion'],
    'sub_1sc3_2sc3_matrix': ['Subordinator', 'Subordinate clause 1', 'Subordinate clause ORC 1', 'Subordinate clause 2', 'Subordinate clause ORC 2', 'Main clause', 'Conclusion'],                
    
}

add_end_region = False
autocaps = True

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

