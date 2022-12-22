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
		return self.value, temp < self.min, temp > self.max, 0

	def set_value(self, value):
		self.value = value
		return self.value
			

class MultiCounter:
	def __init__(self):
		self.counters = {}

	def sett(self, name, value):
		if name in self.counters:
			return self.counters[name].set_value(value), 0
		else:
			self.create(name, value)
			return value, 1

	def create(self, name, value, min=0, max=None):
		if name in self.counters:
			return False
		self.counters[name] = Counter(value,min,max)
		return True

	def change(self,name,amt):
		if name in self.counters:
			return self.counters[name].change(amt)
		if amt > 0:
			self.create(name,amt,0)
			return amt, 0, 0, 1

	def get(self, name):
		if name in self.counters:
			c = self.counter[name]
			return c.value, c.min, c.max
		else:
			return None,None,None


class Player_Counters(MultiCounter):
	def __init__(self,health=20):
		super().__init__()
		self.create("health",health)
		self.create("poison",0,0,10)



if __name__ == '__main__':
	test = Counter()
