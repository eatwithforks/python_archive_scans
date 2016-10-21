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

    def params(self):
        """
            Remove arguments with None
        """
        return self.args

