#!/usr/bin/python

import logging

#logging configuration
LOG_FNAME = 'engine.log'
logging.basicConfig(format='[%(asctime)s] %(levelname)s:\t%(message)s', filename=LOG_FNAME, level=logging.DEBUG)



#game stages
LOBBY 		= 0	#collecting players, modifying options
OPENING 	= 1	#game has started, positioning armies
PLAYING		= 2	#game is being played, it's someone's turn
FINISHED	= 3	#game is over, winner was determined

class Game:
	def __init__(self):
		logging.info('creating new game')
		self.stage = LOBBY
		self.players = []
		self.log = []
		self.winner = None

	def start_game(self):
		if (self.stage != LOBBY):
			logging.error("trying to start an already started game. No action will be performed.")
		else:
			#start game		

	def adjudicate(self,winner):
		if not (winner in self.players):
			logging.error("trying to adjudicate match to player not playing in this game! No action will be performed")
		else:
			self.winner = winner
		

logging.info("starting oor engine...")

testgame = Game()

testgame.start_game()
