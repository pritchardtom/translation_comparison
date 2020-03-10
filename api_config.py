"""
This is where you should put all your API keys and endpoint URLs, et cetera.
"""

import uuid


################################################################################
# YANDEX

YANDEX_API_KEY = "<insert API Key within quotes>"
YANDEX_URL = "<insert URL within quotes>"


################################################################################
# MICROSOFT

MICROSOFT_API_VER = "/translate?api-version=3.0"
MICROSOFT_API_KEY = "<insert API Key within quotes>"
MICROSOFT_ENDPOINT_URL = "https://api.cognitive.microsofttranslator.com/" + MICROSOFT_API_VER
MS_KEY_VAR = "TRANSLATOR_TEXT_SUBSCRIPTION_KEY" # subscription key for Translator resource
MS_ENDPOINT_VAR = "TRANSLATOR_TEXT_ENDPOINT"         # global endpoint for Translator resource

# required for auth to Azure:
MS_HEADERS = {
    'Ocp-Apim-Subscription-Key': MICROSOFT_API_KEY,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}


################################################################################
# GOOGLE

GOOGLE_JSON = "<insert path to google project .json file within quotes>"

################################################################################
