#!/usr/bin/env Rscript
library(tidyverse)
library(stringr)

args = commandArgs(trailingOnly=TRUE)

models = c("rnng", "tinylstm")

read_without_col_names = function(filename) {
    read_tsv(filename, col_names=F) %>%
       rename(model_word=X1, surprisal=X2) %>%
       mutate(model=filename) %>%
       separate(model, into=c("model", "trash"), sep="/") %>%
       select(-trash)
}

s = models %>%
    str_c("/", args[1]) %>%
    map(read_without_col_names) %>%
    reduce(bind_rows) %>%
    mutate(unk=if_else(str_detect(model_word, "UNK"), "True", "False"))

d = read_csv(args[2])

ds = replicate(length(models), d, simplify=F) %>%
    bind_rows() %>%
    filter(model == "gulordava") %>%
    select(-surprisal, -model, -model_word, -unk) %>%
    bind_cols(s) %>%
    mutate(test=(model_word == word) | unk=="True")

stopifnot(all(ds$test))

result = d %>%
    bind_rows(ds %>% select(-test))

write_csv(result, "combined_results_with_rnng_and_tinylstm.csv")
