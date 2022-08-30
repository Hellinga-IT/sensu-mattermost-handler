#!/usr/bin/python
import argparse
import sys
import json
from requests import get, post, put
from datetime import datetime
from pprint import pprint

def main():
    ## arguments
    parser = argparse.ArgumentParser(description='push events to mattermost webhook')
    parser.add_argument('-u', type=str, dest='url', required=True, help='the url to mattermost webhook')
    parser.add_argument('-s', dest='show_history', default=False, action=argparse.BooleanOptionalAction, help='show history of the trigger')
    args = parser.parse_args()

    # read event
    lines = sys.stdin.readlines()
    data = ""
    for line in lines:
        data = data.join(line)
    # create json obj from event
    obj = json.loads(data)
    history = "history: "
    if ((obj['check']['history'] is not None) and (args.show_history == True)):
        for hist in obj['check']['history']:
            dt = datetime.fromtimestamp(hist['executed'])
            history = history + "status: " + str(hist['status']) + " " + str(dt) + ", "
        message = obj['entity']['system']['hostname'] + ": " + obj['check']['output'] + " " + history
    else:
        message = obj['entity']['system']['hostname'] + ": " + obj['check']['output']

    event = {"text": message}
    r = post(args.url, data=json.dumps(event))

if __name__ == '__main__':
    main()
