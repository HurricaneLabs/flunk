import argparse

import yaml

from . import flunk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", default="facts.yml")
    ap.add_argument("-e", "--enumerate", default=False)
    ap.add_argument("-H", "--hostname", required=True)
    ap.add_argument("-u", "--username", required=True)
    ap.add_argument("-p", "--password", required=True)
    ap.add_argument("facts", nargs="*")
    args = ap.parse_args()

    with open(args.config, "r") as f:
        facts_config = yaml.load(f)

    facts = flunk(
        hostname=args.hostname,
        username=args.username,
        password=args.password,
        facts_config=facts_config,
        fact_list=args.facts,
        allow_enumerate=args.enumerate,
    )

    print(yaml.dump(facts, default_flow_style=False))
