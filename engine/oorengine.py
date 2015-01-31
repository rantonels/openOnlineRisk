#!/usr/bin/python

import logging
import random
import os,sys
import time

#change directory to script directory
os.chdir(os.path.dirname(sys.argv[0]))

#logging configuration
LOG_FNAME = 'engine.log'
logFormat='[%(asctime)s] %(levelname)s:\t%(message)s'
logFormatSh='%(levelname)s:\t%(message)s'

logger = logging.getLogger('oorengine')
logger.setLevel(logging.DEBUG)

logfh = logging.FileHandler(LOG_FNAME)
logfh.setLevel(logging.DEBUG)

logch = logging.StreamHandler()
logch.setLevel(logging.DEBUG)

logfmt 		= logging.Formatter(logFormat)
logfmtsh 	= logging.Formatter(logFormatSh)


logfh.setFormatter(logfmt)
logch.setFormatter(logfmtsh)

logger.addHandler(logfh)
logger.addHandler(logch)


#CONSTANTS
GAMES_DIR 	= '../games/'	#folder to contain game data
DELAY 		= 0.050		#msecs between pipe reads

#utilities

def ensure_dir(f):
    d = f
    if not os.path.exists(d):
        os.makedirs(d)
    else:
	logger.warning("directory %s already exists."%d)

#animal names :D

try:
	f = open('../animals.txt','r')
except IOError:
	logging.error('no animals.txt found. This is very, very serious.')
	exit()
ANAMES = [l.strip() for l in f.readlines()]
f.close()

#game stages
LOBBY 		= 0	#collecting players, modifying options
OPENING 	= 1	#game has started, positioning armies
PLAYING		= 2	#game is being played, it's someone's turn
FINISHED	= 3	#game is over, winner was determined

#preparing pipe

logger.debug("preparing pipe...")

FIFO_PATH = '/tmp/oorengine_pipe'

if os.path.exists(FIFO_PATH):
	logger.warning("pipe object was not closed correctly.")
	os.unlink(FIFO_PATH)

if not os.path.exists(FIFO_PATH):
	os.mkfifo(FIFO_PATH)
	




class Game:
	def __init__(self,gid=None):
		logger.info('creating new game')
		self.stage = LOBBY
		self.players = []
		self.log = []
		self.winner = None

		if (gid==None):
			self.gid = random.getrandbits(32)
		else:
			self.gid = gid
	
		#check for folder
		ensure_dir(GAMES_DIR+"%8x"%(self.gid))

		#generate match name
		self.name = ANAMES[self.gid%len(ANAMES)]+" "+ANAMES[(self.gid>>16)%len(ANAMES)]

		logger.info('new game "%s" created (%8x)'%(self.name,self.gid))

	def start_game(self):
		if (self.stage != LOBBY):
			logger.error("trying to start an already started game. No action will be performed.")
		else:
			#start game
			pass	

	def adjudicate(self,winner):
		if not (winner in self.players):
			logger.error("trying to adjudicate match to player not playing in this game! No action will be performed")
		else:
			self.winner = winner
		

logger.info("starting oor engine main loop...")

while True:
	try:
		time.sleep(DELAY)
		sys.stdout.flush()
	
		#reopen pipe
		pipein = open(FIFO_PATH, 'r')

		#read line from pipe
		nlines = pipein.read().split('\n')

		#cleanup
		nlines = map(str.strip,nlines)	#strip whitespace
		nlines = filter(None,nlines)	#remove empty lines

		pipein.close()

		if len(nlines) == 0:
			continue

		for line in nlines:
			logger.info("MESSAGE RECEIVED: "+line)
	except KeyboardInterrupt:
		logger.info("got KeyboardInterrupt, logging off...")
		#destroy pipe
		os.unlink(FIFO_PATH)
		break

logger.info("shutting down.")
