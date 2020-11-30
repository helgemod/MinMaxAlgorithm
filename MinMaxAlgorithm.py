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
#   Suggestion: Put breakpoint in "minimaxer"-method and step through to understand
#   how the algorithm works.
#

"""
import logging
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s=> %(message)s')
#logging.basicConfig(filename="MinMaxLog.txt",filemode='w+',level=logging.DEBUG, format='%(levelname)s=> %(message)s')
logging.basicConfig(level=logging.INFO, format='%(levelname)s=> %(message)s')
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

MINMAX_ALGO = 1
MINMAXALPHABETAPRUNING_ALGO = 2
MINMAX_ALGO_WITH_LOGGING = -1

KEY_EVAL = "MinMaxAlgo_keyEval"
KEY_BESTMOVE = "MinMaxAlgo_keyBestMove"

class GameAlgo:

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

    def __init__(self, evalFunc_callback,
                 maximizerMoveFunc_callback,
                 minimizerMoveFunc_callback,
                 maximizerUndoMoveFunc_callback,
                 minimizerUndoMoveFunc_callback,
                 getListOfPossibleMovesAsMaximizer_callback,
                 getListOfPossibleMovesAsMinimizer_callback,
                 minEval=-100, maxEval=100, depth=6):

        self.evalFunc_callback = evalFunc_callback
        self.maximizerMoveFunc_callback = maximizerMoveFunc_callback
        self.minimizerMoveFunc_callback = minimizerMoveFunc_callback
        self.maximizerUndoMoveFunc_callback = maximizerUndoMoveFunc_callback
        self.minimizerUndoMoveFunc_callback = minimizerUndoMoveFunc_callback
        self.getListOfPossibleMovesAsMaximizer_callback = getListOfPossibleMovesAsMaximizer_callback
        self.getListOfPossibleMovesAsMinimizer_callback = getListOfPossibleMovesAsMinimizer_callback
        self.MIN_EVAL = minEval
        self.MAX_EVAL = maxEval
        self.DEPTH = depth

    def calculateMove(self, whichAlgo, maximizingPlayer, depth):
        if whichAlgo == MINMAX_ALGO:
            myMove = self.minimax(depth, maximizingPlayer)
        elif whichAlgo == MINMAXALPHABETAPRUNING_ALGO:
            myMove = self.minMaxAlphaBetaPruning(depth, maximizingPlayer, self.MIN_EVAL, self.MAX_EVAL)
        elif whichAlgo == MINMAX_ALGO_WITH_LOGGING:
            myMove = self.minimaxWithLogging(depth, maximizingPlayer)
        else:
            myMove = self.minimax(self.DEPTH, maximizingPlayer)
        return myMove[KEY_BESTMOVE]

    #This code is clean school book example
    def minimax(self, depth, maximizingPlayer):
        if maximizingPlayer:
            moveList = self.getListOfPossibleMovesAsMaximizer_callback()
        else:
            moveList = self.getListOfPossibleMovesAsMinimizer_callback()

        if depth == 0 or len(moveList) == 0:
            bottomEval = self.evalFunc_callback()
            return {KEY_EVAL: bottomEval, KEY_BESTMOVE: None}

        if maximizingPlayer:
            evalMaxResult = {KEY_EVAL: self.MIN_EVAL, KEY_BESTMOVE: None}
            for move in moveList:

                #Try a move
                self.maximizerMoveFunc_callback(move)

                # RECUR
                evalResult = self.minimax(depth-1, False)

                #Remove token before next loop
                self.maximizerUndoMoveFunc_callback(move)

                # Is this move better?
                if evalResult[KEY_EVAL] > evalMaxResult[KEY_EVAL]:
                    evalMaxResult[KEY_EVAL] = evalResult[KEY_EVAL]
                    evalMaxResult[KEY_BESTMOVE] = move
            return evalMaxResult

        #Minimizer
        else:
            evalMinResult = {KEY_EVAL: self.MAX_EVAL, KEY_BESTMOVE: None}
            for move in moveList:

                # Try a move
                self.minimizerMoveFunc_callback(move)

                # RECUR
                evalResult = self.minimax(depth - 1, True)

                # Remove token before next loop
                self.minimizerUndoMoveFunc_callback(move)

                # Is this move better?
                if evalResult[KEY_EVAL] < evalMinResult[KEY_EVAL]:
                    evalMinResult[KEY_EVAL] = evalResult[KEY_EVAL]
                    evalMinResult[KEY_BESTMOVE] = move
            return evalMinResult

    #This code is with logging for better understanding while analyzing
    #afterward.
    def minimaxWithLogging(self, depth, maximizingPlayer,nn=None):
        maxMinInfo = "(MAX)"
        ident = 3
        if not maximizingPlayer:
            maxMinInfo = "(MIN)"
        if nn == None:
            nn = "ROOT"

        if maximizingPlayer:
            moveList = self.getListOfPossibleMovesAsMaximizer_callback()
        else:
            moveList = self.getListOfPossibleMovesAsMinimizer_callback()

        if depth == 0 or len(moveList) == 0:
            bottomEval = self.evalFunc_callback()
            logging.info("-" *((self.DEPTH-depth)*ident) + maxMinInfo + nn+" ***BOTTOM*** Evaluated to:"+str(bottomEval))
            return {KEY_EVAL: bottomEval, KEY_BESTMOVE: None}

        logging.info("-" * ((self.DEPTH - depth) * ident) + maxMinInfo + nn)

        if maximizingPlayer:
            evalMaxResult = {KEY_EVAL: self.MIN_EVAL, KEY_BESTMOVE: None}
            for move in moveList:

                #Try a move
                self.maximizerMoveFunc_callback(move)

                # RECUR
                evalResult = self.minimaxWithLogging(depth-1, False, nn+"/"+str(move))

                #Remove token before next loop
                self.maximizerUndoMoveFunc_callback(move)

                # Is this move better?
                if evalResult[KEY_EVAL] > evalMaxResult[KEY_EVAL]:
                    evalMaxResult[KEY_EVAL] = evalResult[KEY_EVAL]
                    evalMaxResult[KEY_BESTMOVE] = move
                    logging.info("-" * ((self.DEPTH - depth) * ident) + maxMinInfo + nn + " ...better move:"+str(move))
            logging.info("-" * ((self.DEPTH - depth) * ident) + maxMinInfo + nn + " *BEST MOVE:" + str(evalMaxResult[KEY_BESTMOVE]))
            return evalMaxResult

        #Minimizer
        else:
            evalMinResult = {KEY_EVAL: self.MAX_EVAL, KEY_BESTMOVE: None}
            for move in moveList:

                # Try a move
                self.minimizerMoveFunc_callback(move)

                # RECUR
                evalResult = self.minimaxWithLogging(depth - 1, True, nn+"/"+str(move))

                # Remove token before next loop
                self.minimizerUndoMoveFunc_callback(move)

                # Is this move better?
                if evalResult[KEY_EVAL] < evalMinResult[KEY_EVAL]:
                    evalMinResult[KEY_EVAL] = evalResult[KEY_EVAL]
                    evalMinResult[KEY_BESTMOVE] = move
                    logging.info("-" * ((self.DEPTH - depth) * ident) + maxMinInfo + nn + " ...better move:" + str(move))
            logging.info("-" * ((self.DEPTH - depth) * ident) + maxMinInfo + nn + " *BEST MOVE:" + str(evalMinResult[KEY_BESTMOVE]))
            return evalMinResult

    def minMaxAlphaBetaPruning(self, depth, maximizingPlayer, alpha, beta, nn=None):
        if nn is None:
            nn="R "
        if depth == 0:
            #We're at the bottom node! Evaluate this node and return it up the tree.
            bottomEval = self.evalFunc_callback()
            return {KEY_EVAL: bottomEval, KEY_BESTMOVE: None}

        #Don't need to read out list if depth == 0!!
        if maximizingPlayer:
            moveList = self.getListOfPossibleMovesAsMaximizer_callback()
        else:
            moveList = self.getListOfPossibleMovesAsMinimizer_callback()
        #print(str(nn)+": "+str(moveList))
        if len(moveList) == 0:
            #I can't do any moves! (Probably board is full, if Tic Tac Toe.) Eval and call up.
            bottomEval = self.evalFunc_callback()
            #print("Eval, due to no movelist:",bottomEval, nn)
            return {KEY_EVAL: bottomEval, KEY_BESTMOVE: None}

        if maximizingPlayer:
            evalMaxResult = {KEY_EVAL: self.MIN_EVAL, KEY_BESTMOVE: moveList[0]}
            for move in moveList:

                if nn == "R ":
                    pass
                    #print("Trying move",move)

                #Try a move
                self.maximizerMoveFunc_callback(move)

                # RECUR
                evalResult = self.minMaxAlphaBetaPruning(depth-1, False, alpha, beta, nn+" "+str(move))

                #Remove token before next loop
                self.maximizerUndoMoveFunc_callback(move)

                # Is this move better?
                if evalResult[KEY_EVAL] > evalMaxResult[KEY_EVAL]:
                    evalMaxResult[KEY_EVAL] = evalResult[KEY_EVAL]
                    evalMaxResult[KEY_BESTMOVE] = move

                #Is this move the best I know so far?
                if evalMaxResult[KEY_EVAL] > alpha:
                    alpha = evalMaxResult[KEY_EVAL]

                # Minimizer above me knows he can achieve "beta".
                # "alpha" is what I as maximizer AT LEAST will
                # throw back up at him. So, if minimizer above
                # me has found a better move (beta<=alpha), he will NOT pick
                # this branch anyway. So stop investigating further!
                if beta <= alpha:
                    #print("MAX> PRUNE:",nn)
                    break

            return evalMaxResult

        #Minimizer
        else:
            evalMinResult = {KEY_EVAL: self.MAX_EVAL, KEY_BESTMOVE: moveList[0]}
            for move in moveList:
                if nn == "R ":
                    pass
                    #print("Trying move", move)
                # Try a move
                self.minimizerMoveFunc_callback(move)

                # RECUR
                evalResult = self.minMaxAlphaBetaPruning(depth - 1, True, alpha, beta, nn+str(move))

                if nn == "R " and evalResult == 1000:
                    print("Forced win for X if I draw: ",move)

                # Remove token before next loop
                self.minimizerUndoMoveFunc_callback(move)

                # Is this move better?
                if evalResult[KEY_EVAL] < evalMinResult[KEY_EVAL]:
                    evalMinResult[KEY_EVAL] = evalResult[KEY_EVAL]
                    evalMinResult[KEY_BESTMOVE] = move
                    if nn == "R ":
                        pass
                        #print("Best move for O so far:", evalMinResult[KEY_BESTMOVE], evalMinResult[KEY_EVAL])

                if evalMinResult[KEY_EVAL] < beta:
                    evalMinResult[KEY_EVAL] = evalResult[KEY_EVAL]
                    beta = evalMinResult[KEY_EVAL]
                    if nn == "R ":
                        pass
                        #print("...also updating beta to:", beta)

                # Maximizer above me knows he can achieve "alpha".
                # "beta" is what I as minimizer AT LEAST will
                # throw back up at him. So, if maximizer above
                # me has found a better move (beta<=alpha), he will NOT pick
                # this branch anyway. So stop investigating further!
                if beta <= alpha:
                    if nn == "R ":
                        print("...PRUNE! Got better moves to make!:")
                    #print("MIN> PRUNE:", nn)
                    break

            return evalMinResult


if __name__ == '__main__':
    print("MinMaxAlgo run from a commandprompt. Not yet implemented.")
