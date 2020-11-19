#!/usr/bin/env python

"""
# MinMaxAlgorithm is the standard "Minimax" or "Min Max" algorithm.
#
# The purpose of this is:
#   1) Implement the algorithm in a generic way.
#   2) For demo purpose. Hopefully its is clean and easy to understand
#      how it works.
#   3) To use in conjunctions with "StrideDimension"-module.
#       www.github.com/helgemod/Stridedimensions
#
# Usage:
#
#   Create an object of class MinMaxAlgo with the proper callback functions.
#   The reason for callback functions is to make the object generic and reusable
#   for many games using the MinMax-algo
#
# Note:
#   The Min Max algorithm is not optimal for games with many options. Therefore
#   it can be further developed with Alpha-Beta pruning. See other module for
#   this implementation.
#

"""

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s=> %(message)s')
logging.disable(logging.CRITICAL)

__author__ = "Helge Modén, www.github.com/helgemod"
__copyright__ = "Copyright 2020, Helge Modén"
__credits__ = None
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Helge Modén, https://github.com/helgemod/MinMaxAlgorithm"
__email__ = "helgemod@gmail.com"
__status__ = "https://github.com/helgemod/MinMaxAlgorithm"
__date__ = "2020-11-20"



class MinMaxAlgo:

    """
    Explanation of callback functions.
    evalFunc_callback -
        Shall be a function that gives an evaluation for the current position in the game.
        0  => Even
        >0 => Maximum player has advantage
        <0 => Minimum player has advantage
    maximizerMoveFunc_callback - Makes one "move" (as of your definitions given in "getListOfPossi..." below) as
                                 the maximizer player.
    minimizerMoveFunc_callback - As above but for minimizer player.
    maximizerUndoMoveFunc_callback - Take back the "move" done by maximizer player.
    minimizerUndoMoveFunc_callback - " (but for minimizer player)
    getListOfPossibleMovesAsMaximizer_callback - Return a list with currently all possible moves for maximizer player.
    getListOfPossibleMovesAsMinimizer_callback - As above but for mimimizer player.

    """

    evalFunc_callback=None
    maximizerMoveFunc_callback = None
    minimizerMoveFunc_callback = None
    maximizerUndoMoveFunc_callback = None
    minimizerUndoMoveFunc_callback = None
    getListOfPossibleMovesAsMaximizer_callback = None
    getListOfPossibleMovesAsMinimizer_callback = None

    MIN_EVAL = -100
    MAX_EVAL = 100

    DEPTH = 2

    KEY_EVAL = "MinMaxAlgo_keyEval"
    KEY_BESTMOVE = "MinMaxAlgo_keyBestMove"

    def __init__(self, evalFunc_callback, \
                 maximizerMoveFunc_callback,\
                 minimizerMoveFunc_callback, \
                 maximizerUndoMoveFunc_callback, \
                 minimizerUndoMoveFunc_callback, \
                 getListOfPossibleMovesAsMaximizer_callback,\
                 getListOfPossibleMovesAsMinimizer_callback, \
                 minEval, maxEval):

        self.evalFunc_callback=evalFunc_callback
        self.maximizerMoveFunc_callback = maximizerMoveFunc_callback
        self.minimizerMoveFunc_callback = minimizerMoveFunc_callback
        self.maximizerUndoMoveFunc_callback = maximizerUndoMoveFunc_callback
        self.minimizerUndoMoveFunc_callback = minimizerUndoMoveFunc_callback
        self.getListOfPossibleMovesAsMaximizer_callback = getListOfPossibleMovesAsMaximizer_callback
        self.getListOfPossibleMovesAsMinimizer_callback = getListOfPossibleMovesAsMinimizer_callback
        self.MIN_EVAL=minEval
        self.MAX_EVAL=maxEval

    def calculateMove(self,maximizingPlayer):
        myMove = self.minimax(self.DEPTH,maximizingPlayer)
        return myMove[self.KEY_BESTMOVE]

    def minimax(self,depth,maximizingPlayer,loggingNodeName=None):
        if loggingNodeName == None:
            loggingNodeName = "ROOT NODE"

        logging.debug(" "*(self.DEPTH - depth)+loggingNodeName)

        if maximizingPlayer:
            moveList = self.getListOfPossibleMovesAsMaximizer_callback()
        else:
            moveList = self.getListOfPossibleMovesAsMinimizer_callback()

        if depth==0 or len(moveList)==0:
            bottomEval = self.evalFunc_callback()
            return {self.KEY_EVAL:bottomEval, self.KEY_BESTMOVE:None}

        if maximizingPlayer:
            evalMaxResult = {self.KEY_EVAL:self.MIN_EVAL,self.KEY_BESTMOVE:None}
            for move in moveList:

                #Try a move
                self.maximizerMoveFunc_callback(move)

                #For logging
                nn = loggingNodeName+"("+str(move)+")"

                # RECUR
                evalResult = self.minimax(depth-1, False, nn)

                #Remove token before next loop
                self.maximizerUndoMoveFunc_callback(move)

                # Is this move better?
                if evalResult[self.KEY_EVAL] > evalMaxResult[self.KEY_EVAL]:
                    evalMaxResult[self.KEY_EVAL] = evalResult[self.KEY_EVAL]
                    evalMaxResult[self.KEY_BESTMOVE] = move
            return evalMaxResult

        #Minimizer
        else:
            evalMinResult = {self.KEY_EVAL:self.MAX_EVAL,self.KEY_BESTMOVE:None}
            for move in moveList:

                # Try a move
                self.minimizerMoveFunc_callback(move)

                # For logging
                nn = loggingNodeName + "(" + str(move) + ")"

                # RECUR
                evalResult = self.minimax(depth - 1, True, nn)

                # Remove token before next loop
                self.minimizerUndoMoveFunc_callback(move)

                # Is this move better?
                if evalResult[self.KEY_EVAL] < evalMinResult[self.KEY_EVAL]:
                    evalMinResult[self.KEY_EVAL] = evalResult[self.KEY_EVAL]
                    evalMinResult[self.KEY_BESTMOVE] = move
            return evalMinResult

if __name__ == '__main__':
    print("MinMaxAlgo run from a commandprompt. Not yet implemented.")