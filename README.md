# Translation Comparison

A work-in-progress Python program which obtains translations from the following APIs:

- Yandex    [Done]
- Microsoft [Done]
- Google    [Done]
- Lilt

It will also perform metrics on the returned translations, BLEU, for example.

## To-Do

- [ ] Add Lilt functionality (no termbase, default memory files).
- [ ] Add n-gram features for BLEU scores.
- [ ] Check APIs as some may provide own BLEU scores.
- [ ] Add ability to handle more than one reference/Gold_Std sentence.
- [ ] Add language look-up feature to check whether lang is valid, and to obtain
      the relevant codes for each API.
- [ ] Add date_time stamp to file outputs to avoid creating duplicates/overwriting.
- [ ] Add option for simple file with just source sentences, and no gold standard

- [ ] Create installation instructions.
- [ ] Create usage docs.

## Done

- [x] Added BLEU scores (prelim only, needs further investigation).
- [x] single_sentence_translate now returns a dictionary, rather than printing.
- [x] Added file_translate function which returns df with all API translations.
- [x] Modified the argparse "args" with relevant parameters.
