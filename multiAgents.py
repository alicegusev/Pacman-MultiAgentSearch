# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import math
import random, util

from game import Agent

class ReflexAgent(Agent):
	"""
	A reflex agent chooses an action at each choice point by examining
	its alternatives via a state evaluation function.

	The code below is provided as a guide.  You are welcome to change
	it in any way you see fit, so long as you don't touch our method
	headers.
	"""


	def getAction(self, gameState):
		"""
			You do not need to change this method, but you're welcome to.

		getAction chooses among the best options according to the evaluation function.

		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
		"""
		# Collect legal moves and child states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		"Add more of your code here if you want to"

		return legalMoves[chosenIndex]

	def evaluationFunction(self, currentGameState, action):
		"""
		This question is not included in project for CSCI360
		Design a better evaluation function here.

		The evaluation function takes in the current and proposed child
		GameStates (pacman.py) and returns a number, where higher numbers are better.

		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.

		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState (pacman.py)
		childGameState = currentGameState.getPacmanNextState(action)
		newPos = childGameState.getPacmanPosition()
		newFood = childGameState.getFood()
		newGhostStates = childGameState.getGhostStates()
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

		"*** YOUR CODE HERE ***"
		return childGameState.getScore()

def scoreEvaluationFunction(currentGameState):
	"""
	This default evaluation function just returns the score of the state.
	The score is the same one displayed in the Pacman GUI.

	This evaluation function is meant for use with adversarial search agents
	(not reflex agents).
	"""
	return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
	"""
	This class provides some common elements to all of your
	multi-agent searchers.  Any methods defined here will be available
	to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

	You *do not* need to make any changes here, but you can if you want to
	add functionality to all your adversarial search agents.  Please do not
	remove anything, however.

	Note: this is an abstract class: one that should not be instantiated.  It's
	only partially specified, and designed to be extended.  Agent (game.py)
	is another abstract class.
	"""

	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
		self.index = 0 # Pacman is always agent index 0
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
	"""
	Your minimax agent (question 1)
	"""

	def getAction(self, gameState):
		"""
		Returns the minimax action from the current gameState using self.depth
		and self.evaluationFunction.

		Here are some method calls that might be useful when implementing minimax.

		gameState.getLegalActions(agentIndex):
		Returns a list of legal actions for an agent
		agentIndex=0 means Pacman, ghosts are >= 1

		gameState.getNextState(agentIndex, action):
		Returns the child game state after an agent takes an action

		gameState.getNumGhost():
		Returns the total number of ghosts in the game
		"""

		def minimax(state,depth,agentId):
			if depth == self.depth or state.isWin() or state.isLose():
				return self.evaluationFunction(state)
			if agentId == 0: # pacman, maximizing player
				value = -math.inf
				for action in state.getLegalActions(0):
				   value = max(value, minimax(state.getNextState(0,action),depth,1))
				return value
			else: # ghosts
				value = math.inf
				for action in state.getLegalActions(agentId):
					child = state.getNextState(agentId,action)
					#Case 1: Some agents/ghosts have not be visited
					if agentId != state.getNumGhost():
						value = min(value, minimax(child, depth, agentId + 1))
					else: # last ghost
						value = min(value, minimax(child, depth + 1, 0))
				return value

		#call minimax
		# values = []
		# for action in gameState.getLegalActions(0):
		#     values.append((action,minimax(gameState.getNextState(0,action),0,1)))

		# sorted_values = sorted(values, key=lambda x:x[1], reverse = True)

		# return sorted_values[0][0]
		small = -math.inf
		action = Directions.WEST
		for act in gameState.getLegalActions(0):

			value = minimax(gameState.getNextState(0, act),0,1)
			if value > small or small == -math.inf:
				small = value
				action = act

		return action




class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	Your minimax agent with alpha-beta pruning (question 2)
	"""

	def getAction(self, gameState):
		"""
		Returns the minimax action using self.depth and self.evaluationFunction
		"""
		def alphabeta(state,a,b,depth,agentId):

			if depth == self.depth or state.isWin() or state.isLose():
				return self.evaluationFunction(state)
			if agentId == 0: # pacman, maximizing player
				value = -math.inf
				for action in state.getLegalActions(0):
					value = max(value, alphabeta(state.getNextState(0,action),a,b,depth,1))
					# if value > b:
					#     return value
					# a = max(a,value)
					a = max(a,value)
					if a > b:
						return value;
				return value
			else: # ghosts
				value = math.inf
				for action in state.getLegalActions(agentId): 
					#Case 1: Some agents/ghosts have not be visited
					if agentId != state.getNumGhost():
						value = min(value, alphabeta(state.getNextState(agentId,action), a, b, depth, agentId + 1))
					else: # last ghost
						value = min(value, alphabeta(state.getNextState(agentId,action), a, b, depth + 1, 0))  
					# if value < a:
					#     return value
					# b = min(value, b)
					b = min(b,value)
					if b < a:
						return value; 
				return value

		#call minimax
		values = []
		a = -math.inf
		b = math.inf

		utility = -math.inf
		action = Directions.WEST
		a = -math.inf
		b = math.inf
		for act in gameState.getLegalActions(0):
			value= alphabeta(gameState.getNextState(0,act),a, b, 0,1)
			if value > utility:
				utility = value
				action = act
			if utility > b:
				return utility
			a = max(a, utility)

		return action



		# return sorted_values[0][0]


class ExpectimaxAgent(MultiAgentSearchAgent):
	"""
	  Your expectimax agent (question 3)
	"""

	def getAction(self, gameState):
		"""
		Returns the expectimax action using self.depth and self.evaluationFunction

		All ghosts should be modeled as choosing uniformly at random from their
		legal moves.
		"""
		def expectimax(state,depth,agentId):
			if depth == self.depth or state.isWin() or state.isLose():
				return self.evaluationFunction(state)
			if agentId == 0: # max-value
				value = -math.inf
				for action in state.getLegalActions(0):
					value = max(value, expectimax(state.getNextState(0,action),depth,1))
				return value
			else: # expected value
				value = 0
				for action in state.getLegalActions(agentId):
					child = state.getNextState(agentId,action)
					#Case 1: Some agents/ghosts have not be visited
					if agentId != state.getNumGhost():
						value += expectimax(child, depth, agentId + 1)
					else: # last ghost
						value += expectimax(child, depth + 1, 0)
				return (value / float(len(gameState.getLegalActions(agentId))))


		small = -math.inf
		action = Directions.WEST
		for act in gameState.getLegalActions(0):

			value = expectimax(gameState.getNextState(0, act),0,1)
			if value > small or small == -math.inf:
				small = value
				action = act

		return action



def betterEvaluationFunction(currentGameState):
	"""
	Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	evaluation function (question 4).

	DESCRIPTION: <write something here so we know what you did>
	"""
	value = 0
	"*** YOUR CODE HERE ***"
	numGhosts = currentGameState.getNumGhost()
	numFood = currentGameState.getNumFood()
	score = currentGameState.getScore()
	newPos = currentGameState.getPacmanPosition()

	newGhostStates = currentGameState.getGhostStates()
	newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
	time_count = 0
	for time in newScaredTimes:
		time_count = time_count + time

	ghost_dist = []
	for ghost in currentGameState.getGhostPositions():
		ghost_dist.append(abs(newPos[0] - ghost[0]) + abs(newPos[1] - ghost[1]))

	for ghost in ghost_dist:
		if ghost < 3:
			value += 3*ghost
		elif ghost < 7:
			value += 2*ghost
		else:
			value += .5*ghost
		
	pellet_dist = 0
	count = 0
	for pellet in currentGameState.getCapsules():
		count = count + 1
		pellet_dist = pellet_dist + abs(newPos[0] - pellet[0]) + abs(newPos[1] - pellet[1])
		if (pellet == newPos):
			numGhosts = 0

	value += .2*pellet_dist*numGhosts*time_count*numGhosts

	value += (1.5*score)
	value += -10*numFood
	value += -20*count

	# return value
	# value += (.55*score) + .000001*numFood + ((.69)*ghost_dist) + ((.73)*pellet_dist*time_count*numGhosts)
	return value
	# 585
	# no change: 778.5  -- 3278 
	# numghosts: -524 * .12
	# numFood : -564 * .12
	# numScore : -67.6c
	# ghost_dist: -1599 but gives me 4 points *
	# pellet_dist: -524
# Abbreviation
better = betterEvaluationFunction
