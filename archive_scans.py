#!/usr/bin/python
# -*- coding: utf-8 -*-
from lib.scans_controller import ScansController
from lib.servers_controller import ServersController
from lib.options import Options
import lib.file_controller as File
import os

def main():
    scans = ScansController()
    servers = ServersController()
    opts = Options().params()
    path = os.path.join(os.path.dirname(__file__), 'details/')

    servers_index = servers.index()
    for server in servers_index['servers']:
        server_path = path + "%s_%s/" % (server['hostname'], server['id'])
        File.write_dir(server_path)

        kwargs = {'server_id': server['id'], 'since': opts['since'], 'until':opts['until']}
        scans_index = scans.index(**kwargs)
        for scan in scans_index:
            data = scans.show(scan['id'])['scan']
            scan_path = server_path + "%s_%s_%s_details.txt" % (data['module'], data['id'], data['created_at'])
            File.write_file(scan_path, str(data))
            print "wrote %s_%s" % (data['id'], data['module'])

if __name__ == "__main__":
    main()
