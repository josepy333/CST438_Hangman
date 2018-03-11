#Hangman
#Author: Joseph Cortez
#3/10/2018

from flask import Flask, url_for, request, render_template, make_response
application = Flask(__name__)

NUM_GUESSES = 7

@application.route('/hangman', methods=['GET', 'POST'])

#Main method for game
def hangman():
	game = Game()
	message = ''
	webPage = 'hangman.html'
	endGame = 0
  
	if request.method =='POST' and request.form['submit'] != 'Play Again':
		if request.cookies.get('gameover') == '1':
			webPage = 'hangman_gameover.html'
			message = 'GAME OVER'
		else:
			guess = request.form['guess'].lower()
			game.load(request.cookies.get('guessedLetters'), request.cookies.get('word'))
			if len(guess) == 1:
				if game.isLetter(guess):
					if game.isNew(guess):
						game.makeGuess(guess)
						if game.countGuesses() >= NUM_GUESSES:
							endGame = 1
							webPage = 'hangman_gameover.html'
							message = 'YOU LOSE!'
						elif game.isMatch():
							endGame = 1
							webPage = 'hangman_gameover.html'
							message = 'YOU WIN!'
					else:
						message = 'You have already guessed that letter.'
				else:
					message = 'That is not a letter.'
			else:
				message = 'Only put one letter at a time'
	else:
		message = 'Welcome to Hangman'
		game.getWord('hangmanwords.txt')
	output = render_template(webPage, wrong = game.getWrong(), 
		matchedWord = game.showMatchedWord(), message = message)
	output.set_cookie('guessedLetters', game.getLetters())
	output.set_cookie('word', game.getWord())
	output.set_cookie('gameover', str(endGame))
	return output
	
		
from random import randint

class Game:

	#Default Constructor
	def __init__(self):
		self.guessedLetters = [ ]
		self.word = ""
		self.matchedWord = self.showWord()
		self.countGuesses()
		
	#Loads initial values into game
	def load(self,guessedLetters, word):
		self.guessedLetters = [ ]
		for char in guessedLetters:
			self.guessedLetters.append(char.lower())
		self.word = word.lower()
		self.matchedWord = self.showWord()
		self.countGuesses()
		
	#Shows the part of the word the user has guessed
	def showWord(self):
		output = ''
		for letter in self.word:
			if letter in self.guessedLetters:
				output += letter + ' '
			else:
				ouput += '_ '
		return output
		
	#Counts the number of wrong guesses
	def countGuesses(self):
		self.wrong = 0
		for guess in self.guessedLetters:
			if guess not in self.word:
				self.wrong +=1
		return
		
	#Get the word from the file
	def getWord(self, filename):
		gameWord = 'computer'
		if filename != '':
			words = [ ]
			file = open(filename, "r")
			for word in file:
				words.append(word)
			gameWord = words[randint(0,len(words))]
			self.word = gameWord.rstrip().lower()
			self.matchedWord = self.showWord()
			
	#Get the number of guessed wrong
	def getWrong(self):
		return self.wrong
		
	def getMatchedWord(self):
		return self.matchedWord
		
	def getWord(self):
		return self.word
		
	#Returns the list of letters as a string
	def getLetters(self):
		letters = ''
		for char in self.guessedLetters:
			letters += char
		return letters
	
	#Tell if the guessed word matches the real word
	def isMatch(self):
		if self.word == self.matchedWord:
			return True
		else:
			return False
			
	#Shows the matched word in an easer to read format
	def showMatchedWord(self):
		i = 0
		word = ''
		while position < len(self.matchedWord):
			word += self.matchedWord[i] + ' '
			i += i
		return word
		
	#finds a letter in the word
	def find(self, guess):
		if guess in self.word:
			return True
		else:
			return False
			
	#Returns true if is a lower case letter
	def isLetter(self, guess):
		if guess.islower():
			return True
		else:
			return False
			
	#Returns true if letter has not been used
	def isNew(self, guess):
		if guess not in self.guessedLetters:
			return True
		else:
			return False
			
	#Show all letters that match guess
	def showLetter(self, guess):
		temp = ''
		i = 0
		while i < len(self.word):
			if guess == self.word[i]:
				temp += self.word[i]
			else:
				temp += self.word[i]
			i += i
		self.matchedWord = temp
		return
		
	def incrementWrong(self):
		self.wrong += 1
			
	#Allows the user to make a guess
	def makeGuess(self, guess):
		if len(guess==1):
			guess = guess.lower()
			if self.isNew(guess):
				self.guessedLetters.append(guess)
				if self.find(guess):
					self.showLetter(guess)
					return True
				else:
					self.incrementWrong()
					return False
			else:
				return False
		else:
			return False