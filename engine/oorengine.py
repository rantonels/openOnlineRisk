#!/usr/bin/python

import logging
import random
import os,sys
import time

import re

import cPickle as pickle

#change directory to script directory
os.chdir(os.path.dirname(sys.argv[0]))

#LOGGING CONFIGURATION
LOG_FNAME = 'engine.log'
logFormat='[%(asctime)s] %(levelname)s:\t\t%(message)s'
logFormatSh='%(levelname)s\t%(message)s'

#main logger
logger = logging.getLogger('oorengine')
logger.setLevel(logging.DEBUG)

#logfile handler
logfh = logging.FileHandler(LOG_FNAME)
logfh.setLevel(logging.DEBUG)

#stream handler
logch = logging.StreamHandler()
logch.setLevel(logging.DEBUG)

#adding handlers -> main logger
logger.addHandler(logfh)
logger.addHandler(logch)

#format setup
logfmt 		= logging.Formatter(logFormat)
logfmtsh 	= logging.Formatter(logFormatSh)

logfh.setFormatter(logfmt)
logch.setFormatter(logfmtsh)


#LOADING PLAYER DB
logger.debug("loading player database...")
try:
	player_db = pickle.load(open('../database.dat','r'))
except IOError:
	logger.error("unable to open player database \"database.dat\".")
	exit()



#CONSTANTS
GAMES_DIR 	= '../games/'	#folder to contain game data
DELAY 		= 0.050		#msecs between pipe reads

MAX_GAMES	= 8		#maximum number of allowed games

#UTILITIES

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
	logger.error('no animals.txt found. This is very, very serious.')
	exit()
ANAMES = [l.strip() for l in f.readlines()]
f.close()



#LOADING MAP DATA

logger.info("loading map data...")

import ConfigParser
Config = ConfigParser.ConfigParser()

try:
	Config.read('../map.dat')
except IOError:
	logger.error('no map.dat found. How are we even supposed to play?')
	exit()

#load states list
map_states = Config.sections()

#check for duplicates in states
if (len(map_states)!=len(set(map_states))): #little trick from http://stackoverflow.com/a/1541827
	logger.error("duplicate states in map.dat.")
	exit()

#load connections
map_connections = {}

for s in map_states:
	if("nb" in Config.options(s)):
		raws = Config.get(s,"nb")
		conns = map(str.strip,raws.split(','))

		map_connections[s] = conns	

	else:
		logger.error('no "nb" option for state %s.'%s)
		exit()

#check for nonexisting states in connection

for s in map_states:
	for ss in map_connections[s]:
		if (not (ss in map_states)):
			logger.error('state "%s", declared as connected to %s, is not in main states list'%(ss,s))
			exit()
		if (not (s in map_connections[ss])):
			logger.error('conflicting (one-way) connection between states %s and %s'%(s,ss))
			exit()


#GAMES STAGES CONSTANTS

LOBBY 		= 0	#collecting players, modifying options
OPENING 	= 1	#game has started, positioning armies
PLAYING		= 2	#game is being played, it's someone's turn
FINISHED	= 3	#game is over, winner was determined

#PREPARING PIPE

logger.debug("preparing pipe...")

FIFO_PATH = '/tmp/oorengine_pipe'

if os.path.exists(FIFO_PATH):
	logger.warning("pipe object was not closed correctly.")
	os.unlink(FIFO_PATH)

if not os.path.exists(FIFO_PATH):
	os.mkfifo(FIFO_PATH)
	

#GAME CLASS


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
		elif (len(self.players)<2):
			logger.error("trying to start a game with less than two people. No action will be performed.")
		else:
			#start game
			self.stage = OPENING


	def adjudicate(self,winner):
		if not (winner in self.players):
			logger.error("trying to adjudicate match to player not playing in this game! No action will be performed")
		else:
			self.winner = winner
	
#setup gamelist	
games_list = []


#MESSAGE PARSING

mesparser = re.compile("(\w+):(\w+)@(\d+) (.*)")

def parse_message(message):
	pars = mesparser.match(message)
	if (pars == None):
		logger.warning("message does not match regular expression. Ignored.")	
		return
	
	m_uname 	= pars.group(1)
	m_passhash	= pars.group(2)
	m_game		= pars.group(3)
	m_commands	= map(str.strip,pars.group(4).split(" "))

	logger.debug("Player %s @ game %s requests: "%(m_uname,m_game)+ ",".join(m_commands))

	if ( not (m_uname in player_db)):
		logger.warning("Player %s does not exist. Ignoring request."%m_uname)
		return
	if (player_db[m_uname]["hpass"] != m_passhash):
		logger.warning("Password for player is incorrect. Ignoring request.")
		return
	




#MAIN LOOP

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
			parse_message(line)
	except KeyboardInterrupt:
		logger.info("got KeyboardInterrupt, logging off...")
		#destroy pipe
		os.unlink(FIFO_PATH)
		break

logger.info("shutting down.")
