# Authors: Greg Robson
# 000919616
# Version 3-27-18 v0.03

from game import *


def main():
    p = PuzzleSearch()

    while not p.lost:
        print(p.attempt.__str__())
        abc_boards = []  # Order number 1
        acb_boards = []  # Order number 2
        bac_boards = []  # Order number 3
        bca_boards = []  # Order number 4
        cab_boards = []  # Order number 5
        cba_boards = []  # Order number 6
        max_score = -1000
        order = -1

        # Find all boards with placing A first
        boards_a = p.find_moves(1, p.attempt.board)
        for i in range(0, len(boards_a)):
            boards_ab = p.find_moves(2, boards_a[i])
            for j in range(0, len(boards_ab)):
                boards_abc = p.find_moves(3, boards_ab[j])
                abc_boards.append(boards_abc)

            boards_ac = p.find_moves(3, boards_a[i])
            for j in range(0, len(boards_ac)):
                boards_acb = p.find_moves(3, boards_ac[j])
                acb_boards.append(boards_acb)

        # Find all boards with placing B first
        boards_b = p.find_moves(2, p.attempt.board)
        for i in range(0, len(boards_b)):
            boards_ba = p.find_moves(1, boards_b[i])
            for j in range(0, len(boards_ba)):
                boards_bac = p.find_moves(3, boards_ba[j])
                bac_boards.append(boards_bac)

            boards_bc = p.find_moves(3, boards_b[i])
            for j in range(0, len(boards_bc)):
                boards_bca = p.find_moves(1, boards_bc[j])
                bca_boards.append(boards_bca)

        # Find all boards with placing C first
        boards_c = p.find_moves(3, p.attempt.board)
        for i in range(0, len(boards_c)):
            boards_ca = p.find_moves(1, boards_c[i])
            for j in range(0, len(boards_ca)):
                boards_cab = p.find_moves(2, boards_ca[j])
                cab_boards.append(boards_cab)

            boards_cb = p.find_moves(2, boards_c[i])
            for j in range(0, len(boards_cb)):
                boards_cba = p.find_moves(1, boards_cb[j])
                cba_boards.append(boards_cba)

        for i in range(0, len(abc_boards)):
            score = p.score_board(abc_boards[i])
            if score > max_score:
                order = 1
                max_score = score
                index = i

        for i in range(0, len(acb_boards)):
            score = p.score_board(acb_boards[i])
            if score > max_score:
                order = 2
                max_score = score
                index = i

        for i in range(0, len(bac_boards)):
            score = p.score_board(bac_boards[i])
            if score > max_score:
                order = 3
                max_score = score
                index = i

        for i in range(0, len(bca_boards)):
            score = p.score_board(bca_boards[i])
            if score > max_score:
                order = 4
                max_score = score
                index = i

        for i in range(0, len(cab_boards)):
            score = p.score_board(cab_boards[i])
            if score > max_score:
                order = 5
                max_score = score
                index = i

        for i in range(0, len(cba_boards)):
            score = p.score_board(cba_boards[i])
            if score > max_score:
                order = 6
                max_score = score
                index = i

        if order == -1:
            p.lost = True
        else:
            if order == 1:
                p.set_board(abc_boards[index])
            elif order == 2:
                p.set_board(acb_boards[index])
            elif order == 3:
                p.set_board(bac_boards[index])
            elif order == 4:
                p.set_board(bca_boards[index])
            elif order == 5:
                p.set_board(cab_boards[index])
            else:
                p.set_board(cba_boards[index])

        if not p.lost:
            p.attempt.refresh_pieces()


class PuzzleSearch:

    def __init__(self):
        self.attempt = Game()
        self.lost = False

    def find_moves(self, choice, state):
        boards = []
        if int(choice) == 1:
            piece = self.attempt.first
        elif int(choice) == 2:
            piece = self.attempt.second
        else:
            piece = self.attempt.third
        for j in range(0, 10):
            for k in range(0, 10):
                 if int(state[j][k]) == 0:
                    if self.attempt.placement_check(j, k, choice, state, True):
                        piece.coords = self.coords_shift(j, k, choice)
                        boards.append(self.attempt.new_board(piece.coords, state, True))
                        piece.coords = self.coords_shift(-j, -k, choice)

        return boards

    def score_board(self, state):
        return 0

    def coords_shift(self, x, y, choice):
        if int(choice) == 1:
            piece = self.attempt.first
        elif int(choice) == 2:
            piece = self.attempt.second
        else:
            piece = self.attempt.third

        # print(piece.coords, x, y)
        for i in range(0, len(piece.coords)):
            piece.coords[i] = [piece.coords[i][0] + x, piece.coords[i][1] + y]

        # print(piece.coords, x, y)
        return piece.coords

    def set_board(self, state):
        # First, find the score differential
        score = 0
        old_board = 0
        new_board = 0
        for i in range(0, len(self.attempt.first.coords)):
            score += 1
        for i in range(0, len(self.attempt.second.coords)):
            score += 1
        for i in range(0, len(self.attempt.third.coords)):
            score += 1

        for i in range(0, 10):
            for j in range(0, 10):
                if self.attempt.board[i][j] == 1:
                    old_board += 1
                if state[i][j] == 1:
                    new_board += 1
        # If there is a differential, that means a row was removed,
        # and this adds that extra row score into the total score
        # for the AI to be that much happier about.
        diff = abs(old_board + score - new_board)
        if diff != 0:
            score += diff

        self.attempt.board = state

main()
