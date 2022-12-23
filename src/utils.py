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
| Max Marshall    | 2022-12-20 | Created File
| Max Marshall    | 2022-12-22 | Added process_skulk, strip_comments
|
|
"""

def yes(string, default="y"):
	yes_vals = ["y","ye","yes"]
	no_vals = ["n","no"]
	if string.lower() in yes_vals:
		return True
	if string.lower() in no_vals:
		return False
	if string == "":
		if default in yes_vals:
			return True
		if default in no_vals:
			return False
	# If matches no cases, deafult False
	return False


# Complex AutoPay bullsh*t to enable not specifying lands for casting
def pay_optimization(lands,card):
	return True


def strip_comments(text):
	while text.find("#") != -1:
		start = text.find("#")
		end = text.find("\n",start)
		text = text[:start] + text[end+1:]
	return text


def process_skulk(text):
	text = strip_comments(text)
	skulk = {}
	commands = text.split("}")
	for command in commands:
		if command.strip("\n").strip("\t").strip() == "":
			continue
		name, script = command.split("{")
		name = name.strip("\n").strip()
		if script.strip("\n").strip("\t").strip() == "":
			skulk[name] = [[]]
			continue
		script = script.strip("\n").strip().split(";")
		script.remove("")
		for i in range(len(script)):
			line = script[i]
			line = line.strip("\n").strip().split(" ")
			for j in range(len(line)):
				item = line[j]
				line[j] = item.strip("\n").strip()
			script[i] = line
		skulk[name] = script
	return skulk


if __name__ == '__main__':
	pass
