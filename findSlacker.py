#!/usr/bin/env python

import requests
import json
import sys
import re


class FindSlacker():

    def __init__(self):
        self.process_args()

        with open('config.json', 'r') as f:
            config = json.load(f)
        self.url = config['url']
        self.api_token = config['api_token']

    def process_args(self):
        if len(sys.argv) < 2:
            print 'Missing argument, must supply search pattern'
            sys.exit(1)
        self.pattern = sys.argv[1]

    def get_member_data(self):
        try:
            response = requests.get(
                url=self.url,
                params={
                    "token": self.api_token,
                    "presence": "1",
                },
            )
            member_data = json.loads(response.content)

        except requests.exceptions.RequestException:
            print 'HTTP Request failed!'

        return member_data['members']

    def find_member(self):
        members = self.get_member_data()

        matches = []

        for member in members:

            # Slackbot is formatted differently and breaks, and we'll never
            # need to delete it anyway.
            if member['name'] == 'slackbot':
                continue

            # Ignore deleted users
            if member['deleted']:
                continue

            if re.search(self.pattern, member['name'], re.IGNORECASE):
                if member not in matches:
                    matches.append(member)

            if re.search(self.pattern, member['profile']['real_name'],
                         re.IGNORECASE):
                if member not in matches:
                    matches.append(member)

            if re.search(self.pattern, member['profile']['email'],
                         re.IGNORECASE):
                if member not in matches:
                    matches.append(member)

        for match in matches:
            print 'User %s:' % match['name']
            print '    Full Name:     %s' % match['profile']['real_name']
            print '    Email Address: %s' % match['profile']['email']
            print '    Presence:      %s' % match['presence']
            print ''


if __name__ == '__main__':
    slack = FindSlacker()
    slack.find_member()
