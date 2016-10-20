#!/usr/bin/python
# -*- coding: utf-8 -*-
import cloudpassage
import lib.loadyaml as loadyaml

class ScansController(object):
    def __init__(self):
        self.configs = loadyaml.load_portal()

    def create_halo_session_object(self):
        """create halo session object"""

        session = cloudpassage.HaloSession(self.configs['key_id'], self.configs['secret_key'])
        return session

    def index(self, options = None):
        """HTTP Index scans from Halo"""
        session = self.create_halo_session_object()
        api = cloudpassage.HttpHelper(session)
        url = "/v1/scans?%s" % options
        return api.get(url)