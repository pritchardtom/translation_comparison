# Translation Comparison

A work-in-progress Python program which obtains translations from the following APIs:

- Yandex    (https://translate.yandex.com/developers/keys)     
- Microsoft (https://docs.microsoft.com/en-us/azure/cognitive-services/translator/)
- Google    (https://cloud.google.com/translate/docs)
- Lilt      (https://lilt.com/docs/api)

It will also perform metrics on the returned translations, BLEU, for example.


## To-Do

- [ ] Put the Lilt payload into api_config file?
- [ ] Possibly alter function of -p arg to allow input() from user, rather than
      cramming everything into command line arg?
- [ ] Add option to save simple sentence translation to output file.
- [ ] Put supported languages in a .csv instead?
- [ ] Produce some performance measurements (time) on different requests,
      both in length of sentence, and separate portions of code.
- [ ] Add threading to speed up API requests.
- [ ] Look at using NIST in addition to BLEU/hLEPORE.
- [ ] Add hLEPORE metric analysis to translations.
- [ ] Add n-gram features for BLEU scores.
- [ ] Add ability to handle more than one reference/Gold_Std sentence in input file.
- [ ] Add language look-up feature to check whether lang is valid, and to obtain
      the relevant codes for each API.
- [ ] Add date_time stamp to file outputs to avoid creating duplicates/overwriting.
- [ ] Add option for simple file with just source sentences, and no gold standard
- [ ] Create installation instructions.
- [ ] Create usage docs.


## Done

- [x] Add Lilt functionality (no termbase, default memory files).
- [x] Check APIs as some may provide own BLEU scores.
- [x] Added BLEU scores (prelim only, needs further investigation).
- [x] single_sentence_translate now returns a dictionary, rather than printing.
- [x] Added file_translate function which returns df with all API translations.
- [x] Modified the argparse "args" with relevant parameters.
