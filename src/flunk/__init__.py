import warnings

import requests
import yaml
from libweb.json import JsonService
from requests.packages.urllib3 import exceptions


def getSessionKey(hostname, username, password):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", exceptions.InsecureRequestWarning)
        r = requests.post(
            "https://%s:8089/services/auth/login?output_mode=json" % hostname,
            data={"username": username, "password": password},
            verify=False
        )
    return r.json()["sessionKey"]


def flunk(hostname, username, password, facts_config, fact_list=None, allow_enumerate=False):
    creds = {"splunk": "Splunk %s" % getSessionKey(hostname, username, password)}

    flunk = {}
    for fact in facts_config:
        conf = {
            "url": "https://%s:8089%s" % (hostname, fact["uri"]),
            "ignored_status_codes": [401, 403, 503],
            "params": {
                "output_mode": "json",
            },
            "auth": {
                "name": "splunk",
                "headers": ["Authorization"]
            },
            "jsonpath": fact["facts"],
            "verify_ssl": False
        }

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", exceptions.InsecureRequestWarning)
            for result in JsonService(creds=creds, **conf):
                flunk.update(result)

        if "enumerate" in fact and allow_enumerate:
            baseFact = list(fact["facts"].keys())[0]
            conf["url"] = "%s/{value}" % conf["url"]
            for value in flunk[baseFact]:
                conf["jsonpath"] = {
                    "%s.%s" % (baseFact, value): fact["enumerate"]
                }
                s = JsonService(creds=creds, opts={"value": value}, **conf)
                s.swallow_exceptions = False
                for result in s:
                    flunk.update(result)

    if fact_list:
        flunk = {k: v for (k, v) in flunk.items() if k in fact_list}

    return flunk
