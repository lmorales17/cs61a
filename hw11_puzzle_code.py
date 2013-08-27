#Puzzle 1
import string
def foo_converter(text):
	return text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyz", "cdefghijklmnopqrstuvwxyzab"))
#Puzzle 2

def foo_finder(symbols):
	rare_characters = string.ascii_uppercase
	rare_character_string = ''
	for symbol in symbols:
		if symbol in rare_characters:
			rare_character_string += symbol
	return rare_character_string

