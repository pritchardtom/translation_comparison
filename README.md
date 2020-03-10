# Translation Comparison

A work-in-progress Python program which obtains translations from the following APIs:

- Yandex    [Done]
- Microsoft [Done]
- Google    [Done]
- Lilt

It will also perform metrics on the returned translations, BLEU, for example.

## To-Do

- Add function for dealing with input_file i.e., save file to pandas df, batch the translations, and save them to df.
        - Already written, just need to tweak to include in translator.py
- Add BLEU scores, and check API docs as some may provide this already.
        - Although, a few seem to produce a variant of this, i.e., confidence in the translation itself.
- The single_sentence_translate function should return a dictionary of the translations, rather than print them?
- Modify some of the args to be optional/required etc.  Check argparse doc for params.
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
