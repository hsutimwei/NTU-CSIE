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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        ghosts = [i.getPosition() for i in newGhostStates]
        for i in ghosts:
            if newScaredTimes[0] > 0 and manhattanDistance(i, newPos) <=1.5:
                return 9999
        for i in ghosts:
            if manhattanDistance(i, newPos) <=1.5 and newScaredTimes[0] <= 0 :
                return -999
        if newPos in currentGameState.getFood().asList() or newPos in currentGameState.getCapsules():
            return 9999
        if action==Directions.STOP:
            return -999
        closestfood=999999
        for i in newFood.asList():
            closestfood=min(closestfood,manhattanDistance(i, newPos))
        closestghost=999999
        for j in ghosts:
            closestghost=min(closestghost,manhattanDistance(j, newPos))
            
        if newScaredTimes[0]<=0:
            return  closestghost / closestfood
        else:
            return - closestghost / closestfood
    
def scoreEvaluationFunction(currentGameState: GameState):
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
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
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

        numagent=gameState.getNumAgents()
        
        def maxvalue(state: GameState,depth):
            if state.isWin() or state.isLose() or depth == 0:
                #print("kk",state.isWin() , state.isLose() , depth)
                return self.evaluationFunction(state)
            value=-999999999999
            for action in state.getLegalActions():
                #print(v,action,0,depth)
                value=max(value,minvalue(state.generateSuccessor(0, action),depth,1))
            return value
                
        def minvalue(state: GameState,depth,ghost):
            if state.isWin() or state.isLose() or depth == 0:
                #print("jj",state.isWin() , state.isLose() , depth)
                return self.evaluationFunction(state)
            value=999999999999
            for action in state.getLegalActions(ghost):
                #print(v,action,ghost,depth)
                if ghost==numagent-1:
                    value=min(value,maxvalue(state.generateSuccessor(ghost, action),depth-1))
                else:
                    value=min(value,minvalue(state.generateSuccessor(ghost, action),depth,ghost+1))
                #print(v,action,ghost,depth)
            return value
        
        a=-9999999
        Action=None
        for action in gameState.getLegalActions():
            b= minvalue(gameState.generateSuccessor(0, action), self.depth,1)
            if a<b:
                a=b
                Action=action
        return Action
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numagent=gameState.getNumAgents()
        
        def maxvalue(state: GameState,depth,alpha,beta):
            if state.isWin() or state.isLose() or depth == 0:
                #print("oo",state.isWin() , state.isLose() , depth)
                return self.evaluationFunction(state)
            value=-999999999999
            for action in state.getLegalActions():
                #print(v,action,0,depth)
                value=max(value,minvalue(state.generateSuccessor(0, action),depth,1,alpha,beta))
                if value>beta:
                    #print("pp",beta,value)
                    return value
                alpha=max(alpha,value)
                #print("jj",beta,value)
            return value
                
        def minvalue(state: GameState,depth,ghost,alpha,beta):
            if state.isWin() or state.isLose() or depth == 0:
                #print("jj",state.isWin() , state.isLose() , depth)
                return self.evaluationFunction(state)
            value=999999999999
            for action in state.getLegalActions(ghost):
                #print("kk",action,alpha,beta,value)
                #print(v,action,ghost,depth)
                if ghost==numagent-1:
                    value=min(value,maxvalue(state.generateSuccessor(ghost, action),depth-1,alpha,beta))
                else:
                    value=min(value,minvalue(state.generateSuccessor(ghost, action),depth,ghost+1,alpha,beta))
                if value<alpha:
                    return value
                beta=min(value,beta)
                #print("kk",alpha,beta,value)
                #print(v,action,ghost,depth)
            return value
        
        a=-9999999
        Action=None
        alpha=-99999999999
        beta=99999999999
        for action in gameState.getLegalActions():
            #print(alpha,beta)
            value= minvalue(gameState.generateSuccessor(0, action), self.depth,1,alpha,beta)
            if a<value:
                a=value
                Action=action
            if value>beta:
                #print("pp",beta,value)
                return value
            alpha=max(alpha,value)
        return Action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        numagent=gameState.getNumAgents()
        
        def maxvalue(state: GameState,depth):
            if state.isWin() or state.isLose() or depth == 0:
                #print("kk",state.isWin() , state.isLose() , depth)
                return self.evaluationFunction(state)
            value=-999999999999
            for action in state.getLegalActions():
                #print(v,action,0,depth)
                value=max(value,minvalue(state.generateSuccessor(0, action),depth,1))
            return value
                
        def minvalue(state: GameState,depth,ghost):
            if state.isWin() or state.isLose() or depth == 0:
                #print("jj",state.isWin() , state.isLose() , depth)
                return self.evaluationFunction(state)
            value=999999999999
            sum=0
            cnt=0
            for action in state.getLegalActions(ghost):
                #print(v,action,ghost,depth)
                if ghost==numagent-1:
                    value=maxvalue(state.generateSuccessor(ghost, action),depth-1)
                else:
                    value=minvalue(state.generateSuccessor(ghost, action),depth,ghost+1)
                sum+=value
                cnt+=1
            #print(state.getLegalActions(ghost),sum,cnt)
            return sum/cnt
        
        a=-9999999
        Action=None
        for action in gameState.getLegalActions():
            b= minvalue(gameState.generateSuccessor(0, action), self.depth,1)
            
            if a<=b:
                if action!="Stop" or a!=b:
                    Action=action
                a=b

        return Action

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
    ghosts = [i.getPosition() for i in newGhostStates]
    for i in ghosts:
        if newScaredTimes[0] > 0 and manhattanDistance(i, newPos) <=4:
            return 9999
    for i in ghosts:
        if manhattanDistance(i, newPos) <=4 and newScaredTimes[0] <= 0 :
            return -999999
    if newPos in currentGameState.getFood().asList() or newPos in currentGameState.getCapsules():
            return 9999

    foods=0
    for i in newFood.asList():
        foods+=1/manhattanDistance(i, newPos)*0.7
    for i in currentGameState.getCapsules():
        foods+=1/manhattanDistance(i, newPos)
    ghost=0
    for i in ghosts:
        ghost+=1/manhattanDistance(i, newPos)
    if newScaredTimes[0] <= 19:
        return  foods-len(newFood.asList())-ghost*2*random.uniform(1,1.03) +currentGameState.getScore()
    else:
        return  foods-len(newFood.asList())+ghost*90+currentGameState.getScore()*1.0591




# Abbreviation
better = betterEvaluationFunction
