""" Add documentation here """

import argparse
import json
import pandas
import requests
import supported_languages as langs
import private_api_config as api_cfg
# import api_config as api_cfg
from google.cloud import translate_v2 as google_trans

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


def microsoft_translate(text="hello", target_language="fr"):
    payload = {"to": target_language}
    body = [{"text": text}]
    ms_request = requests.post(api_cfg.MICROSOFT_ENDPOINT_URL, params=payload, headers=api_cfg.MS_HEADERS, json=body).json()
    return ms_request[0]["translations"][0]["text"]


def yandex_translate(text="hello", target_language="fr"):
    payload = {"key": api_cfg.YANDEX_API_KEY, "text": text, "lang": target_language}
    yan_request = requests.get(api_cfg.YANDEX_URL, params=payload).json()
    return yan_request["text"][0]


def google_translate(text="hello", target_language="fr"):
    translate_client = google_trans.Client()
    goo_request = translate_client.translate(text, target_language)
    return goo_request["translatedText"]
