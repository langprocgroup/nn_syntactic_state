#!/usr/bin/python3
from __future__ import print_function
import os
import sys
import glob
import functools

#import rfutils
import pandas as pd

UNK_TOKENS = {"<unk>", "<UNK>"}
FINAL_TOKENS = {"<eos>", "</S>", "</s>"}


# For running on Jenova with n-gram baseline
"""MODELS = {
    'google': [
        "python ~/code/lm_1b/lm_1b/eval_test_google.py --pbtxt ~/code/lm_1b/data/graph-2016-09-10.pbtxt --ckpt '../../../code/lm_1b/data/ckpt-*' --vocab_file ~/code/lm_1b/data/vocab-2016-09-10.txt --output_file {output_path} --input_file {input_path}",
    ],
    'gulordava': [
        "python ~/src/colorlessgreenRNNs/src/language_models/evaluate_target_word_test.py --checkpoint ~/src/colorlessgreenRNNs/src/hidden650_batch128_dropout0.2_lr20.0.pt --surprisalmode True --data ~/src/colorlessgreenRNNs/data/lm/English --prefixfile {input_path} --outf {output_path}",
    ],
    'kenlm': [
        'cat {input_path} | sed "s/ <eos>//g" | ~/src/kenlm/build/bin/query ~/src/kenlm/build/1b.mmap | python postprocess_kenlm.py > {output_path}',
    ],
}"""

# For running on Jenova
MODELS = {
    'google': [
        "python ~/code/lm_1b/lm_1b/eval_test_google.py --pbtxt ~/code/lm_1b/data/graph-2016-09-10.pbtxt --ckpt '../../../code/lm_1b/data/ckpt-*' --vocab_file ~/code/lm_1b/data/vocab-2016-09-10.txt --output_file {output_path} --input_file {input_path}",
    ],
    'gulordava': [
        "python ~/src/colorlessgreenRNNs/src/language_models/evaluate_target_word_test.py --checkpoint ~/src/colorlessgreenRNNs/src/hidden650_batch128_dropout0.2_lr20.0.pt --surprisalmode True --data ~/src/colorlessgreenRNNs/data/lm/English --prefixfile {input_path} --outf {output_path}",
    ]
}


# For Ethan runnign on the RCE server
"""MODELS = {
    'google': [
        "python ../../lm_1b/lm_1b/eval_test_google.py --pbtxt /nfs/projects/e/etw241/lm_1b/data/graph-2016-09-10.pbtxt --ckpt '../../lm_1b/data/ckpt-*' --vocab_file /nfs/projects/e/etw241/lm_1b/data/vocab-2016-09-10.txt --output_file {output_path} --input_file {input_path}",
    ],
    'gulordava': [
        "python ../../colorlessgreenRNNs/src/language_models/evaluate_target_word_test.py --checkpoint /nfs/projects/e/etw241/colorlessgreenRNNs/src/hidden650_batch128_dropout0.2_lr20.0.pt --surprisalmode True --data /nfs/projects/e/etw241/colorlessgreenRNNs/data/lm/English --prefixfile {input_path} --outf {output_path}",
    ]
}"""

# For Richard running locally
"""MODELS = {
    'google': [
        "python ~/src/models/research/lm_1b/eval_test_google.py --pbtxt ~/src/models/research/lm_1b/graph-2016-09-10.pbtxt --vocab_file ~/src/models/research/lm_1b/vocab-2016-09-10.txt --ckpt '/Users/canjo/src/models/research/lm_1b/ckpt/ckpt-*' --output_file {output_path} --input_file {input_path}",
    ],
    'gulordava': [
        "python ~/src/colorlessgreenRNNs/src/language_models/evaluate_target_word_test.py --checkpoint ~/src/colorlessgreenRNNs/src/hidden650_batch128_dropout0.2_lr20.0.pt --surprisalmode True --data ~/src/colorlessgreenRNNs/data/lm/English --prefixfile {input_path} --outf {output_path}",
    ],
}"""


    
def do_system_calls(cmds):
    for cmd in cmds:
        # We're making calls for effect; redirect stdout to stdout
        print("Running command: %s" % cmd, file=sys.stderr)
        os.system(cmd)
        #print(rfutils.system_call(cmd))

def run_model(model_name, input_path, output_path):
    return do_system_calls(
        cmd.format(input_path=input_path, output_path=output_path)
        for cmd in MODELS[model_name]
    )

def sentences(words):
    def gen():
        sentence = []
        for word in words:
            sentence.append(word)
            if is_final(word):
                yield tuple(sentence)
                sentence.clear()
    return map(" ".join, gen())

def is_unk(w):
    return w in UNK_TOKENS

def is_final(w):
    return w in FINAL_TOKENS

def run_models(path, conditions_df, models):
    # Write sentences to a txt file to be fed to the LSTMs
    input_filename = os.path.join(path, "input.txt")
    with open(input_filename, 'wt') as outfile:
        for sentence in sentences(conditions_df['word']):
            print(sentence, file=outfile)
            
    # Run the LSTMs by command line invocation
    def output_dfs():
        for model in models:
            output_filename = os.path.join(path, "%s_output.tsv" % model)
            print(output_filename)
            #run_model(model, input_filename, output_filename)
            output_df = pd.read_csv(
                os.path.join(output_filename),
                sep="\t",
                header=None,
                index_col=None,
                names=['model_word', 'surprisal']
            )
            output_df['model'] = model
            yield pd.concat([conditions_df, output_df], axis=1)

    # Combine results with conditions
    df = functools.reduce(pd.DataFrame.append, output_dfs())

    # Do some checking
    assert df.shape == (conditions_df.shape[0] * len(models), conditions_df.shape[1] + 3)
    df['unk'] = df['model_word'].map(is_unk)
    df['final'] = df['model_word'].map(is_final)
    print(df[(df['model_word'] != df['word']) & ~df['unk'] & ~df['final']])
    assert ((df['model_word'] == df['word']) | df['unk'] | df['final']).all()
    
    return df


def main(path, *models):
    if not models:
        models = MODELS
    path = os.path.abspath(path)
    # Read in the data
    conditions_df = pd.read_csv(
        os.path.join(path, "items.tsv"),
        sep="\t",
    )
    df = run_models(path, conditions_df, models)
    df.to_csv(os.path.join(path, "combined_results.csv"))

if __name__ == "__main__":
    main(*sys.argv[1:])
