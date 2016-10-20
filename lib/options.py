#!/usr/bin/python
# -*- coding: utf-8 -*-
"""options"""
import argparse


parser = argparse.ArgumentParser(description='Archive Scans')
parser.add_argument('--auth', help='Read auth info from <file>', required=True)
parser.add_argument('--since', help='Only get historical scans after <when> (ISO-8601 format)', required=False)
parser.add_argument('--until', help='Only get historical scans till <when> (ISO-8601 format)', required=False)

class Options(object):
    def __init__(self):
        self.known_params = ['since', 'until']
        self.args = vars(parser.parse_args())

    def clean_params(self):
        """
            Remove arguments with None
        """
        self.args = {k: v for k, v in self.args.items() if v}
        return self.args

    def inject_scan_params(self):
        self.args['scan_options'] = []

        for k, v in self.args.iteritems():
            if k in self.known_params:
                self.args['scan_options'].append({k: v})

        for element in self.args['scan_options']:
            for key in element.keys():
                del self.args[key]

        return self.args

    def params(self):
        self.clean_params()
        return self.inject_scan_params()
