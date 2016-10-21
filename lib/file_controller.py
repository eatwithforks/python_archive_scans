#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

def write_file(path, data):
    with open(path, 'a') as output_file:
        output_file.write(data)

def write_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)