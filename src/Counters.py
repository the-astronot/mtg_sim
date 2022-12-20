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
| Max Marshall    | 2022-12-19 | Created File
|
|
|
"""

#import

class Counter:
	def __init__(self, Value=0,Min=None,Max=None):
		self.value = Value
		self.min = Min
		self.max = Max

	def change(self,value):
		temp = self.value + value
		if not (temp < self.min or temp > self.max):
			self.value = temp
		return self.value, temp < self.min, temp > self.max

	def set_value(self, value):
		self.value = value
		return self.value
			

class Counters:
	def __init__(self):
		pass


class Player_Counters(Counters):
	def __init__(self):
		self.counters = {}
		self.counters["health"] = Counter(20,1)
		self.counters["poison"] = Counter(0,0,10)
	
	def change_counter(self,name,amount):
		if name in self.counters:
			counter = self.counters[name]
			return counter.change(amount)
		else:
			self.counters[name] = Counter(0,0)
			return counter.change(amount)

	def set_counter(self,name,value):
		if name in self.counters:
			counter = self.counters[name]
			return counter.set_value(value)
		else:
			self.counters[name] = value
			return self.value



if __name__ == '__main__':
	test = Counters()
