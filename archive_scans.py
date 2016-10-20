#!/usr/bin/python
# -*- coding: utf-8 -*-
from lib.scans_controller import ScansController
from lib.query_controller import QueryController

def main():
    scans = ScansController()
    scans_index =  scans.index(QueryController().query())
    print scans_index

if __name__ == "__main__":
    main()
