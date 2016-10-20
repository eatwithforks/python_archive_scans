#!/usr/bin/python
# -*- coding: utf-8 -*-
from lib.options import Options

class QueryController(object):
    def __init__(self):
        self.args = Options().params()

    def query(self):
        str = ""
        for item in self.args['scan_options']:
            for k, v in item.iteritems():
                str += "%s=%s&" % (k, v)
        return str
