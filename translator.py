""" Add documentation here """

import argparse
import json
import pandas
import requests
import supported_languages as langs
import private_api_config as api_cfg
# import api_config as api_cfg
from google.cloud import translate_v2 as google_trans
from nltk.translate.bleu_score import sentence_bleu

################################################################################

def readfile(filename):
    """Read in a .csv and return a Pandas DataFrame"""
    try:
        return pandas.read_csv(filename, sep="|", names=["Source", "Gold_Std"])
    except FileNotFoundError:
        print("File not found.")
    except pandas.errors.ParserError:
        print("There was an error reading your csv file.")


def writefile(dataframe, filename):
    """Take a Pandas Dataframe, and save it to a filename."""
    try:
        dataframe.to_csv(filename, index=False, header=True)
    except OSError:
        print("There was an error writing your file.")


def language_verifier(string_from_args):
    """Take a language from args, and return if an accepted language."""
    pass
    # if string_from_args in langs.LANG_CODES:
        # call each service trans to check codes
        # return f"{string_from_args} is a supported language"


def microsoft_translate(text, source_language, target_language):
    payload = {"to": target_language}
    body = [{"text": text}]
    ms_request = requests.post(api_cfg.MICROSOFT_ENDPOINT_URL, params=payload, headers=api_cfg.MS_HEADERS, json=body).json()
    return ms_request[0]["translations"][0]["text"]


def yandex_translate(text, source_language, target_language):
    payload = {"key": api_cfg.YANDEX_API_KEY, "text": text, "lang": target_language}
    yan_request = requests.get(api_cfg.YANDEX_URL, params=payload).json()
    return yan_request["text"][0]


def google_translate(text, source_language, target_language):
    translate_client = google_trans.Client()
    goo_request = translate_client.translate(text, target_language, format_="text")
    return goo_request["translatedText"]


def single_sentence_translate(text, source_language, target_language):
    yandex = yandex_translate(text, source_language, target_language)
    microsoft = microsoft_translate(text, source_language, target_language)
    google = google_translate(text, source_language, target_language)
    results = {"Yandex": yandex, "Microsoft": microsoft, "Google": google}
    return results


def file_translate(dataframe, source_language, target_language):
    yandex_trans = []
    microsoft_trans = []
    google_trans = []
    for item in dataframe["Source"]:
        yandex_trans.append(yandex_translate(item, source_language, target_language))
        microsoft_trans.append(microsoft_translate(item, source_language, target_language))
        google_trans.append(google_translate(item, source_language, target_language))
    dataframe["Yandex_Translation"] = yandex_trans
    dataframe["Microsoft_Translation"] = microsoft_trans
    dataframe["Google_Translation"] = google_trans
    return dataframe


def calculate_bleu(dataframe):
    yandex_bleu = []
    microsoft_bleu = []
    google_bleu = []
    for idx in dataframe.index:
        ref_sentences = [dataframe["Gold_Std"][idx].split(" ")]
        yandex_sentences = dataframe["Yandex_Translation"][idx].split(" ")
        microsoft_sentences = dataframe["Microsoft_Translation"][idx].split(" ")
        google_sentences = dataframe["Google_Translation"][idx].split(" ")
        yandex_score = sentence_bleu(ref_sentences, yandex_sentences)
        microsoft_score = sentence_bleu(ref_sentences, microsoft_sentences)
        google_score = sentence_bleu(ref_sentences, google_sentences)
        yandex_bleu.append(yandex_score)
        microsoft_bleu.append(microsoft_score)
        google_bleu.append(google_score)
    dataframe["Yandex_BLEU"] = yandex_bleu
    dataframe["Microsoft_BLEU"] = microsoft_bleu
    dataframe["Google_BLEU"] = google_bleu
    return dataframe


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_file", help="Select the .csv file with source sentences.")
parser.add_argument("-o", "--output_file", help="Select a filename to save the results --> (not avail under '-s' option).")
parser.add_argument("-p", "--phrase", help="Translate a single phrase/sentence.  Result returned to stdout.")
parser.add_argument("-s", "--source_lang", help="Source language of input text/phrase.", default="en")
parser.add_argument("-t", "--trans_to", help="Language to translate source to.", default="fr")
args = parser.parse_args()


if args.phrase:
    ans = single_sentence_translate(args.phrase, args.source_lang, args.trans_to)
    print()
    print(f"Yandex....... {ans['Yandex']}")
    print(f"Microsoft.... {ans['Microsoft']}")
    print(f"Google....... {ans['Google']}")
    print()


if args.input_file:
    df = readfile(args.input_file)
    res = file_translate(df, args.source_lang, args.trans_to)
    bleu = calculate_bleu(res)
    writefile(bleu, args.output_file)
