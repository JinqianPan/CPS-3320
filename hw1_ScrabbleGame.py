# Scrabble Game

def letterScore(singleLetter):

	# Save scores into dictionary

	tileValue = {'A':1, 'B':3, 'C':3, 'D':2, 'E':1, 'F':4, 'G':2, 'H':4, 'I':1, 'J':8, 'K':5, 'L':1, 'M':3, 'N':1, 'O':1, 'P':3, 'Q':10, 'R':1, 'S':1, 'T':1, 'U':1, 'V':4, 'W':4, 'X':8, 'Y':4, 'Z':10}

	# Determine whether the single string is a letter

	if singleLetter.isalpha() == True:

		# Make swtich letter to capital letter

		singleLetter = singleLetter.upper()

		return tileValue.get(singleLetter)

	else:

		return 0

def wordScore(word):

	sum = 0

	for singleLetter in word:

		# sum the score of each string

		sum = sum + letterScore(singleLetter)

	return sum

# Input

word = str(input("Please enter a word or string: "))

# Output

print("You get ", wordScore(word), " Scores!")