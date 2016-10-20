#!/usr/bin/python
# -*- coding: utf-8 -*-

def write(path, data):
    with open(path, 'a') as output_file:
        output_file.write(data)