#!/usr/bin/python
# -*- coding: utf-8 -*-
from lib.scans_controller import ScansController
from lib.servers_controller import ServersController
from lib.options import Options
import lib.file_controller as File
import os
from dateutil.parser import parse
from Queue import Queue
from threading import Thread


class ArchiveScans(object):
    def __init__(self):
        self.scans = ScansController()
        self.servers = ServersController()
        self.opts = Options().params()
        self.path = os.path.join(os.path.dirname(__file__), 'details/')
        self.threads = 5
        self.q = Queue(maxsize=0)

    def servers_path(self, path, server):
        return path + "%s_%s/" % (server['hostname'], server['id'])

    def scans_path(self, path, scan):
        return path + "%s_%s_%s_details.txt" % (scan['module'],
                                                scan['id'],
                                                self.iso8601(scan['created_at']))

    def iso8601(self, date):
        return parse(date).strftime("%Y-%m-%d")

    def setup_queue(self):
        for i in range(self.threads):
            worker = Thread(target=self.consumer, args=(self.q,))
            worker.setDaemon(True)
            worker.start()

    def consumer(self, q):
        while True:
            qdata = self.q.get()
            File.write_file(qdata['path'], str(qdata['data']))
            print "%s_%s" % (qdata['data']['id'], qdata['data']['module'])
            self.q.task_done()

    def producer(self):
        servers_index = self.servers.index()
        for server in servers_index['servers']:
            server_path = self.servers_path(self.path, server)
            File.write_dir(server_path)

            kwargs = {
                'server_id': server['id'],
                'since': self.opts['since'],
                'until': self.opts['until']
            }

            scans_index = self.scans.index(**kwargs)
            self.setup_queue()
            for scan in scans_index:
                scan_path = self.scans_path(server_path, scan)
                if not os.path.isfile(scan_path):
                    data = self.scans.show(scan['id'])['scan']
                    self.q.put({'path': scan_path, 'data': data})


if __name__ == "__main__":
    ArchiveScans().producer()
