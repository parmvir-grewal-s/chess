from constants import *
from square import Square
from piece import *
from move import Move
class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        piece.moved = True

        # now that we've calculated moves and have moved, reset list of valid moves
        piece.clear_moves()

        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def calc_moves(self, piece, row, col):
        '''
            Calculates all valid moves a given piece can make
        '''

        def pawn_moves():
            steps = 1 if piece.moved else 2

            # vertical moves 

            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))

            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if not self.squares[possible_move_row][col].has_piece():
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        move = Move(initial, final)
                        piece.add_move(move)
                    else:
                        break
                else:
                    break
            
            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.colour):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def knight_moves():
            possible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1)
            ]
            
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_enemy(piece.colour):
                        # create squares of the move before and after
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create the new move
                        move = Move(initial, final)
                        # append new move
                        piece.add_move(move)
                
        def straight_line_moves(increments):
            for incr in increments:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        if not self.squares[possible_move_row][possible_move_col].has_piece():
                            piece.add_move(move)
                    
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.colour):
                            piece.add_move(move)
                            break
                        
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.colour):
                            break
                    
                    else: break

                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjacents = [
                (row - 1, col - 1), # up left
                (row - 1, col), # up
                (row - 1, col + 1), # up right
                (row, col + 1), # right
                (row + 1, col + 1), # down right
                (row + 1, col), # down
                (row + 1, col - 1), # down left
                (row, col - 1) # left
            ]
            
            # normal moves
            for possible_move in adjacents:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_enemy(piece.colour):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)
                    
            # castling moves

            # queen-side castling

            # king-side castling



        # is the piece being checked a pawn
        if isinstance(piece, Pawn): pawn_moves()
        elif isinstance(piece, Knight): knight_moves()
        elif isinstance(piece, Bishop):
            straight_line_moves([
                (-1, 1), # up right
                (-1, -1), # up left
                (1, 1), # down right
                (1, -1) # down left
            ])
        elif isinstance(piece, Rook):
            straight_line_moves([
                (-1, 0), # up
                (1, 0), # down
                (0, -1), # left
                (0, 1) # right
            ])
        elif isinstance(piece, Queen):
            straight_line_moves([
                (-1, 1), # up right
                (-1, -1), # up left
                (1, 1), # down right
                (1, -1), # down left
                (-1, 0), # up
                (1, 0), # down
                (0, -1), # left
                (0, 1) # right
            ])
        elif isinstance(piece, King): king_moves()

    # Private methods have an underscore prefix

    # Creates the starting point for the chessboard
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, colour):
        row_pawn, row_other = (6, 7) if colour == 'white' else (1, 0)

        # Add all the pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(colour))
        
        # Add the knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(colour))
        self.squares[row_other][6] = Square(row_other, 6, Knight(colour))

        # Add the bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(colour))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(colour))

        # Add the rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(colour))
        self.squares[row_other][7] = Square(row_other, 7, Rook(colour))

        # Add the queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(colour))

        # Add the king
        self.squares[row_other][4] = Square(row_other, 4, King(colour))
