# Translation Comparison

A work-in-progress Python program which obtains translations from the following APIs:

- Yandex
- Microsoft
- Google
- Lilt

It will also perform metrics on the returned translations, BLEU, for example.

## To-Do

- Modify some of the args to be optional/required etc.  Check argparse doc for params.
- Add date_time stamp to file outputs to avoid creating duplicates/overwriting.
- Add option for simple file with just source sentences, and no gold standard
