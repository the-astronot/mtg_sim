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


class Card:

	def __init__(self, data):
		self.types = []
		self.colors = []
		self.cost = {}
		self.converted_cost = None
		self.unpack_data(data)
		self.location = None

	def __repr__(self):
		return self.short_name

	def __str__(self):
		return "{}:{}:{}".format(self.name,self.type_short,self.conv_cost)

	def unpack_data(self, data):
		self.name = data.name
		self.type = data.type

	def set_location(self, location):
		self.location = location



if __name__ == '__main__':
	
	test = Card()
