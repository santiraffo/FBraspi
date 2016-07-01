#!/usr/bin/env python3

import time
import argparse         # allows us to pass in some parameters through command line
import logging		# More convenient logging, easier for debug and the like. import in any file you want to log from
import os
import json
from ubidots import ApiClient
from serial.serialutil import SerialException
from pprint import pprint

import sys
if sys.version_info < (3, 3, 0):
    from requests import ConnectionError

# To make pycharm and everyone happy, should refer to modules through package
from services.arduino.communication import Groduino     # Use Groduino instance for all serial comm.
from services.configuration import SerialParameters
from services.server import Server
from services.bot import Bot


def commandLineInit():
    """argparse stuff, sets program description and command line args. returns dict of arguments
    :return: dict with all command line args
    """

    # argparse provides cmd line description, --help, and args. try grodaemon.py --help
    program_description = "groterm: terminal to control/test grobot \n"
    program_epilog = ("Note: If multiple logging flags are set, highest one will be chosen.\n"
                      "Default log level is logging.WARNING. --info is nice too."
                      )
    parser = argparse.ArgumentParser(description=program_description,
                                     epilog=program_epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    # Flags
    parser.add_argument('-p', '--port', help='serial port to connect to, default /dev/ttyACM0', default='/dev/ttyACM0')
    parser.add_argument('-s', '--server', help='Url of server to connect to. Should have trailing slash', default=None)

    parser.add_argument('-v', '--verbose', action='store_true', help='Print verbose output')   # default False
    parser.add_argument('-i', '--info', action='store_true', help="Output info messages to show what's going on")
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet output, only errors and critical')
    parser.add_argument('-qq', '--qquiet', action='store_true', help='Really quiet output, only critical')

    args = parser.parse_args()
    args_dict = vars(args)	    # convert all args to a dict for convenience. use ex. args_dict['verbose']

    # Get correct log level
    if args_dict['verbose']:
        log_level = logging.DEBUG
    elif args_dict['info']:
        log_level = logging.INFO
    elif args_dict['quiet']:
        log_level = logging.ERROR
    elif args_dict['qquiet']:
        log_level = logging.CRITICAL
    else:
        log_level = logging.WARNING

    # Set up loggers
    logging_format = logging.Formatter('%(asctime)s :: %(name)-12s :: %(levelname)-8s :: %(message)s')

    logging_file = 'grodaemon.log'
    logging.basicConfig(level=logging.DEBUG,        # file logger should always be very verbose.
                        datefmt='%y-%m-%d %H:%M',
                        filename=logging_file,
                        filemode='w')
    logging.getLogger('').handlers[0].setFormatter(logging_format)   # we want to have the same format for both outputs

    console_logger = logging.StreamHandler()
    console_logger.setFormatter(logging_format)
    console_logger.setLevel(level=log_level)
    logging.getLogger('').addHandler(console_logger)

    logging.info('Starting grodaemon!')
    logging.debug('Logging to %s', os.path.join(os.getcwd(), logging_file))

    logging.getLogger('requests').setLevel(logging.WARNING)

    logging.debug('Input parameters:')
    for arg in args_dict:
        logging.debug('\t'+str(arg) + '\t' + str(args_dict[arg]))

    return args_dict


def hwInit(port, serial_parameters: SerialParameters) -> Groduino:
    """Initialize hw, return Groduino instance. NOTE: this will keep retrying until connection is established!
    :return: Groduino instance. handshaken, stirred, and ready to drink!

    """

    # Initialization Code (INIT)
    while 1:
        try:
            return Groduino(port=port, serial_parameters=serial_parameters)
        except (ConnectionError, SerialException):
            logging.exception('Failed to init Groduino, retrying in 3 seconds')
        time.sleep(3)

message_count = 0

# Main Code
if __name__ == "__main__":
	
	cmdargs_dict = commandLineInit()
	
	serial_params = SerialParameters()
	groduino = hwInit(port=cmdargs_dict['port'], serial_parameters=serial_params)
	# TODO just init the server inside bot. Bot should take ip of server to connect to
	
	api = ApiClient(token='RBgwxE0fSTaFS7IH7EqIya2Nl6yVek') #TODO leer desde txt
	
	#Create a "Variable" object

	datas= api.get_datasources ()      

        dic={datas[0].name:datas[0],datas[1].name:datas[1],datas[2].name:datas[2]} # learning not to use Switchs fking Py...

        ctrlActFloraBox=dic['Ctrl Actuators floraBox']
        ctrlVarFloraBox=dic['Ctrl floraBox']
        varFloraBox=dic['Variables floraBox']
        
	while 1:
		message = groduino.receive(blocking=True)
		if not message:
			print ("No message")
		logging.debug('Handling: %s',message)
	
		try:
			message_dict =json.loads(message)
		except ValueError:
			logging.error('Unable to parse message, json.loads failed')
			logging.debug('',exc_info=True)
		
		message_count += 1
		variablesFB=varFloraBox.get_variables()
		data=[]
		for x in range(0,len(variablesFB)):
                    data.insert(0,{'variable':variablesFB[x].id,'value':message_dict[variablesFB[x].description]})
                api.save_collection(data)

		time.sleep(30)



#{"AACR 1":1,"AAHE 1":2,"AAHU 1":3,"AAVE 1":4,"ALMI 1":5,"ALPN 1":6,"ALPN 2":7,"GEND":8,"GTYP":9,"SACO 1":10,"SAHU 1":11,"SAHU 2":12,"SATM 1":13,"SATM 2":14,"SGSO 1":15,"SGWO 1":16,"SLIN 1":18,"SLPA 1":17,"SWEC 1":19,"SWPH 1":20,"SWTM 1":21}
