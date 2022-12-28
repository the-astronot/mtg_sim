"""
	Copyright (C) 2022  Max Marshall   

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see https://www.gnu.org/licenses/.
________________
|_File_History_|________________________________________________________________
|_Programmer______|_Date_______|_Comments_______________________________________
| Max Marshall    | 2022-12-18 | Created File
| Max Marshall    | 2022-12-22 | Basic Interpreter Integration
|
|
"""
from utils import yes
from Player import Player
from Card import Card, ExampleCard, ExampleLand
from SkulkInterpreter import SkulkInterpreter, CMND_STRUCT
import random


class Arena:
	def __init__(self, players):
		self.players = players
		self.interpreter = SkulkInterpreter(self)
		self.ready = False
		self.debug = True

	def print(self, string):
		if self.debug:
			print(string)

	def get_active_cards(self,target_player):
		cards = []
		locations = ["hand","mat","graveyard","exile"]
		if target_player is not None:
			for loc in locations:
					for card in target_player.locations[loc].cards:
						cards.append(card)
		else:
			for player in self.players:
				for loc in locations:
					for card in player.locations[loc].cards:
						cards.append(card)
		self.print("NUM_CARDS: {}".format(len(cards)))
		return cards

	def pre_game(self, health=20, min_deck=60):
		for player in self.players:
			player.setHealth(health)
			if player.deck.size() < min_deck:
				print("Error: {} playing with too small a deck.".format(player.name))
				cont = input("Continue? (Y/n): ")
				if not yes(cont):
					print("Declined, Returning.")
					return
				print("Approved.")
			player.setup()
		self.set_order()
		self.print("Order: {}".format(self.ordered))
		self.winner = None
		self.ready = True

	def set_order(self):
		scores = {}
		for player in self.players:
			score = random.randint(1,100000)
			scores[player]=score
		self.ordered = []
		for player in self.players:
			added = False
			for i in range(len(self.ordered)):
				if scores[player] > scores[self.ordered[i]]:
					self.ordered.insert(i,player)
					added = True
					break
			if not added:
				self.ordered.append(player)
			
	def play_game(self):
		if not self.ready:
			print("Error: Attempted to begin play without setting up game.\nRun pre_game first and try again.")
			return
		self.round = 1
		while self.winner is None:
			self.print("BEGINNING ROUND {:02d}".format(self.round))
			for player in self.ordered:
				self.play_turn(player)
				self.check_winner()
				if self.winner is not None:
					break
			self.round += 1

	def play_turn(self, player):
		self.interpreter.add_call(CMND_STRUCT("update",None,None))
		self.interpreter.add_call(CMND_STRUCT("round_begin",None,player))
		# Begin untap step
		self.interpreter.add_call(CMND_STRUCT("untap",None,player))
		# Draw Card
		self.interpreter.add_call(CMND_STRUCT("update",None,None))
		self.interpreter.add_call(CMND_STRUCT("draw",player,player))
		# MAIN PHASE 1
		self.interpreter.add_call(CMND_STRUCT("update",None,None))
		self.main_phase(player)
		# COMBAT PHASE
		self.interpreter.add_call(CMND_STRUCT("update",None,None))
		self.combat_phase(player)
		# MAIN PHASE 2
		self.interpreter.add_call(CMND_STRUCT("update",None,None))
		self.main_phase(player)
		# END PHASE
		self.interpreter.add_call(CMND_STRUCT("update",None,None))
		self.interpreter.add_call(CMND_STRUCT("round_end",None,player))
		self.interpreter.add_call(CMND_STRUCT("update",None,None))
		return

	def main_phase(self, player):
		self.print("ENTERING MAIN PHASE")
		action = 0
		while action is not None:
			targets = [player.hand,player.mat,player.graveyard]
			possible_actions = []
			for target in targets:
				for card in target.cards:
					actions = card.getPlayable()
					for action in actions:
						possible_actions.append(CMND_STRUCT(action,card,player))
				cmnd = player.choice(possible_actions)
			if cmnd is not None:
				self.interpreter.add_call(cmnd)
		
	def combat_phase(self, player):
		potential_attackers = []
		potential_targets = []
		for card in player.mat:
			if card.can_attack():
				potential_attackers.append(card)
		for other_player in self.players:
			if other_player is not player:
				for card in player.mat:
					if card.can_be_attacked:
						potential_targets.append(card)
		attackers = player.select_attackers(potential_attackers)
		defenders = {}
		for attacker in attackers:
			if attacker.target in defenders:
				defenders[attacker.target].append()

	def check_winner(self):
		still_alive = []
		for player in self.players:
			if player.isAlive():
				still_alive.append(player)
		if len(still_alive) == 1:
			self.winner = still_alive[0]
		elif len(still_alive) == 0:
			self.winner = self.players


if __name__ == '__main__':
	cards = [ExampleCard() for _ in range(36)] + [ExampleLand() for _ in range(24)]
	p1 = Player("Max",cards,"../data/player.sklk")
	p2 = Player("Garrett")
	p3 = Player("Emilie")
	p4 = Player("Austin")
	arena = Arena([p1])
	#print(p1.deck)
	arena.pre_game()
	print(p1.hand)
	print(arena.players)
	arena.play_game()
