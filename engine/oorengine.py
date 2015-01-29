#!/usr/bin/python

import logging

#game stages
LOBBY 		= 0	#collecting players, modifying options
OPENING 	= 1	#game has started, positioning armies
PLAYING		= 2	#game is being played, it's someone's turn
FINISHED	= 3	#game is over, winner was determined

class Game:
	def __init__(self):
		self.stage = LOBBY
		self.players = []
		self.log = []

	def start_game(self):
		if (self.stage != LOBBY):
			print "trying to start an already started game. No action will be performed."
	

print "starting oor engine..."


