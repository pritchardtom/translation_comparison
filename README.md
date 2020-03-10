# Translation Comparison

A work-in-progress Python program which obtains translations from the following APIs:

- Yandex    [Done]
- Microsoft [Done]
- Google    [Done]
- Lilt

It will also perform metrics on the returned translations, BLEU, for example.

## To-Do

- Investigate BLEU NLTK doc for best scores possible.
- Check API docs as some may provide their own BLEU scores too.
- Deal with erroneous languages by searching LANG_CODES.
  - Should also obtain the codes for each API too, "fr", "de", et cetera.
- Add date_time stamp to file outputs to avoid creating duplicates/overwriting.
- Add option for simple file with just source sentences, and no gold standard

- Create installation instructions:
  - Anaconda
    - conda create -n translate python=3.7 ...
    - packages used:
    - google-cloud-translate
    - uuid
    - pandas
    - requests
    - nltk
    - et cetera.
    - Google SDK
  - API Keys:
    - Yandex --> https://translate.yandex.com/developers/keys
    - Microsoft Azure
    - Google Translate
    - Lilt (if using)?

## Done

- Added BLEU scores (prelim only, needs further investigation).
- single_sentence_translate now returns a dictionary, rather than printing.
- Added file_translate function which returns df with all API translations.
- Modified the argparse "args" with relevant parameters.
