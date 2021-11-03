import random
import os
import threading
import copy

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Boards. Connect4, Nine men's morris or Draughts can also be implemented.

class TicTacToe:
	""" 
	Implements a TicTacToe board.
	Possible moves 1-9.
	Player are 'x' and 'o'
	"""
	def __init__(self, board=9*[' ']):
		self.board = board

	#### All boards need the following functions to work with the Minimax-opponent.
	def print(self):
		print('  _ _ _  ')
		print('| ' + self.list2String(self.board[ :3]) + ' |')
		print('| ' + self.list2String(self.board[3:6]) + ' |')
		print('| ' + self.list2String(self.board[6:9]) + ' |')
		print('  \u203E \u203E \u203E')

	def checkWinner(self):
		""" ' ' = no winner, otherwise return 'x' or 'o'. """
		from operator import itemgetter

		winners = [ self.board[:3],  self.board[3:6],  self.board[6:9], 
					self.board[::3], self.board[1::3], self.board[2::3],
					itemgetter(0,4,8)(self.board), itemgetter(2,4,6)(self.board)]

		for winner in winners:
			if self.allTheSame(winner):
				return winner[0]

		return ' '

	def deleteMove(self, i):
		""" 0 = everything fine. 1 = invalid move """
		if self.board[i-1] == ' ':
			print('Move is already empty.')
			return 1
		self.board[i-1] = ' '
		return 0

	def setMove(self, i, player):
		""" 0 = everything fine. 1 = invalid move """
		if not(player == 'x' or player == 'o'):
			print('Invalid player.')
			return 1
		if self.checkInput(i):
			print('Invalid move.')
			return 1

		self.board[i-1] = player
		return 0

	def possibleMoves(self):
		return [ele for ele in range(1,10) if self.board[ele-1] == ' ']

	#### internal functions, i.e. not used by the opponents
	def checkInput(self, i):
		""" 0 = valid input. 1 = invalid input """
		if type(i) != type(1):
			return 1
		if i < 1 or i > 9:
			return 1
		if self.board[i-1] == ' ':
			return 0
		else:
			return 1

	def allTheSame(self, l):
		""" True = List has only either 'x' or 'o' entries. False = otherwise """
		if ' ' in l:
			return False
		result = True
		if len(l) > 0:
			result = all(ele == l[0] for ele in l)
		return result

	def list2String(self, s):
		return (' '.join(s))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Player is the prototype of a player.
# After that we implement three opponents: Random opponent, MinimaxOpponent 
# and MinimaxOpponent with Threads

class Player:
	""" 
	Prototype of an opponent.
	Game must terminate with Win, Loss or Draw.
	play() performs one game: Human always 'x' vs Computer always 'o'.
	"""
	def __init__(self, board):
		self.board = board

	def nextMove(self, showThought=False):
		""" computes the next move. """
		pass

	def play(self, firstMove='j'):
		""" performs a whole game """
		numMoves = len(board.board)
		numIterations = int(numMoves / 2) + numMoves % 2

		for round in range(0, numIterations):
			if firstMove != 'j':
				# compute next move and set it
				move = self.nextMove()

				# update board
				if self.board.setMove(move, 'o'):
					print('Computerzug ungueltig. Algorithmus fehlerhaft.')
					quit()

				# check winner
				winner = self.board.checkWinner()
				if winner != ' ' or (round == numIterations-1 and firstMove == 'nOK'):
					break

			# forget about the first move
			if firstMove == 'n':
				firstMove = 'nOK'
			if firstMove == 'j':
				firstMove = 'jOK'

			# show board
			os.system('clear')
			self.board.print()

			# ask for next move and update board
			while True:
				try:
					move = int(input('Nummer des Feldes eingeben (0 = beenden): '))
				except:
					continue
				if move == 0:
					quit()
				if not(self.board.setMove(move, 'x')):
					break

			# check winner
			winner = self.board.checkWinner()
			if  winner != ' ':
				break

		# announce winner
		os.system('clear')
		self.board.print()
		print(winner + ' hat gewonnen.')

class RandomOpponent(Player):
	""" 
	Opponent performs random moves.
	"""
	def __init__(self, board):
		Player.__init__(self, board)

	def nextMove(self):
		return random.choice(self.board.possibleMoves())
	
class MinimaxOpponent(Player):
	""" 
	Implementation of Minimax Algorithm for games with three outcomes.
	"""
	def __init__(self, board):
		Player.__init__(self, board)

	def evaluateMove(self, previousPlayer):
		"""
		recurively sets a possible move and returns the 
		outcome of the game when there are no possible moves
		0 = Draw, 1 = Computer 'o' wins, -1 = Human 'x' wins
		"""
		# Is there a winner?
		winner = self.board.checkWinner()
		if winner != ' ':
			if winner == 'x':
				return -1
			elif winner == 'o':
				return 1

		# next player
		currentPlayer = 'o' if (previousPlayer == 'x') else 'x'

		# evaluate next possible moves
		moves = self.board.possibleMoves()

		# game over? no winner
		if len(moves) == 0:
			return 0

		# check out next possible moves
		scores = []
		for ele in moves:
			# realise move
			self.board.setMove(ele, currentPlayer)
			# recursion
			scores.append(self.evaluateMove(currentPlayer))
			# undo move
			self.board.deleteMove(ele)
			# can we leave the node? (here we use that 1 is maximum and -1 minimum)
			if previousPlayer == 'x':
				if scores[-1] == 1:
					break
			else:
				if scores[-1] == -1:
					break

		# return max if previous player is 'x'
		if previousPlayer == 'x':
			return max(scores)
		# return min if previous player is 'o'
		if previousPlayer == 'o':
			return min(scores)


	def nextMove(self, showThought=False):
		""" overwrite function from Player. Return next computer move. """
		moves = self.board.possibleMoves()

		# evaluate moves
		movesScore = []
		for ele in moves:
			# realise move
			self.board.setMove(ele, 'o')
			# recursion
			movesScore.append(self.evaluateMove('o'))
			# undo move
			self.board.deleteMove(ele)
			# can we leave the node? (here we use that 1 is maximum)
			if movesScore[-1] == 1:
				break

		# show toughts
		if showThought == True:
			print(moves)
			print(movesScore)
			input()

		return moves[movesScore.index(max(movesScore))]

class MinimaxOpponentThreads(Player):
	""" 
	Implementation of Minimax Algorithm for games with three outcomes.
	Uses threads to speed up computing.
	It starts from
	"""
	def __init__(self, board):
		Player.__init__(self, board)
		self.lenOfChunks = 1

	def evaluateMove(self, board, previousPlayer):
		# Is there a winner?
		winner = board.checkWinner()
		if winner != ' ':
			if winner == 'x':
				return -1
			elif winner == 'o':
				return 1

		# next player
		currentPlayer = 'o' if (previousPlayer == 'x') else 'x'

		# evaluate next possible moves
		moves = board.possibleMoves()

		# game over? no winner
		if len(moves) == 0:
			return 0

		# check out next possible moves
		scores = []
		for ele in moves:
			# realise move
			board.setMove(ele, currentPlayer)
			# recursion
			scores.append(self.evaluateMove(board, currentPlayer))
			# undo move
			board.deleteMove(ele)
			# can we leave the node? (here we use that 1 is maximum and -1 minimum)
			if previousPlayer == 'x':
				if scores[-1] == 1:
					break
			else:
				if scores[-1] == -1:
					break

		# return max if previous player is 'x'
		if previousPlayer == 'x':
			return max(scores)
		# return min if previous player is 'o'
		if previousPlayer == 'o':
			return min(scores)

	def threadCalc(self, chunk, board, movesScore):
		""" required for threading """
		for ele in chunk:
			# realise move
			board.setMove(ele, 'o')
			# recursion
			movesScore.append([ele, self.evaluateMove(board, 'o')])
			# undo move
			board.deleteMove(ele)
			# can we leave the node? (here we use that 1 is maximum)
			if movesScore[-1] == 1:
				break

	def nextMove(self, showThought=False):
		moves = self.board.possibleMoves()

		# chunk list of possible moves
		chunksMoves = [moves[i:i + self.lenOfChunks] for i in range(0, len(moves), self.lenOfChunks)]

		# prepare threads and start them
		threads = []
		movesScore = []
		for chunk in chunksMoves:
			boardCopy = copy.deepcopy(self.board)
			threads.append(threading.Thread(target=self.threadCalc, args=(chunk, boardCopy, movesScore)))
			threads[-1].start()

		# join threads
		for thread in threads:
			thread.join()

		# order movesScores
		movesScore.sort(key=lambda a: a[0])
		movesScore = [ele[1] for ele in movesScore]

		# show toughts
		if showThought == True:
			print(moves)
			print(movesScore)
			input()

		return moves[movesScore.index(max(movesScore))]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Let's try it.

# show welcome screen for TicTacToe
print('\n--- Willkommen bei TicTacToe ---\n')
print('Hier sind das Spielfeld')
print('und die Nummerierung.')
TicTacToe([str(i) for i in range(1,10)]).print()
print('Sie spielen mit x.')
while 1:
	try:
		firstMove = str(input('Wollen Sie anfangen? (j/n, q=quit): '))
	except:
		continue
	if firstMove == 'q':
		quit()
	if firstMove == 'j' or firstMove == 'n':
		break

# create the board
board = TicTacToe()

# choose opponent and perform one game
#RandomOpponent(board).play()
MinimaxOpponent(board).play(firstMove=firstMove)
#MinimaxOpponentThreads(board).play(firstMove=firstMove)
