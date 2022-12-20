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
|
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
	# If matches no cases, return False
	return False




if __name__ == '__main__':
	pass
