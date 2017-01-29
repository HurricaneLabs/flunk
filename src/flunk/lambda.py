import yaml

from . import flunk


def main(event, context):
    if "facts_config" not in event:
        with open("facts.yml", "r") as f:
            event["facts_config"] = yaml.load(f)
    return flunk(**event)
