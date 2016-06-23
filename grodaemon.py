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
	
	api = ApiClient(token='RBgwxE0fSTaFS7IH7EqIya2Nl6yVek')
	
	#Create a "Variable" object
	
	temperatureID 	= "5769a9917625424ca5ed3f29"
	humidityID 	= "5769b8da7625425365cb2d73"
	floraBoxID	= "5769a92d762542486fedcaa9"
	
	floraBox= api.get_datasource (floraBoxID)

#	AACRa=floraBox.create_variable({"name":"AACR 1","unit":""})
#	AAHEa=floraBox.create_variable({"name":"AAHE 1","unit":""})
#	AAHUa=floraBox.create_variable({"name":"AAHU 1","unit":""}) 
#	AAVEa=floraBox.create_variable({"name":"AAVE 1","unit":""}) 
#	ALMIa=floraBox.create_variable({"name":"ALMI 1","unit":""}) 
#	ALPNa=floraBox.create_variable({"name":"ALPN 1","unit":""})
#	ALPNb=floraBox.create_variable({"name":"ALPN 2","unit":""}) 
#	GEND =floraBox.create_variable({"name":"GEND","unit":""})
#	GTYP =floraBox.create_variable({"name":"GTYP","unit":""}) 
#	SACOa=floraBox.create_variable({"name":"SACO 1","unit":""})
#	SAHUa=floraBox.create_variable({"name":"SAHU 1","unit":""})
#	SAHUb=floraBox.create_variable({"name":"SAHU 2","unit":""})
#	SATMa=floraBox.create_variable({"name":"SATM 1","unit":""})
#	SATMb=floraBox.create_variable({"name":"SATM 2","unit":""})
#	SGSOa=floraBox.create_variable({"name":"SGSO 1","unit":""})
#	SGWOa=floraBox.create_variable({"name":"SGWO 1","unit":""})
#	SLINa=floraBox.create_variable({"name":"SLIN 1","unit":""})
#	SLPAa=floraBox.create_variable({"name":"SLPA 1","unit":""})
#	SWECa=floraBox.create_variable({"name":"SWEC 1","unit":""})
#	SWPHa=floraBox.create_variable({"name":"SWPH 1","unit":""})
#	SWTMa=floraBox.create_variable({"name":"SWTM 1","unit":""})


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
		variablesFB=floraBox.get_variables()

		variablesFB[0].save_value({"value":message_dict["AACR 1"]})
		variablesFB[1].save_value({"value":message_dict["AAHE 1"]})
		variablesFB[2].save_value({"value":message_dict["AAHU 1"]})
		variablesFB[3].save_value({"value":message_dict["AAVE 1"]})
		variablesFB[4].save_value({"value":message_dict["ALMI 1"]})
		variablesFB[5].save_value({"value":message_dict["ALPN 1"]})
		variablesFB[6].save_value({"value":message_dict["ALPN 2"]})
		#variablesFB[7].save_value({"value":message_dict["GEND"]}) 
		#variablesFB[8].save_value({"value":message_dict["GTYP"]}) 
		variablesFB[9].save_value({"value":message_dict["SACO 1"]})
		variablesFB[10].save_value({"value":message_dict["SAHU 1"]})
		variablesFB[11].save_value({"value":message_dict["SAHU 2"]})
		variablesFB[12].save_value({"value":message_dict["SATM 1"]})
		variablesFB[13].save_value({"value":message_dict["SATM 2"]})
		variablesFB[14].save_value({"value":message_dict["SGSO 1"]})
		variablesFB[15].save_value({"value":message_dict["SGWO 1"]})
		variablesFB[16].save_value({"value":message_dict["SLIN 1"]})
		variablesFB[17].save_value({"value":message_dict["SLPA 1"]})
		variablesFB[18].save_value({"value":message_dict["SWEC 1"]})
		variablesFB[19].save_value({"value":message_dict["SWPH 1"]})
		variablesFB[20].save_value({"value":message_dict["SWTM 1"]})

		print ("message:")
		print ("",message)
		print ("JSON")
		print ("",message_dict)
		pprint(message_dict)
		print(message_dict["AACR 1"])
		time.sleep(30)

#    server = Server(cmdargs_dict['server'])
#    bot = Bot(groduino, server)

#    bot.run()


