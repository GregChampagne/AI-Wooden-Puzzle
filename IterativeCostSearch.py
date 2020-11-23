from pq import *
from Piece import *
import random
from copy import *


def main():
    s = IterativeCostSearchWoodenBlock(20, 1)
    go = int(input("Please anything but -1 to continue"))
    while go != -1:
        s = IterativeCostSearchWoodenBlock(20, 1)
        go = int(input("Please anything but -1 to continue"))


class UtilityNode:
    """
    Adapted from code by Peter Norvig
    A class for general purpose informed node. Contains information
    on node's state, parent, operator, and depth. Each node has an
    associated utility based on the state class' heuristic
    """
    def __init__(self, state, parent, operator, depth):
        self.state = state
        self.parent = parent
        self.operator = operator
        self.depth = depth
    def priority(self):
        """
        Needed to determine where the node should be placed in the
        priority queue.  
        """
        return self.state.heuristic()

class IterativeCostSearchWoodenBlock():
    """
    Adapted from code by Peter Norvig
    An informed search class that uses a priority queue and
    traverses a search tree containing instances of the UtilityNode
    class. Specific to wooden block puzzle. Only expands a node
    if it has a certain utility, if no node meets cutoff then cutoff
    is lowered and nodes reevaluated. As an argument, takes initial
    cutoff and the amount to decrement cutoff when unsucessful. Search
    is episodic in sense that every series of three placements is
    treated as a new problem
    """
    def __init__(self, initialCutOff, decrement):
        self.initialCutOff = initialCutOff
        self.cutOff = initialCutOff
        self.decrement = decrement
        # Score list keeps track of score progression, so that it can
        # be accessed once search is complete
        self.scoreList = []
        # Creates an instance of wooden block game with empty board and
        # three random pieces
        initialState = WoodenBlockState([[0] * 10 for i in range(10)],
                                        Piece(random.randint(0, 18)),
                                        Piece(random.randint(0, 18)),
                                        Piece(random.randint(0, 18)), 0, 0)
        print(str(initialState))
        # Searches for solution until no available moves left, prints
        # board after every three placements. Updates scoreList
        solution = self.search(initialState)
        while(solution != None):
            self.scoreList.append(solution.state.score)
            currentState = WoodenBlockState(solution.state.boardState,
                                        Piece(random.randint(0, 18)),
                                        Piece(random.randint(0, 18)),
                                        Piece(random.randint(0, 18)),
                                        solution.state.score, 0)
            print(str(currentState))
            solution = self.search(currentState)
        if not self.deadEndNodes.empty():
            solution = self.deadEndNodes.dequeue()
            print(str(solution.state))
            self.scoreList.append(solution.state.score)
    def search(self, gameState):
        """
        Explores all possible nodes based on current game state and
        expands nodes that meet utility cutoff. Returns a solution
        node of depth 3.
        """
        # Creates priority queue and adds node with current game state
        # and resets cutOff to initial value
        q = PriorityQueue()
        q.enqueue(UtilityNode(gameState, None, None, 0))
        # deadEndNodes is a queue of nodes that are not a solution, but
        # have no legal moves possible
        self.deadEndNodes = PriorityQueue()
        # Evaluates all nodes in queue until it is empty
        while not q.empty():
            self.cutOff = self.initialCutOff
            validStateFound = False
            negativeCutOffFlag = False
            current = q.dequeue()
            # If at depth three then three placements have been made and current node is solution
            if current.depth == 3:
                self.showPath(current)
                return current
            else:
                successors = []
                # If no moves are legal then add node to deadEndNodes queue
                if(len(current.state.legalPlacements) == 0):
                    self.deadEndNodes.enqueue(current)
                # Makes every legal placement, generating new game states and collecting all game states
                for i in range(len(current.state.legalPlacements)):
                    successors.append(current.state.makePlacement(current.state.boardState,
                                                                  current.state.legalPlacements[i][0],
                                                                  current.state.legalPlacements[i][2],
                                                                  current.state.legalPlacements[i][3]))
                # If new game state has utility above cutoff then that state is added to queue
                # and a valid state has been found. Else, decrement cutoff and reevaluate all
                # states. If cutoff becomes negative then stops evaluating states
                while not (validStateFound or negativeCutOffFlag):
                    for i in range(len(successors)):
                        if successors[i].heuristic() > self.cutOff:
                            n = UtilityNode(successors[i],
                                             current,
                                             str(current.state.legalPlacements[i][1:]),
                                             current.depth+1)
                            q.enqueue(n)
                            validStateFound = True
                    self.cutOff -= self.decrement
                    if self.cutOff < 0:
                        negativeCutOffFlag = True
                        
                    
    def showPath(self, node):
        """
        Uses the buildPath function to print out the operators
        needed to reach current state
        """
        path = self.buildPath(node)        
        for current in path:
            if current.depth != 0:
                print("Operator:", current.operator)
    def buildPath(self, node):
        """
        Beginning at the goal node, follow the parent links back
        to the start state.  Create a list of the states traveled
        through during the search from start to finish.
        """
        result = []
        while node != None:
            result.insert(0, node)
            node = node.parent
        return result

class WoodenBlockState():
    """ 
    Implements the the wooden block puzzle game involving a 10x10
    board and three avaiable pieces to place on board. The state
    stores information of the board state, the pieces available to
    place and the score of the game.
    """
    def __init__(self, boardState, piece1, piece2, piece3, score, scoreDifferential):
        """
        boardState is a 10x10 list where each index refers to a tile.
        Occupied tiles are denoted with a 1 and blank tiles with a 0.
        pieces is a list containing the three piece objects.
        score is an integer.
        """
        self.boardState = boardState
        self.pieces = [piece1, piece2, piece3]
        self.score = score
        self.scoreDifferential = scoreDifferential
        self.legalPlacements = []
        self.holes = 0
        self.holeScore = 0
        self.clearedScore = 0
        # Checks placement of every piece on every tile and collects all legal placements
        # along with checking how 'holey' the board is
        for piece in range(len(self.pieces)):
            for x in range(10):
                for y in range(10):
                    if self.legal(self.boardState, self.pieces[piece], x, y):
                        self.legalPlacements.append([self.pieces[piece],"Piece " + str(piece+1),x,y,])
                    if x < 9 and y < 9:
                        if self.boardState[x][y] == 0 and self.boardState[x+1][y] == 1 and self.boardState[x-1][y] == 1 and self.boardState[x][y+1] == 1 and self.boardState[x][y-1] == 1:
                            self.holeScore -= 1
                    if x < 8 and y < 8:
                        if self.boardState[x][y] == 0 and self.boardState[x+2][y] == 1 and self.boardState[x-2][y] == 1 and self.boardState[x][y+2] == 1 and self.boardState[x][y-2] == 1:
                            self.holeScore -= 1

        for i in range(0, 10):
            for j in range(0, 10):
                borders = 0
                if self.boardState[i][j] == 0:
                    if i == 0:
                        borders += 1
                    elif self.boardState[i - 1][j] == 1:
                        borders += 1

                    if i == 9:
                        borders += 1
                    elif self.boardState[i + 1][j] == 1:
                        borders += 1

                    if j == 0:
                        borders += 1
                    elif self.boardState[i][j - 1] == 1:
                        borders += 1

                    if j == 9:
                        borders += 1
                    elif self.boardState[i][j + 1] == 1:
                        borders += 1

                    if borders == 4:
                        self.holes += 1

        # While loop that goes through the grid looking to see if a 5
        # down piece can be played. If it can, that is noted and the loop stops
        # if not, it takes note of the longest straight down piece that is viable
        # to be played.
        left = True
        x = 0
        y = 0
        current = 0
        self.longestDown = 1
        while self.longestDown != 5 and left:
            if self.boardState[x][y] == 0:
                current += 1
                if current > self.longestDown:
                    self.longestDown = current
            else:
                current = 0
            y += 1
            if y > 9:
                y = 0
                x += 1
            if x > 9:
                left = False

        # This while loop does the exact same thing, just with accross moves
        # instead of down moves.
        left = True
        x = 0
        y = 0
        current = 0
        self.longestCross = 1
        while self.longestCross != 5 and left:
            if self.boardState[x][y] == 0:
                current += 1
                if current > self.longestCross:
                    self.longestCross = current
            else:
                current = 0
            x += 1
            if x > 9:
                x = 0
                y += 1
            if y > 9:
                left = False

        # Finds the number of unique places within the grid where a 3x3
        # block could be placed.
        self.grids = 0
        space = 0
        for x in range(0, 8):
            for y in range(0, 8):
                for a in range(0, 3):
                    for b in range(0, 3):
                        space += self.boardState[x + a][y + b]
                if space == 0:
                    self.grids += 1
            
                    
                        
                    
                
                
    def __str__(self):
        """
        Returns a string representation of the state.
        Prints out full board and score. Uses printPiece
        function to print out the piece objects
        """
        print("CURRENT SCORE: " + str(self.score))
        # The table creation and print out
        # Asterisks denote an end border, |'s a in table border
        rows = []
        print("  * 0 * 1 * 2 * 3 * 4 * 5 * 6 * 7 * 8 * 9")
        for i in range(0, 10):
            rows.append(str(i) + " * ")
            for j in range(0, 10):
                out = " "
                if self.boardState[i][j] == 1:
                    out = "X"
                rows[i] += str(out + " | ")
            print(rows[i])
        printPiece(self.pieces[0], self.pieces[1], self.pieces[2])
        return "\n"
    def legal(self, boardState, piece, x, y):
        """
        Tests whether the move is illegal given a piece, the board state,
        and the (x,y) coordinates of the tile to place the piece
        """
        # If there is no piece to move, then the move is illegal
        if piece == 0:
            return False
        coordinates = deepcopy(piece.coords)
        # Changes every value of the piece type into the proper coordinates
        # and checks to make sure that they are legal coordinates
        legal = True
        for i in range(0, len(coordinates)):
            coordinates[i] = [coordinates[i][0] + x, coordinates[i][1] + y]
            if coordinates[i][1] > 9 or coordinates[i][0] > 9:
                legal = False
            if coordinates[i][1] < 0 or coordinates[i][0] < 0:
                legal = False
        if legal:
            for i in range(0, len(coordinates)):
                try:
                    if boardState[coordinates[i][0]][coordinates[i][1]] == 1:
                        legal = False
                except:
                    legal = False
        return legal

    def makePlacement(self, boardState, piece, x, y):
        """
        Places a piece in an (x,y) coordinate tile and generates
        a new board state with that placement. Updates score based
        on placement. If a row is filled then it is emptied and 10
        is added to score
        """
        coordinates = deepcopy(piece.coords)
        score = self.score 
        newBoardState = deepcopy(boardState)
        # Shifts coordinates of piece and makes placement. Stores index of
        # piece in piece list. 
        for i in range(0, len(coordinates)):
            coordinates[i] = [coordinates[i][0] + x, coordinates[i][1] + y]
        for i in range(0, len(coordinates)):
            newBoardState[coordinates[i][0]][coordinates[i][1]] = 1
            score += 1
        index = self.pieces.index(piece)
        # Checks for full rows or columns and if any empties them
        for row in range(0, 10):
            count = 0
            for i in range(0, 10):
                if newBoardState[row][i] == 1:
                    count += 1
            if count == 10:
                for j in range(0, 10):
                    newBoardState[row][j] = 0
                    score += 1
                self.clearedScore += 1
        for col in range(0, 10):
            count = 0
            for i in range(0, 10):
                if newBoardState[i][col] == 1:
                    count += 1
            if count == 10:
                for j in range(0, 10):
                    newBoardState[j][col] = 0
                    score += 1
                self.clearedScore += 1
        # Generates new state with the updated board and the piece that
        # was used removed from available pieces
        if index == 0:
            return WoodenBlockState(newBoardState, 0, self.pieces[1], self.pieces[2], score, score - self.score)
        if index == 1:
            return WoodenBlockState(newBoardState, self.pieces[0], 0, self.pieces[2], score, score - self.score)
        if index == 2:
            return WoodenBlockState(newBoardState, self.pieces[0], self.pieces[1], 0, score, score - self.score)

    def heuristic(self):
            """
            Returns the estimated utility of a node, based on a
            number of different features. 
            """
            # Looks at every tile on board to determine number of legal placements
            # left and how 'holey' the board is

            long_x = 2 ^ self.longestCross
            long_y = 2 ^ self.longestDown

            return 1000 + 25 * self.clearedScore + long_x + long_y + 9 * self.grids - 50 * self.holes

def printPiece(a, b, c):
    """
    Prints three piece objects in an easily readable format given.
    If the piece is equal to 0, then that means that piece slot is
    empty, so nothing is printed.
    """
    if a != 0:
        a = a.coords
    else:
        a = []
    if b != 0:
        b = b.coords
    else:
        b = []
    if c != 0:
        c = c.coords
    else:
        c = []
    for i in range(0, 5):
        vals = []
        row = " "
        for j in range(0, 15):
            vals.append(0)
        for j in range(0, 5):
            for k in range(0, len(a)):
                if a[k] == [i, j]:
                    vals[j] = 1
        for j in range(0, 5):
            for k in range(0, len(b)):
                if b[k] == [i, j]:
                    vals[j + 5] = 1
        for j in range(0, 5):
            for k in range(0, len(c)):
                if c[k] == [i, j]:
                    vals[j + 10] = 1
        for j in range(0, len(vals)):
            if j % 5 == 0:
                row += " |"
            if vals[j] == 0:
                row += "  "
            else:
                row += " X"

        row += " |"

        print(row)

main()
