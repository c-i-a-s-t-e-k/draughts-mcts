PLAYER_1 = -1  # Black pieces
PLAYER_2 = 1   # White pieces
EMPTY = 0
KING_1 = -2    # Black king
KING_2 = 2     # White king

class Draughts:
    def __init__(self, player1, player2, board_size=8):
        self.board_size = board_size
        self.board = self.initialize_board()
        self.player1 = player1  # Black pieces (moves from top to bottom)
        self.player2 = player2  # White pieces (moves from bottom to top)
        self.chars = {
            EMPTY: " ", 
            PLAYER_1: "●", 
            PLAYER_2: "○",
            KING_1: "⚪",
            KING_2: "⚫"
        }
        self.current_player = PLAYER_1  # Black starts
    
    def initialize_board(self):
        # Create an empty board (standard 8x8 checkerboard with 12 pieces per player)
        board = [[EMPTY for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        # Place the initial pieces
        for row in range(self.board_size):
            for col in range(self.board_size):
                # Only place pieces on dark squares (odd sum of coordinates)
                if (row + col) % 2 == 1:
                    if row < 3:  # White pieces at the top
                        board[row][col] = PLAYER_2
                    elif row > 4:  # Black pieces at the bottom
                        board[row][col] = PLAYER_1
        
        return board
    
    def print_board(self, verbose=True):
        if not verbose:
            return
        
        # Print column headers
        print("  ", end="")
        for i in range(self.board_size):
            print(f"  {i} ", end="")
        print()
        
        # Print top border
        print("  ┼" + "───┼" * self.board_size)
        
        # Print rows
        for i, row in enumerate(self.board):
            print(f"{i} │", end="")
            for cell in row:
                if abs(cell) == 2:
                    print(f" {self.chars[cell]}│", end="")
                else:
                    print(f" {self.chars[cell]} │", end="")
            print()
            
            # Print row separator
            if i < self.board_size - 1:
                print("  ┼" + "───┼" * self.board_size)
                
        print()
        print()
    
    def get_valid_moves(self, player):
        # print(f"get valid moves for player:{player}")
        # Returns a list of valid moves for the player
        # Each move is a dict with start_pos, end_pos, and captures
        all_valid_moves = []
        capture_moves = []
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.board[row][col]
                
                # Check if the piece belongs to the player
                if (piece == player) or (piece == player * 2):  # Regular piece or king
                    # print(f"piece: {piece} at {row}, {col}")
                    # Get possible moves for this piece
                    piece_moves = self.get_piece_moves((row, col))
                    
                    # Separate capture moves
                    for move in piece_moves:
                        if move['captures']:
                            capture_moves.append(move)
                        else:
                            all_valid_moves.append(move)
        
        return all_valid_moves + capture_moves
    
    def get_piece_moves(self, position):
        # Returns valid moves for a piece at the given position
        row, col = position
        piece = self.board[row][col]
        moves = []
        
        # If it's an empty cell, return empty list
        if piece == EMPTY:
            return moves
        
        # Determine the player
        player = 1 if piece > 0 else -1
        is_king = abs(piece) == 2
        
        # Direction of movement (kings can move in both directions)
        directions = []
        if is_king or player == PLAYER_1:  # Black pieces move down
            directions.extend([(-1, -1), (-1, 1)])
        if is_king or player == PLAYER_2:  # White pieces move up
            directions.extend([(1, -1), (1, 1)])
        
        # Check regular moves first
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check if the new position is on the board
            if 0 <= new_row < self.board_size and 0 <= new_col < self.board_size:
                # Check if the new position is empty
                if self.board[new_row][new_col] == EMPTY:
                    moves.append({
                        'start_pos': position,
                        'end_pos': (new_row, new_col),
                        'captures': []
                    })
        
        # Check capture moves
        capture_moves = self.get_capture_moves(position)
        moves.extend(capture_moves)
        
        return moves
    
    def get_capture_moves(self, position, captured=None):
        # Returns all possible capture moves from a position
        if captured is None:
            captured = []
            
        row, col = position
        piece = self.board[row][col]
        moves = []
        
        # If it's an empty cell, return empty list
        if piece == EMPTY:
            return moves
        
        # Determine the player
        player = 1 if piece > 0 else -1
        is_king = abs(piece) == 2
        
        # Direction of movement (kings can move in all directions)
        directions = []
        if is_king or player == PLAYER_1:  # Black moves down
            directions.extend([(-1, -1), (-1, 1)])
        if is_king or player == PLAYER_2:  # White moves up
            directions.extend([(1, -1), (1, 1)])
        
        # Check for capture moves
        for dr, dc in directions:
            # Position of the potential opponent piece
            capture_row, capture_col = row + dr, col + dc
            
            # Position after the capture
            new_row, new_col = row + 2*dr, col + 2*dc
            
            # Check if the capture and landing positions are on the board
            if (0 <= capture_row < self.board_size and 0 <= capture_col < self.board_size and
                0 <= new_row < self.board_size and 0 <= new_col < self.board_size):
                
                # Get the piece at the capture position
                capture_piece = self.board[capture_row][capture_col]
                
                # Check if there's an opponent's piece to capture
                if (capture_piece != EMPTY and 
                    (capture_piece * player < 0) and  # Different signs means different players
                    self.board[new_row][new_col] == EMPTY and
                    (capture_row, capture_col) not in captured):
                    
                    # This is a valid capture move
                    capture_move = {
                        'start_pos': position,
                        'end_pos': (new_row, new_col),
                        'captures': captured + [(capture_row, capture_col)]
                    }
                    
                    moves.append(capture_move)
                    
                    # Recursively check for multiple captures
                    # Temporarily modify the board to simulate the capture
                    temp_piece = self.board[row][col]
                    temp_capture = self.board[capture_row][capture_col]
                    
                    self.board[row][col] = EMPTY
                    self.board[new_row][new_col] = temp_piece
                    self.board[capture_row][capture_col] = EMPTY
                    
                    # Get additional captures
                    additional_captures = self.get_capture_moves(
                        (new_row, new_col), 
                        captured + [(capture_row, capture_col)]
                    )
                    
                    # Restore the board
                    self.board[row][col] = temp_piece
                    self.board[new_row][new_col] = EMPTY
                    self.board[capture_row][capture_col] = temp_capture
                    
                    # Add the additional captures
                    moves.extend(additional_captures)
        
        return moves
    
    def make_move(self, move):
        # Execute a move on the board
        start_row, start_col = move['start_pos']
        end_row, end_col = move['end_pos']
        
        # Get the piece to move
        piece = self.board[start_row][start_col]
        
        # Move the piece
        self.board[start_row][start_col] = EMPTY
        self.board[end_row][end_col] = piece
        
        # Check if a piece was captured
        for capture_row, capture_col in move['captures']:
            self.board[capture_row][capture_col] = EMPTY
        
        # Check if the piece should be crowned as a king
        if piece == PLAYER_1 and end_row == 0:  # Black piece reaches top row
            self.board[end_row][end_col] = KING_1
        elif piece == PLAYER_2 and end_row == self.board_size - 1:  # White piece reaches bottom row
            self.board[end_row][end_col] = KING_2
        
        # Switch the current player
        self.current_player *= -1
    
    def play(self, verbose=False):
        # Game loop
        game_over = False
        result = None
        
        self.print_board(verbose)
        
        while not game_over:
            # Get the current player
            current_player = self.player1 if self.current_player == PLAYER_1 else self.player2
            
            # Get valid moves for the current player
            valid_moves = self.get_valid_moves(self.current_player)
            
            # Check if the current player has any moves
            if not valid_moves:
                # Current player cannot move, so the other player wins
                if self.current_player == PLAYER_1:
                    result = PLAYER_2  # Player 2 wins
                    if verbose:
                        print(f"Player 2 {self.player2.name} wins! Player 1 {self.player1.name} has no valid moves.")
                else:
                    result = PLAYER_1  # Player 1 wins
                    if verbose:
                        print(f"Player 1 {self.player1.name} wins! Player 2 {self.player2.name} has no valid moves.")
                game_over = True
                break
            
            # Ask the player to make a move
            move = current_player.move(self.board, self.current_player, valid_moves)
            
            # Execute the move
            self.make_move(move)
            self.print_board(verbose)
            
            # Check if the game is over (a player has no pieces left)
            if self.check_for_end():
                game_over = True
                if self.current_player == PLAYER_1:  # Current player is the one who just played
                    result = PLAYER_1  # Player 1 wins
                    if verbose:
                        print(f"Player 1 {self.player1.name} wins! Player 2 {self.player2.name} has no pieces left.")
                else:
                    result = PLAYER_2  # Player 2 wins
                    if verbose:
                        print(f"Player 2 {self.player2.name} wins! Player 1 {self.player1.name}  has no pieces left.")
        
        return result
    
    def check_for_end(self):
        player1_pieces, player2_pieces = self.count_pieces()
        
        return player1_pieces == 0 or player2_pieces == 0
    
    def get_board_state(self):
        # Return a deep copy of the board
        return [row[:] for row in self.board]
    
    def set_board(self, board, current_player):
        # Check if the board has the same shape
        if len(board) != self.board_size or any(len(row) != self.board_size for row in board):
            raise ValueError("The provided board does not have the correct dimensions")
        
        # Check if the board contains only expected values
        valid_values = [EMPTY, PLAYER_1, PLAYER_2, KING_1, KING_2]
        for row in board:
            for cell in row:
                if cell not in valid_values:
                    raise ValueError(f"The board contains invalid value: {cell}")
        
        # If all checks pass, overwrite the current board
        self.board = [row[:] for row in board]  # Deep copy to avoid reference issues
        if current_player in {PLAYER_1, PLAYER_2}:
            self.current_player = current_player
        else:
            raise ValueError(f"Invalid current player: {current_player}")


    def count_pieces(self):
        # Count the number of pieces for each player
        player1_pieces = 0
        player2_pieces = 0
        
        for row in self.board:
            for cell in row:
                if cell == PLAYER_1 or cell == KING_1:
                    player1_pieces += 1
                elif cell == PLAYER_2 or cell == KING_2:
                    player2_pieces += 1
        
        return player1_pieces, player2_pieces 