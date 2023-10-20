
class Square:

    COL_LABELS = {0: 'a', 1: 'b', 2: 'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.col_labels = self.COL_LABELS[col]

    def has_piece(self):
        return self.piece != None
    
    def is_empty(self):
        return self.piece == None
    
    def has_enemy_piece(self, colour):
        return self.has_piece() and self.piece.colour != colour
    
    def has_team_piece(self, colour):
        return self.has_piece() and self.piece.colour == colour
    
    def is_empty_or_enemy(self, colour):
        return self.is_empty() or self.has_enemy_piece(colour)


    @staticmethod
    def in_range(*args):
        '''
            Checks if a given set of positions are on the board
            returns False if any position is off the board
            returns True otherwise
        '''
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        
        return True
    
    @staticmethod
    def get_label_col(col):
        COL_LABELS = {0: 'a', 1: 'b', 2: 'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
        return COL_LABELS[col]


    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col