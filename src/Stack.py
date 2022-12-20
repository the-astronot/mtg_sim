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
|
|
|
"""
from Card import Card
import random

class Stack:

	def __init__(self, cards=None):
		self.cards = cards
		

class Deck(Stack):

	def __init__(self):
		self.debug = False
		self.ordered = []
		self.cards = []
		self.nonlands = []
		self.lands = []
		for _ in range(24): # This is just for a test of the shuffling system
			self.lands.append("L")
		for _ in range(36):
			self.nonlands.append("NL")
		self.cards = self.lands + self.nonlands
		
	def prepare(self):
		# Mana-Sets the Deck as best it can
		self.ordered = []
		ratio = len(self.nonlands)/float(len(self.lands))
		lands = self.lands.copy()
		nonlands = self.nonlands.copy()
		i = 0
		cnt = ratio
		while len(lands) > 0 or len(nonlands) > 0:
			if i > cnt:
				cnt += ratio
				if len(lands) > 0:
					card = random.choice(lands)
					idx = lands.index(card)
					lands.pop(idx)
					self.ordered.append(card)
			else:
				if len(nonlands) > 0:
					card = random.choice(nonlands)
					idx = nonlands.index(card)
					nonlands.pop(idx)
					self.ordered.append(card)
				i+=1

	def shuffle(self):
		# Performs a faux-Magic Shuffle
		temp = self.ordered.copy()
		block_size = int(len(temp)/6.0)
		self.ordered = []
		self.ordered = temp[:block_size]
		temp = temp[block_size:]
		while len(temp) > 0:
			num_cards_to_add = random.randint(int(block_size*0.75),int(block_size*1.5))
			num_cards_to_add = min(len(temp),num_cards_to_add)
			loc = random.choice([0,1])
			if loc == 0:
				self.ordered = temp[:num_cards_to_add] + self.ordered
				temp = temp[num_cards_to_add:]
			else:
				self.ordered = self.ordered + temp[:num_cards_to_add]
				temp = temp[num_cards_to_add:]
		self.print(self.ordered)

	def print(self, string):
		# Handy debugging
		if self.debug:
			print(string)

	def size(self):
		# Total size of the deck
		return len(self.ordered)



if __name__ == '__main__':
	test = Deck()
