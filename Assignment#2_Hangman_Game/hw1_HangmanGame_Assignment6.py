# Hangman game!

import sys
import random

def pick_word():
	# Assignment6 chose random words from files
	file = open('hangman.txt', 'r')
	wordList = []
	for line in file.readlines():
		line = line.strip()
		wordList.append(line)
	file.close()
	return wordList[random.randint(0, len(wordList) - 1)]

def game():

	A = pick_word()
	L = []
	for string in A:
		L.append('_')

	# Counters
	play = True
	counter = 0

	while play == True:
		i = 0
		j = 7

		letter = str(input("Guess a letter: "))

		for currentletter in A:
			if letter == currentletter:
				L[i] = letter
				j = j - 1
			i = i + 1

		# Print BAD GUESS! when given wrong string
		if j == 7:
			print("BAD GUESS!")
			counter = counter + 1
			print("You still have ", 6 - counter, "chance.")
		
		# After 6 times, Game Over
		if counter == 6:
			print("Game Over, you lose the game!")
			print("The word is ", A, ".")
			sys.exit()

		# Display what the player has thus far (L) with a space
		# separating each letter
		print(' '.join(str(n) for n in L))

		# Test to see if the word has been successfully completed,
		# and if so, end the loop
		if A == L:
			play = False

	print("GREAT JOB!")

game()
