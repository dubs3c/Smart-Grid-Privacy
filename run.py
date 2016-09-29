#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""╔═╗┌┬┐┌─┐┬─┐┌┬┐  ╔╦╗┌─┐┌┬┐┌─┐┬─┐  ╔═╗┬─┐┬┬  ┬┌─┐┌─┐┬ ┬
╚═╗│││├─┤├┬┘ │   ║║║├┤  │ ├┤ ├┬┘  ╠═╝├┬┘│└┐┌┘├─┤│  └┬┘
╚═╝┴ ┴┴ ┴┴└─ ┴   ╩ ╩└─┘ ┴ └─┘┴└─  ╩  ┴└─┴ └┘ ┴ ┴└─┘ ┴ 

By Dubell & Widegren

Usage:
  run.py --mode=client|server [-v] [-vv]
Options:
  -h, --help            	Show this screen.
  --version             	Show version.
  mode (client|server)  	Initiate server or client mode.
  -v, --verbose         	Show information regarding setup.
  -vv, --very-verbose   	Display everything.
"""
from docopt import docopt
from src.server import Server
from src.client import Client
from src.core import Core


def main(arguments):
	core = Core()

	if arguments['--mode'] == 'client':
		client = Client()
		client.setup()
		client.start()
	elif arguments['--mode'] == 'server':
		server = Server()
		server.setup()
	else:
		core.logger.error("You need to specify either server or client mode!")


if __name__ == '__main__':
	arguments = docopt(__doc__, version="Smart Meter Privacy 1.0")
	main(arguments)
