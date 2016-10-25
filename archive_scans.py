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
        self.queues = {
            'files': Queue(maxsize=0),
            'scans': Queue(maxsize=0)
        }

    def servers_path(self, path, server):
        return path + "%s_%s/" % (server['hostname'], server['id'])

    def scans_path(self, path, scan):
        return path + "%s_%s_%s_details.txt" % (scan['module'],
                                                scan['id'],
                                                self.iso8601(scan['created_at']))

    def iso8601(self, date):
        return parse(date).strftime("%Y-%m-%d")

    def setup_queue(self, do_work, queue):
        for i in range(self.threads):
            worker = Thread(target=do_work, args=(queue,))
            worker.setDaemon(True)
            worker.start()

    def files_consumer(self, q):
        while True:
            scan_data = self.queues['files'].get()
            File.write_file(scan_data['path'], str(scan_data['data']))
            print "%s_%s" % (scan_data['data']['id'], scan_data['data']['module'])
            self.queues['files'].task_done()

    def scans_consumer(self, q):
        while True:
            scan_data = self.queues['scans'].get()
            scan_details = self.scans.show(scan_data['scan']['id'])['scan']
            self.queues['files'].put({'path': scan_data['path'], 'data': scan_details})
            self.queues['scans'].task_done()

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

            self.setup_queue(self.files_consumer, self.queues['files'])
            self.setup_queue(self.scans_consumer, self.queues['scans'])

            scans_index = self.scans.index(**kwargs)
            for scan in scans_index:
                scan_path = self.scans_path(server_path, scan)
                if not os.path.isfile(scan_path):
                    self.queues['scans'].put({'path': scan_path, 'scan': scan})


if __name__ == "__main__":
    ArchiveScans().producer()
