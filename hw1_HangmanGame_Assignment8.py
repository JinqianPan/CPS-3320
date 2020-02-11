# Hangman game!

import sys
import random
import turtle
from random_word import RandomWords

def pick_word():
	r = RandomWords()
	return r.get_random_word()

def game():

	A = pick_word()
	L = []
	for string in A:
		L.append('_')

	# Turtle
	t = turtle.Turtle()
	t.penup()
	t.setx(-250)
	t.sety(80)
	t.pd()
	t.speed(50)
	t.fd(100)
	t.rt(180)
	t.fd(50)
	t.rt(90)
	t.fd(170)
	t.rt(90)
	t.fd(100)
	t.rt(90)
	t.fd(50)
	t.ht()

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
		if counter == 1:
			t.pu()
			t.setx(-120)
			t.sety(180)
			t.pd()
			t.circle(20)
			t.ht()
		elif counter == 2:
			t.pu()
			t.setx(-100)
			t.sety(160)
			t.pd()
			t.fd(50)
			t.ht()
		elif counter == 3:
			t.rt(45)
			t.fd(30)
			t.ht()
		elif counter == 4:
			t.pu()
			t.rt(-90)
			t.setx(-100)
			t.sety(110)
			t.pd()
			t.fd(30)
			t.ht()
		elif counter == 5:
			t.pu()
			t.rt(-45)
			t.setx(-100)
			t.sety(135)
			t.pd()
			t.fd(30)
			t.ht()
		elif counter == 6:
			t.pu()
			t.rt(180)
			t.setx(-100)
			t.sety(135)
			t.pd()
			t.fd(30)
			t.pu()
			t.ht()
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
