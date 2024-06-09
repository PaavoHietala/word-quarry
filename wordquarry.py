import random
import numpy as np
import pandas as pd

def create_board(board_size):
    '''
    Create an X-by-Y board, initialized with underscores '_'.

    Parameters
    ----------
    board_size : list of int
        Row and column count for the board

    Returns
    -------
    np.array
        2D board initialized with underscores
    '''

    board = np.chararray(board_size, unicode = True)
    board[:] = '_'

    return board

def check_free(board, idx):
    '''
    Check if the given cell is unoccupied on the board and the index values
    are not outside the board dimensions.

    Parameters
    ----------
    board : np.array
        2D game board
    idx : list
        Row and column index to be checked on the <board>

    Returns
    -------
    bool
        True if cell is free and playable, False otherwise
    '''

    # Check valid indices
    conditions = [idx[0] < board.shape[0],
                  idx[0] >= 0,
                  idx[1] < board.shape[1],
                  idx[1] >= 0]

    if not all(conditions):
        return False

    # Check cell occupancy
    if board[idx[0], idx[1]] == '_':
        return True
    else:
        return False

def get_surrounding(board, idx):
    '''
    Get neighbouring cells which are free to play
    (not occupied or outside the board).

    Parameters
    ----------
    board : np.array
        2D game board
    idx : list
        Row and column index to be checked on the <board>

    Returns
    -------
    list of list of int
        List of valid [row, column] coordinate pairs around <idx>
    '''

    surrounding = [(idx[0] + dx, idx[1] + dy)
                   for dx in (-1, 0, 1)
                   for dy in (-1, 0, 1) 
                   if not (dx == 0 and dy == 0)]
    
    for i in range(len(surrounding) - 1, -1, -1):
        if not check_free(board, surrounding[i]):
            surrounding.pop(i)

    return surrounding

def clear_coords(board, coords):
    '''
    Reset given <coords> on the <board> as underscores.

    Parameters
    ----------
    board : np.array
        2D game board
    coords : list of list of int
        List of [row, column] coordinate pairs to clear from <board>
    
    Returns
    -------
    bool
        True in all cases
    '''

    for coord in coords:
        board[coord[0], coord[1]] = '_'
    
    return True

def starting_slots(board):
    '''
    Check valid starting slots for given <board>.

    Parameters
    ----------
    board : np.array
        2D game board

    Returns
    -------
    list of tuple of int
        List of valid starting point (row, column) coordinate pairs on <board>
    '''

    free = [(x, y) for x in range(board.shape[0])
                   for y in range(board.shape[1])
                   if board[x, y] == '_']

    return free

def place_word(board, word, start_positions = None):
    '''
    Recursively place the given <word> on the <board>, trying out all possible
    <start_positions> in the process.

    Parameters
    ----------
    board : np.array
        2D game board
    word : str
        A word to be placed on the board, a single character is clipped from the
        beginning for each recursive layer
    start_positions : list of list of int, optional
        The set of character placement locations to be tested. In the beginning
        the parameter is chosen by the <starting_slots> function, but it is
        updated for each recursion to hold the empty neighbouring cells,
        by default None

    Returns
    -------
    bool
        True if word placement succeeded, False otherwise.
    '''

    # Reached the end of recursion tree
    if len(word) == 0:
        return True
    
    used_coords = []
    free = False

    if start_positions == None:
        start_positions = starting_slots(board)
    
    while free == False:
        # All directions have been checked, failure
        if len(start_positions) == 0:
            clear_coords(board, used_coords)
            return False
        
        # Pick a new direction for the search
        idx = random.choice(start_positions)
    
        board[idx[0], idx[1]] = word[0]
        used_coords.append((idx[0], idx[1]))

        # We need to go deeper
        if place_word(board, word[1:], get_surrounding(board, idx)):
            return True
        else:
            start_positions.remove(idx)

    return False

def choose_words(board, wordlist):
    '''
    Choose words from the list so that their total length equals the number
    of cells in <board>. The minimum word length is currently hard-coded as 3.

    Parameters
    ----------
    board : np.array
        2D game board
    wordlist : pd.DataFrame
        List of words and their lengths in DataFrame columns

    Returns
    -------
    list of str
        List of words chosen for the game
    '''

    words = []
    chars = board.shape[0] * board.shape[1]

    while sum([len(word) for word in words]) < chars:
        maxlen = chars - sum([len(word) for word in words])

        _wordlist = wordlist.loc[wordlist['length'] <= maxlen]

        word = _wordlist.sample(1)['word'].iloc[0]

        if maxlen - len(word) in [1, 2]:
            continue
        else:
            words.append(word)
    
    print(f'Words: {words}')
    return words

if __name__ == "__main__":
    wordlist = pd.read_csv('finwords_noCompounds.txt')
    print(f'Loaded words, for example {random.choice(wordlist["word"])}')

    board_size = [6, 5]
    board = create_board(board_size)
    words = choose_words(board, wordlist)

    fails = 0

    while True:
        success = False

        for word in words:
            if place_word(board, word):
                success = True
            else:
                success = False
                break
        
        if success:
            break
        else:    
            board = create_board(board_size)
            fails += 1

    print(f'Succeeded in creating a board after {fails} tries:\n')
    print(board)
