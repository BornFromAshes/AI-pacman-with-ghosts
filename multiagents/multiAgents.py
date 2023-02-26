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
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        foodDist = float('inf')
        for food in newFood:
            foodDist = min(foodDist, manhattanDistance(newPos, food))

        for ghost in successorGameState.getGhostPositions():
            if (manhattanDistance(newPos, ghost) < 2):
                return float('-inf')
        return successorGameState.getScore() + 1.0 / foodDist


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return  self.getValue(gameState, 0, 0)[1]


    def getValue(self, gameState, index, depth):
        if len(gameState.getLegalActions(index)) == 0 or depth == self.depth:
            return gameState.getScore(), ''
        if index == 0:
            return self.maxValue(gameState, index, depth)
        else:
            return self.minValue(gameState, index, depth)

    def maxValue(self, gameState, index, depth):
        moves = gameState.getLegalActions(index)
        value = float('-inf')
        action = ''
        for move in moves:
            suc = gameState.generateSuccessor(index, move)
            sucIndex = index + 1
            sucDepth = depth
            if sucIndex == gameState.getNumAgents():
                sucIndex = 0
                sucDepth += 1
            temp = self.getValue(suc, sucIndex, sucDepth)[0]
            if temp > value:
                value = temp
                action = move
        return value, action

    def minValue(self, gameState, index, depth):
        moves = gameState.getLegalActions(index)
        value = float('inf')
        action = ''
        for move in moves:
            suc = gameState.generateSuccessor(index, move)
            sucIndex = index + 1
            sucDepth = depth
            if sucIndex == gameState.getNumAgents():
                sucIndex = 0
                sucDepth += 1
            temp = self.getValue(suc, sucIndex, sucDepth)[0]
            if temp < value:
                value = temp
                action = move
        return value, action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, game_state):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.getValue(game_state, 0, 0, float("-inf"), float("inf"))[1]

    def getValue(self, game_state, index, depth, alpha, beta):
        if len(game_state.getLegalActions(index)) == 0 or depth == self.depth:
            return game_state.getScore(), ''
        if index == 0:
            return self.maxValue(game_state, index, depth, alpha, beta)
        else:
            return self.minValue(game_state, index, depth, alpha, beta)

    def maxValue(self, gameState, index, depth, alpha, beta):
        moves = gameState.getLegalActions(index)
        value = float('-inf')
        action = ''
        for move in moves:
            suc = gameState.generateSuccessor(index, move)
            sucIndex = index + 1
            sucDepth = depth
            if sucIndex == gameState.getNumAgents():
                sucIndex = 0
                sucDepth += 1
            temp = self.getValue(suc, sucIndex, sucDepth, alpha, beta)[0]
            if temp > value:
                value = temp
                action = move
            alpha = max(alpha, value)
            if value > beta:
                return value, action
        return value, action

    def minValue(self, gameState, index, depth, alpha, beta):
        moves = gameState.getLegalActions(index)
        value = float('inf')
        action = ''
        for move in moves:
            suc = gameState.generateSuccessor(index, move)
            sucIndex = index + 1
            sucDepth = depth
            if sucIndex == gameState.getNumAgents():
                sucIndex = 0
                sucDepth += 1
            temp = self.getValue(suc, sucIndex, sucDepth, alpha, beta)[0]
            if temp < value:
                value = temp
                action = move
            beta = min(beta, value)
            if value < alpha:
                return value, action
        return value, action


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.getValue(gameState, 0, 0)[1]

    def getValue(self, gameState, index, depth):
        if len(gameState.getLegalActions(index)) == 0 or depth == self.depth:
            return self.evaluationFunction(gameState), ''
        if index == 0:
            return self.maxValue(gameState, index, depth)
        else:
            return self.exValue(gameState, index, depth)

    def maxValue(self, gameState, index, depth):
        moves = gameState.getLegalActions(index)
        value = float('-inf')
        action = ''
        for move in moves:
            suc = gameState.generateSuccessor(index, move)
            sucIndex = index + 1
            sucDepth = depth
            if sucIndex == gameState.getNumAgents():
                sucIndex = 0
                sucDepth += 1
            temp = self.getValue(suc, sucIndex, sucDepth)[0]
            if temp > value:
                value = temp
                action = move
        return value, action

    def exValue(self, gameState, index, depth):
        moves = gameState.getLegalActions(index)
        value = 0
        prob = 1/ float(len(moves))
        for move in moves:
            suc = gameState.generateSuccessor(index, move)
            sucIndex = index + 1
            sucDepth = depth
            if sucIndex == gameState.getNumAgents():
                sucIndex = 0
                sucDepth += 1
            temp = self.getValue(suc, sucIndex, sucDepth)[0]
            value += temp * prob
        return value, ''


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood().asList()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    "*** YOUR CODE HERE ***"
    foodDist = float('inf')
    for food in newFood:
        foodDist = min(foodDist, manhattanDistance(newPos, food))
    temp = 0
    for ghost in successorGameState.getGhostPositions():
        temp += manhattanDistance(newPos,ghost)
    if(sum(newScaredTimes) > 0):
        temp*=-1
    temp += 0.01
    return successorGameState.getScore() + 1.0 / foodDist - 100.0/temp
# Abbreviation
better = betterEvaluationFunction
