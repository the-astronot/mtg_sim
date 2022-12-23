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
| Max Marshall    | 2022-12-21 | Modified to match changes to Counters Class
|
|
"""
from Stack import Stack, Deck
from Counters import Player_Counters
from Card import Card, ExampleCard, ExampleLand
from utils import process_skulk

class Player:

	def __init__(self, name, cards=[], skulk_file=None):
		self.name = name
		self.hand = Stack()
		self.mat = Stack()
		self.counters = Player_Counters()
		self.deck = Deck(cards)
		self.graveyard = Stack()
		self.exile = Stack()
		self.locations = {"hand":self.hand,"mat":self.mat,"deck":self.deck,"graveyard":self.graveyard,"exile":self.exile}
		self.skulk = {}
		self.skulk_intercepts = {}
		if skulk_file is not None:
			self.read_skulk(skulk_file)
		self.debug = False

	def print(self, string):
		if self.debug:
			print("{}".format(string))

	def read_skulk(self, filename):
		with open(filename,"r") as f:
			text = f.read()
			self.skulk = process_skulk(text)


	def draw_card(self):
		self.hand.cards.append(self.deck.draw())

	def getHealth(self):
		return self.get("health")

	def setHealth(self, value):
		self.sett("health",value)

	def get(self,name):
		v, minim, maxim = self.counters.get(name)
		return v

	def sett(self,name,value):
		return self.counters.sett(name,value)

	def __repr__(self):
		return "{}:{:02d}".format(self.name,self.getHealth())

	def __str__(self):
		return "{}:{:02d}".format(self.name,self.getHealth())

	def setup(self):
		self.deck.prepare()
		for _ in range(5):
			self.deck.shuffle()
		for _ in range(7):
			self.draw_card()


class Human(Player):

	def __init__(self):
		super().__init__()


if __name__ == '__main__':
	cards = [ExampleLand() for _ in range(24)] + [ExampleCard() for _ in range(36)]
	test = Player("Max",cards,"../data/player.sklk")
	print(test.skulk)
