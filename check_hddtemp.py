#!/usr/bin/env python

# -*- coding: utf-8 -*-

# check_hddtemp
# check_hddtemp.py

# Copyright (c) 2011-2012 Alexei Andrushievich <vint21h@vint21h.pp.ua>
# Check HDD temperature Nagios plugin [https://github.com/vint21h/check_hddtemp]
#
# This file is part of check_hddtemp.
#
# check_hddtemp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys

try:
    from optparse import OptionParser
    import socket
except ImportError, err:
    print "ERROR: Couldn't load module. %s" % (err)
    sys.exit(-1)

# metadata
__author__ = "Alexei Andrushievich"
__email__ = "vint21h@vint21h.pp.ua"
__licence__ = "GPLv3 or later"
__description__ = "Check HDD temperature Nagios plugin"
__url__ = "https://github.com/vint21h/check_hddtemp"
VERSION = (0, 2, 0)
__version__ = '.'.join(map(str, VERSION))


def parse_cmd_line():
    """
    Commandline options arguments parsing.
    """

    version = "%%prog %s" % (__version__)
    parser = OptionParser(version=version)
    parser.add_option("-s", "--server", action="store", dest="server",
                                            type="string",
                                            default="", metavar="SERVER",
                                            help="server address")
    parser.add_option("-p", "--port", action="store", type="int", dest="port",
                                            default="7634", metavar="PORT",
                                            help="port number")
    parser.add_option("-d", "--device", action="store", dest="device",
                                            type="string", default="",
                                            metavar="DEVICE", help="device name")
    parser.add_option("-S", "--separator", action="store", type="string",
                                            dest="separator", default="|",
                                            metavar="SAPARATOR",
                                            help="hddtemp separator")
    parser.add_option("-w", "--warning", action="store", type="int",
                            dest="warning", default="40", metavar="TEMP",
                                            help="warning temperature")
    parser.add_option("-c", "--critical", action="store", type="int",
                            dest="critical", default="65", metavar="TEMP",
                                            help="critical temperature")
    parser.add_option("-q", "--quiet", metavar="QUIET", action="store_false",
                                        default=False, dest="quiet",
                                        help="be quiet")

    options = parser.parse_args(sys.argv)[0]

    # check mandatory command line options supplied
    mandatories = ["server", "device", ]
    if not all(options.__dict__[mandatory] for mandatory in mandatories):
        print "Mandatory command line option missing."
        exit(0)

    return options


def get_hddtemp_data(server, port):
    """
    Get and return data from hddtemp server response.
    """

    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        _socket.connect((server, port))
    except socket.error:
        print "ERROR: Server communicating problem."
        socket_.close()
        sys.exit(-1)

    response = _socket.recv(4096)
    _socket.close()

    return response


def parse_response(response, device, separator):
    """
    Search for device and get HDD info from server response.
    """

    hdd_info_keys = ['hdd_model', 'temperature', 'scale', ]
    dev_info = {}

    for dev in response.split(separator*2):
        dev =  dev.strip(separator).split(separator)
        if len(dev) != 4:
            print "ERROR: Server response parsing error."
            sys.exit(-1)
        dev_info.update({dev[0]: dict(zip(hdd_info_keys, dev[1:]))})

    if device not in dev_info.keys():
        print "ERROR: Info about requested device not founded in server response."
        sys.exit(0)

    return dev_info[device]


def check_hddtemp(response, options):
    """
    Return info about HDD statuses to Nagios.
    """

    output_templates = {
        'critical': "CRITICAL: device temperature (%(temperature)s%(scale)s) exceeds critical temperature threshold (%(critical)d%(scale)s)",
        'warning': "WARNING: device temperature (%(temperature)s%(scale)s) exceeds warning temperature threshold (%(warning)d%(scale)s)",
        'ok': "OK: device is functional and stable (%(temperature)s%(scale)s)",
    }

    if int(response["temperature"]) > options.critical:
        data = {
            'temperature': response["temperature"],
            'critical': options.critical,
            'scale': response["scale"],
        }
        print output_templates['critical'] % data
    elif int(response["temperature"]) > options.warning and int(response["temperature"]) < options.critical:
        data = {
            'temperature': response["temperature"],
            'warning': options.warning,
            'scale': response["scale"],
        }
        print output_templates['warning'] % data
    else:
        data = {
            'temperature': response["temperature"],
            'scale': response["scale"],
        }
        print output_templates['ok'] % data


if __name__ == "__main__":
    options = parse_cmd_line()
    check_hddtemp(parse_response(get_hddtemp_data(options.server, options.port), options.device, options.separator), options)