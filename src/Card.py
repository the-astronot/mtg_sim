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
| Max Marshall    | 2022-12-21 | Fleshed out Basic Card Properties
| Max Marshall    | 2022-12-22 | Added more support towards Skulk, example
|
"""
from Counters import MultiCounter


class Card:

	def __init__(self, data=None):
		self.name = None
		self.counters = MultiCounter()
		self.counters.create("tapped",0,0,1)
		self.types = {"L":False,"C":False,"I":False,"S":False,"A":False,"P":False,"E":False,"T":False}
		self.subtypes = []
		self.permanent = False
		self.colors = {"G":True,"R":True,"B":True,"W":True,"K":True,"C":True}
		self.cost = {"G":0,"R":0,"B":0,"W":0,"K":0,"C":0}
		self.rarity = {"L":False,"C":False,"U":False,"R":False,"M":False}
		self.converted_cost = None
		self.image = None
		self.skulk = {} # Event -> Code
		self.skulk_intercepts = {}
		self.text = ""
		self.ftext = ""
		self.relations = {} # Name -> Card
		self.in_play = False
		self.set = None
		self.hash = None
		self.unpack_data(data)
		self.location = None

	def __repr__(self):
		return self.name

	def __str__(self):
		return "{}:{}:{}".format(self.name,self.type_short,self.conv_cost)

	def unpack_data(self, data=None):
		if data is None:
			return
		self.name = data.name
		self.type = data.type

	def set_location(self, location):
		self.location = location


class Creature(Card):
	def __init__(self,Data=None):
		super().__init__()
		self.permanent = True
		self.unpack_data(Data)

	def unpack(self, data=None):
		self.counters.create("")
		self.counters.create("Power",0)
		self.counters.create("Toughness",0)


class Land(Card):
	def __init__(self,Data=None):
		super().__init__(Data)
		self.types["L"] = True
		self.permanent = True
		self.mana = {"G":0,"R":0,"B":0,"W":0,"K":0,"C":0}
		self.spent = {"G":0,"R":0,"B":0,"W":0,"K":0,"C":0}


class ExampleCard(Creature):
	def __init__(self):
		super().__init__()
		self.name = "Death Baron"
		self.types["C"] = True
		self.cost = {"G":0,"R":0,"B":0,"W":0,"K":2,"C":1}
		self.subtypes = ["Zombie","Wizard"]
		self.converted_cost = 3
		self.counters.sett("Power",2)
		self.counters.sett("Toughness",2)
		self.rarity["R"] = True
		self.text = "Skeletons you control and other Zombies you control get +1/+1 and have deathtouch."
		self.ftext = "For the necromancer barons, killing and recruitment are one and the same."
		self.skulk = {"untap":["isAlive","isTapped","untap_card"],"update":["forall cards","isAlive","not ModifiedByMe","subtype Zombie", "inc Power 1","inc Toughness 1","give deathtouch"]}
		self.skulk_intercepts = {}
		self.set = "M19"

class ExampleLand(Land):
	def __init__(self):
		super().__init__()
		self.subtypes = ["Basic Land"]
		self.name = "Swamp"
		self.colors["K"] = True
		self.mana["K"] = 1
		self.mana["C"] = 1
		self.conv_cost = 0
		self.text=""
		self.ftext="But the fourth... The fourth stayed up! And that's what you're gettin' lad, the strongest castle in these Isles."
		self.skulk = {"untap": ["isOnBoard","isTapped","untap_card"]}
		self.skulk_intercepts = {}
		self.rarity["C"] = True


if __name__ == '__main__':
	
	test = Card()
