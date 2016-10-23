#!/usr/bin/python
# -*- coding: utf-8 -*-
from lib.scans_controller import ScansController
from lib.servers_controller import ServersController
from lib.options import Options
import lib.file_controller as File
import os
from dateutil.parser import parse


class ArchiveScans(object):
    def __init__(self):
        self.scans = ScansController()
        self.servers = ServersController()
        self.opts = Options().params()
        self.path = os.path.join(os.path.dirname(__file__), 'details/')

    def servers_write(self, path, server):
        server_path = path + "%s_%s/" % (server['hostname'], server['id'])
        File.write_dir(server_path)
        return server_path

    def scans_write(self, path, scan):
        scan_path = path + "%s_%s_%s_details.txt" % (scan['module'],
                                                     scan['id'],
                                                     self.iso8601(scan['created_at']))
        File.write_file(scan_path, str(scan))

    def iso8601(self, date):
        return parse(date).strftime("%Y-%m-%d")

    def archive(self):
        servers_index = self.servers.index()
        for server in servers_index['servers']:
            server_path = self.servers_write(self.path, server)
            kwargs = {
                'server_id': server['id'],
                'since': self.opts['since'],
                'until': self.opts['until']
            }

            scans_index = self.scans.index(**kwargs)
            for scan in scans_index:
                data = self.scans.show(scan['id'])['scan']
                self.scans_write(server_path, data)
                print "wrote %s_%s" % (data['id'], data['module'])


if __name__ == "__main__":
    ArchiveScans().archive()
