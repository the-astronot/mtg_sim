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
from Stack import Stack, Deck
from Counters import Player_Counters

class Player:

	def __init__(self, name):
		self.name = name
		self.hand = []
		self.counters = Player_Counters()
		self.health = self.counters.counters["health"].value
		self.deck = Deck()
		self.graveyard = Stack()
		self.exile = Stack()

	def __repr__(self):
		return "{}:{:02d}".format(self.name,self.health)

	def __str__(self):
		return "{}:{:02d}".format(self.name,self.health)

	def set_health(self, value):
		self.counters.set_counter("health",value)

	def setup(self):
		self.deck.prepare()
		for _ in range(5):
			self.deck.shuffle()


class Human(Player):

	def __init__(self):
		super().__init__()


if __name__ == '__main__':
	test = Player("Max")
