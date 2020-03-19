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
import timeit

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


def microsoft_translate(text, source_language, target_language):
    """Send a translate request to Microsoft API and return result."""
    payload = {"to": target_language}
    body = [{"text": text}]
    ms_request = requests.post(api_cfg.MICROSOFT_ENDPOINT_URL, params=payload, headers=api_cfg.MS_HEADERS, json=body).json()
    print("Microsoft called...")
    return ms_request[0]["translations"][0]["text"]


def yandex_translate(text, source_language, target_language):
    """Send a translate request to Yandex API and return result."""
    payload = {"key": api_cfg.YANDEX_API_KEY, "text": text, "lang": target_language}
    yan_request = requests.get(api_cfg.YANDEX_URL, params=payload).json()
    print("Yandex called...")
    return yan_request["text"][0]


def google_translate(text, target_language):
    """Send a translate request via Google's Python Cloud module and return result."""
    translate_client = google_trans.Client()
    goo_request = translate_client.translate(text, target_language, format_="text")
    print("Google called...")
    return goo_request["translatedText"]


def lilt_translate(mem_id, text):
    """
    Send a translate request to Lilt API and return result.
    NOTE: You must have an existing Lilt memory_id to run.
    """
    payload = {"key":api_cfg.LILT_API_KEY, "memory_id": mem_id, "source": text}
    lilt_request = requests.get(api_cfg.LILT_TRANSLATE_URL, params=payload).json()
    print("Lilt called...")
    return lilt_request[0]


def single_sentence_translate(text, source_language, target_language):
    """
    When selecting the arg -p or --phrase at CLI, returns individual sentence
    translation for each supported API.
    """
    yandex = yandex_translate(text, source_language, target_language)
    microsoft = microsoft_translate(text, source_language, target_language)
    google = google_translate(text, target_language)
    lilt = lilt_translate(api_cfg.LILT_TEST_MEMORY, text)
    results = {"Yandex": yandex, "Microsoft": microsoft, "Google": google, "Lilt": lilt}
    print(f"Yn time: {yan_end_t}")
    print(f"Ms time: {ms_end_t}")
    print(f"Go time: {goo_end_t}")
    print(f"Lt time: {lilt_end_t}")
    return results


def file_translate(dataframe, source_language, target_language):
    """
    When selecting the arg -i or --input_file at CLI, takes a Pandas
    DataFrame conversion of the .csv input file, and translates each source
    sentence contained within the DataFrame via the supported APIs.  Results are
    saved into DataFrame and returned.
    """
    yandex_trans = [yandex_translate(item, source_language, target_language) for item in dataframe["Source"]]
    microsoft_trans = [microsoft_translate(item, source_language, target_language) for item in dataframe["Source"]]
    google_trans = [google_translate(item, target_language) for item in dataframe["Source"]]
    lilt_trans = [lilt_translate(api_cfg.LILT_TEST_MEMORY, item) for item in dataframe["Source"]]
    dataframe["Yandex_Translation"] = yandex_trans
    dataframe["Microsoft_Translation"] = microsoft_trans
    dataframe["Google_Translation"] = google_trans
    dataframe["Lilt_Translation"] = lilt_trans
    return dataframe


def calculate_bleu(dataframe):
    """
    Reads the Gold_Std and API translations from DataFrame into
    separate lists, and uses the NLTK module to calculate each
    translation's BLEU score.  Results are saved to DataFrame and
    returned.
    """
    ref_sentences = []
    yandex_bleu = []
    microsoft_bleu = []
    google_bleu = []
    for idx in dataframe.index:
        ref_sentences = [dataframe["Gold_Std"][idx].split(" ")]
        yandex_sentences = dataframe["Yandex_Translation"][idx].split(" ")
        microsoft_sentences = dataframe["Microsoft_Translation"][idx].split(" ")
        google_sentences = dataframe["Google_Translation"][idx].split(" ")
        yandex_bleu.append(sentence_bleu(ref_sentences, yandex_sentences))
        microsoft_bleu.append(sentence_bleu(ref_sentences, microsoft_sentences))
        google_bleu.append(sentence_bleu(ref_sentences, google_sentences))
    dataframe["Yandex_BLEU"] = yandex_bleu
    dataframe["Microsoft_BLEU"] = microsoft_bleu
    dataframe["Google_BLEU"] = google_bleu
    return dataframe


def main():
    """
    Decides, depending on command line args passed, what functions to call on
    the inputed data, whether that's a csv file or a simple sentence, passed
    on the CLI.
    """
    start_t = timeit.default_timer()

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
        print(f"Lilt......... {ans['Lilt']}")
        print()

    if args.input_file:
        df = readfile(args.input_file)
        res = file_translate(df, args.source_lang, args.trans_to)
        writefile(res, args.output_file)
        # bleu = calculate_bleu(res)
        # writefile(bleu, args.output_file)

    end_t = timeit.default_timer()
    print(f"Total run time: {end_t}")


if __name__ == "__main__":
    main()
