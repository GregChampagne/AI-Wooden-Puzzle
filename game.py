# Authors: Greg Robson
# 000919616
# Version 3-26-18 v0.03

"""
CURRENT PLANS:
1. Learn how to github with this fully
2. Show the physical pieces remaining
3. Better placement method?
4. Start developing the AI functionality
5. Hone the AI until it is near unbeatable
6. Find a compromise between time and power
7. Graphics?
"""


import random
from Piece import *


# Runs the game for a human to play it
def main():
    print("")


class Game:

    def __init__(self):
        self.board = [[0] * 10 for i in range(10)]
        self.score = 0
        self.first = Piece(random.randint(0, 18))
        self.second = Piece(random.randint(0, 18))
        self.third = Piece(random.randint(0, 18))

    def __str__(self):
        # Score printout
        print("CURRENT SCORE: " + str(self.score))

        # The table creation and print out
        # Asterisks denote an end border, |'s a in table border
        rows = []
        print("  * 0 * 1 * 2 * 3 * 4 * 5 * 6 * 7 * 8 * 9")
        for i in range(0, 10):
            rows.append(str(i) + " * ")
            for j in range(0, 10):
                out = " "
                if self.board[i][j] == 1:
                    out = "X"
                rows[i] += str(out + " | ")
            print(rows[i])

        print_options(self.first.coords, self.second.coords, self.third.coords)
        return ""

    def new_board(self, coords, the_board, test):
        count = 0
        full_rows = []
        full_cols = []

        # Sets the piece on the board
        for i in range(0, len(coords)):
            # print(coords[i][0], coords[i][1])
            the_board[coords[i][0]][coords[i][1]] = 1
            count += 1

        # Checks all of the rows for a full row
        for j in range(0, 10):
            row = 0
            for k in range(0, 10):
                if the_board[j][k] == 1:
                    row += 1
            if row == 10:
                full_rows.append(j)

        # Checks all of the columns for a full column
        for m in range(0, 10):
            col = 0
            for n in range(0, 10):
                if the_board[n][m] == 1:
                    col += 1
            if col == 10:
                full_cols.append(m)

        # Clears all of the full rows
        for y in range(0, len(full_rows)):
            for z in range(0, 10):
                the_board[full_rows[y]][z] = 0
            count += 10

        # Clears all of the full columns
        for v in range(0, len(full_cols)):
            for w in range(0, 10):
                the_board[w][full_cols[v]] = 0
            count += 10

        # If testing boards, returns the resulting board
        if test:
            return the_board
        # Else, it sets the board to its new state
        else:
            self.score += count
            self.board = the_board

    # Checks the validity of a placement, and if not a test, will place the piece
    def placement_check(self, x, y, choice, state, test):
        # Finds the piece based on the choice
        if int(choice) == 1:
            piece = self.first
        elif int(choice) == 2:
            piece = self.second
        else:
            piece = self.third
        coordinates = piece.coords
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
                    if state[coordinates[i][0]][coordinates[i][1]] == 1:
                        legal = False
                except:
                    legal = False

        if test or not legal:
            for i in range(0, len(coordinates)):
                coordinates[i] = [coordinates[i][0] - x, coordinates[i][1] - y]

        # Assuming that the choice has been found to be legal, the piece is emptied,
        # and a new_board is then called to place that piece onto the board
        if choice == 1 and legal and not test:
            self.first.empty()
            self.new_board(coordinates, self.board, test)
        elif choice == 2 and legal and not test:
            self.second.empty()
            self.new_board(coordinates, self.board, test)
        elif legal and not test:
            self.third.empty()
            self.new_board(coordinates, self.board, test)

        # Whether the piece was placed or not, legal will be returned to the calling method
        return legal

    def pieces_left(self):
        return self.first.is_empty() + self.second.is_empty() + self.third.is_empty()

    def pieces(self):
        left = []
        if not self.first.is_empty():
            left.append(1)
        if not self.first.is_empty():
            left.append(2)
        if not self.first.is_empty():
            left.append(3)

        return left

    def refresh_pieces(self):
        self.first = Piece(random.randint(0, 18))
        self.second = Piece(random.randint(0, 18))
        self.third = Piece(random.randint(0, 18))


def print_options(a, b, c):
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
