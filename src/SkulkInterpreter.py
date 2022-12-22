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
| Max Marshall    | 2022-12-22 | Added some basic functionality, still need to
|                 |            | continue to reach sliver of MVP
|
|
"""
from Card import Card, ExampleCard


class SkulkInterpreter:
	def __init__(self, arena):
		self.arena = arena
		self.debug = True
		self.stack = []
		self.commands = { "or":self.b_or,
											"not":self.b_not,
											"=":self.assignment,
											"add":self.add,
											"==":self.equal_to,
											"<":self.less_than,
											"<=":self.less_than_equal_to,
											">":self.greater_than,
											">=":self.greater_than_equal_to,
											"create":self.create,
											"untap_card":self.untap_card
											}
		self.update_cards()

	def print(self,string):
		if self.debug:
			print("SKLK_INTRPRTR: {}".format(string))
		return

	def get_cards(self):
		if self.arena is None:
			self.print("Arena is NONE")
			return []
		return self.arena.get_known_cards()
	
	def update_cards(self):
		self.print("Updating")
		cards = []
		if self.arena is not None:
			cards = self.get_cards()
		self.update(cards)
		
	def broadcast(self,action, cards, trial=False):
		self.print("Broadcasting -> {}".format(action))
		cards = self.get_cards()
		changed = False
		for card in cards:
			finished, added = self.execute(card,action,trial)
			if finished:
				changed = True
				if not trial:
					for item in added:
						self.stack.append(item)
		return changed

	def singlecast(self,action,target,trial=False):
		self.print("Singlecasting -> {}: {}".format(target, action))
		return self.execute(target,action,trial)

	def execute(self,card,action,trial=False):
		self.env = {}
		if not action in card.skulk:
			return
		self.new_state = self.arena.get_state()
		for command in card.skulk[action]:
			pass
		if not trial:
			self.arena.set_state(self.new_state)
		return True

	def try_execute(self,card,action):
		return self.execute(card,action,True)

	def isSkulkTaken(self,card,comm):
		changed = False
		while comm in card.intercepts:
			comm = card.intercepts[comm]
			changed = True
		new_comm = "new_"+comm
		if changed:
			return new_comm
		return comm

	def evaluate(self,card,comm):
		while comm in card.intercepts:
			comm = card.intercepts[comm]
		return self.execute(card,comm)

	def force_evaluate(self,card,comm):
		return self.execute(card,comm)

	####################################
	##  COMMANDS  ######################
	####################################

	# Boolean Alg.
	def b_not(self, card, comm, args):
		return not self.execute()

	def b_or(self, card, comm1, comm2):
		passed = False
		if self.try_execute(card,comm1):
			self.execute(card,comm1)
			passed = True
		if self.try_execute(card,comm2):
			self.execute(card,comm2)
			passed = True
		return passed

	def b_xor(self, card, comm1, comm2):
		return

	# Internal
	def assignment(self, var, value):
		self.env[var] = value

	def add(self,card,comm,skulk):
		card.skulk[comm] = skulk

	# Internal Game States
	def update(self, cards):
		self.broadcast("update", cards)
		return

	# Internal - Assertions
	def equal_to(self, var1, var2):
		var1 = self.get_var(var1)
		var2 = self.get_var(var2)
		return var1 == var2

	def not_equal_to(self, var1, var2):
		return not self.equal_to(var1, var2)

	def less_than(self, var1, self2):
		var1 = self.get_var(var1)
		var2 = self.get_var(var2)
		return var1 < var2

	def greater_than_equal_to(self, var1, var2):
		return not self.less_than(var1, var2)

	def greater_than(self, var1, var2):
		var1 = self.get_var(var1)
		var2 = self.get_var(var2)
		return var1 > var2

	def less_than_equal_to(self, var1, var2):
		return not self.greater_than(var1, var2)

	# Actual commands
	def create(self, card=None, player=None):
		print("Hello_World!")

	def replace(self,card,comm,new_comm,new_skulk=None):
		if new_skulk:
			comm = self.isSkulkTaken(card,comm)
			self.add_skulk(card,new_comm,new_skulk)
		while comm in card.intercepts:
			comm = card.intercepts[comm]
		card.intercepts[comm] = new_comm

	def untap_card(self,card): # DONE
		card.counters.sett("tapped",0)
		return



if __name__ == '__main__':
	card = ExampleCard()

	test = SkulkInterpreter(None)
	card.counters.sett("tapped",1)
	test.commands["untap_card"](card)
	print(card.counters.get("tapped"))
