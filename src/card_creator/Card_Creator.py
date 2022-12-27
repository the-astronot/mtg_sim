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
| Max Marshall    | 2022-12-26 | Created File
|
|
|
"""
import json

class Card_Creator:
	def __init__(self):
		pass


class MTGJSON(Card_Creator):
	def __init__(self, filename, card_dest, card_names=None):
		self.filename = filename
		self.card_names = card_names
		self.card_dest = card_dest
		self.load_json()
		self.color_map = {
			"R":"R",
			"G":"G",
			"U":"B",
			"W":"W",
			"B":"K"
		}
		self.type_map = {
			"Creature": "C",
			"Land": "L",
			"Planeswalker": "P",
			"Instant": "I",
			"Enchantment": "E",
			"Sorcery": "S",
			"Artifact": "A",
			"Token": "T"
		}

	def load_json(self):
		f = open(self.filename,"r")
		self.card_data = json.load(f)
		f.close()
		self.card_data = self.card_data["data"]
		return

	def create_cards(self):
		if self.card_names is None:
			for card_obj in self.card_data:
				self.create_card(card_obj,self.card_data[card_obj][0])
		else:
			for card_obj in self.card_data:
				if card_obj in self.card_names:
					self.create_card(card_obj,self.card_data[card_obj][0])
		return

	def replace_colors(self,colors):
		new_colors = []
		for color in colors:
			new_colors.append(self.color_map[color])
		if new_colors == []:
			new_colors.append("C")
		return new_colors

	def create_card(self,name,data):
		print(name)
		print(data)
		save_data = {"name":name}
		# Colors
		save_data["colors"] = self.replace_colors(data["colors"])
		# Converted Cost
		save_data["convcost"] = data["manaValue"]
		save_data["subtypes"] = data["subtypes"]
		save_data["supertypes"] = data["supertypes"]

		save_data["text"] = data["text"]
		save_data["ftext"] = ""

		return


mtgjson = "../../data/AtomicCards.json"
card_dest = "../../data/test_cards/"
cards = ["Swamp", "Death Baron"]

if __name__ == '__main__':
	test = MTGJSON(mtgjson,card_dest,cards)
	test.create_cards()
