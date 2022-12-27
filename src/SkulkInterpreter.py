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
| Max Marshall    | 2022-12-26 | Modified code away from states towards envs
|
"""
from Card import Card, ExampleCard
from utils import pay_optimization


class CMND_STRUCT:
	def __init__(self, cmnd, card, player):
		self.command = cmnd
		self.card = card
		self.player = player


class SkulkInterpreter:
	def __init__(self, arena):
		self.arena = arena
		self.debug = True
		self.command_stack = []
		self.current_strct = None
		self.var_num = 0
		# Dict of all skulk command names to command funcs
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
		self.side_effects = {
			"draw": "is_drawn",
			"cast": "is_cast",
			"pay": "is_paid",
			"destroy": "is_destroyed",
			"exile": "is_exiled",
			"untap": "is_untapped",
			"modify": "is_modified",
			"bond": "is_bound",
			"equip": "is_equipped"
		}

	def get_var(self):
		string = "_{}".format(self.var_num)
		self.var_num += 1
		return string

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
		
	def broadcast(self,action, env=None):
		# Call for action from all available cards
		self.print("Broadcasting -> {}".format(action))
		cards = self.get_cards()
		changed = False
		for card in cards:
			finished, added = self.execute(card,action,env)
			if finished:
				changed = True
				for item in added:
					self.currrent_stack.append(item)
		return changed

	def singlecast(self,action,target,trial=False):
		# Call for action from single card
		self.print("Singlecasting -> {}: {}".format(target, action))
		return self.execute(target,action,trial)

	def find_skulk(self, loc, action):
		# Figures out where the relevant skulk code resides
		if action in loc.skulk:
			while action in loc.interrupts:
				action = loc.interrupts[action]
			return loc.skulk[action]
		return []

	def execute(self,card=None,action=None,player=None,env=None):
		# Execute skulk code
		if card is None:
			card = self.current_strct.card
		if action is None:
			action = self.current_strct.action
		if player is None:
			player = self.current_strct.player
		side_effects = []
		if not action in card.skulk:
			if not action in player.skulk:
				return False, []
			script_loc = player
		script_loc = card
		script = self.find_skulk(script_loc,action)
		for command in script:
			args = []
			if len(command) > 1:
				args = command[1:]
			success, effects = self.commands[command[0]](card,env,args)
			if not success:
				return False, []
			side_effects = side_effects + effects
		return True, side_effects

	def try_execute(self,card,action):
		# Chcek whether skulk code would evaluate to True or False
		env = {}
		return self.execute(card,action,env)

	def isSkulkTaken(self,card,comm):
		# Checks where replacement code should be stored
		changed = False
		while comm in card.intercepts:
			comm = card.intercepts[comm]
			changed = True
		new_comm = "new_"+comm
		if changed:
			return new_comm
		return comm

	def evaluate(self,card,comm):
		# Find and execute required code, duplicate of find - to be replaced
		while comm in card.intercepts:
			comm = card.intercepts[comm]
		return self.execute(card,comm)

	def force_evaluate(self,card,comm):
		# Force evaluation without interrupts
		return self.execute(card,comm)

	####################################
	##  COMMANDS  ######################
	####################################

	# Boolean Alg.
	def b_not(self, card, comm, args):
		return not self.execute(card,comm)[0], []

	def b_or(self, card, comm1, comm2):
		passed = False
		side_effects = []
		if self.try_execute(card,comm1):
			_, effects = self.execute(card,comm1)
			passed = True
			side_effects = side_effects + effects
		if self.try_execute(card,comm2):
			_, effects = self.execute(card,comm2)
			passed = True
			side_effects = side_effects + effects
		return passed, side_effects

	def b_xor(self, card, comm1, comm2):
		return False, []

	# Conditionals
	def c_if(self,card,args):
		cond = args[0]
		comm1 = args[1]
		comm2 = args[2]
		if self.try_execute(card,cond):
			return self.evaulte(card,comm1)
		return self.evaluate(card,comm2)

	# Internal
	def assignment(self, var, value):
		self.env[var] = value

	def add(self,card,comm,skulk):
		card.skulk[comm] = skulk

	# Internal Game States
	def update(self, cards):
		return self.broadcast("update", cards)

	# Internal - Assertions
	def equal_to(self, var1, var2): # This makes no fucking sense, what is this?
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

	def echo(self, card=None, player=None, string=None):
		print("{}".format(string))
		
	def goto(self,card,player,args):
		target = args[0]
		# assert target in locations
		current_loc = card.location
		current_loc.cards.remove(card)
		card.location = target
		target.cards.append(card)

	def isAlive(self,card,player):
		if card.get("in_play") == True:
			return True
		return False

	def pay(self, card, player):
		lands = []
		for land in player.mat.cards:
			if land.types["L"]:
				lands.append(land)
		return pay_optimization(lands,card)

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
