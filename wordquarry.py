import random
import numpy as np
import pandas as pd
import time

def create_board(board_size):
    board = np.chararray(board_size, unicode = True)
    board[:] = '_'

    #print(f'Created board:\n\n{board}')
    return board

def check_free(board, idx):
    #print(f'Checking {idx}')
    conditions = [idx[0] < board.shape[0],
                  idx[0] >= 0,
                  idx[1] < board.shape[1],
                  idx[1] >= 0]
    if not all(conditions):
        return False
    if board[idx[0], idx[1]] == '_':
        return True
    else:
        return False

def get_surrounding(board, idx):
    surrounding = [(idx[0] + dx, idx[1] + dy)
                   for dx in (-1, 0, 1)
                   for dy in (-1, 0, 1) 
                   if not (dx == 0 and dy == 0)]
    for i in range(len(surrounding) - 1, -1, -1):
        if not check_free(board, surrounding[i]):
            surrounding.pop(i)
    return surrounding

def explore_region(board, start_idx):
    visited = set()
    to_visit = [start_idx]
    while to_visit:
        current = to_visit.pop()
        if current not in visited:
            visited.add(current)
            neighbors = get_surrounding(board, current)
            for neighbor in neighbors:
                if neighbor not in visited:
                    to_visit.append(neighbor)
    return visited

def check_tree_length(check_idx):
    def dfs(node, visited, depth):
        #print(f'Checking {node}, depth {depth}')
        if depth >= 3:
            return True
        visited.add(node)
        for neighbor in get_surrounding(board, node):
            if neighbor not in visited:
                if dfs(neighbor, visited, depth + 1):
                    return True
        visited.remove(node)
        return False

    return dfs(check_idx, set(), 1)

def check_blocking(board, idx, min_length = 3):
    '''
    Check that the current word does not create any unreachable pockets of
    less than min_length letters.

    Parameters
    ----------
    idx : list
        XY coordinates of the letter about to be placed
    min_length : int, optional
        Minimum word length, pockets smaller than this are prevented, by default 3

    Returns
    -------
    bool
        True if the placed character is blocking (creates pockets)
        False otherwise
    '''
    return False

    surrounding = get_surrounding(board, idx)

    board[idx[0], idx[1]] = '$'

    for check_idx in surrounding:
        if not check_tree_length(check_idx):
            board[idx[0], idx[1]] = '_'
            return True

    return False

def next_idx(board, idx):
    free = False
    surrounding = get_surrounding(board, idx)

    while not free:
        if len(surrounding) == 0:
            return False
        
        idx_new = random.choice(surrounding)
        free = check_free(board, idx_new) and not check_blocking(board, idx_new)

        if not free:
            surrounding.remove(idx_new)

    return idx_new

def clear_coords(board, coords):
    for coord in coords:
        board[coord[0], coord[1]] = '_'

def starting_slots(board):
    free = [(x, y) for x in range(board.shape[0])
                   for y in range(board.shape[1])
                   if board[x, y] == '_']

    return free

def place_word(board, word, start_positions = None):
    if len(word) == 0:
        return True
    
    used_coords = []
    free = False

    if start_positions == None:
        start_positions = starting_slots(board)
    
    while free == False:
        if len(start_positions) == 0:
            clear_coords(board, used_coords)
            return False
        
        idx = random.choice(start_positions)
        free = check_free(board, idx) and not check_blocking(board, idx)
        if not free:
            start_positions.remove(idx)
            continue
    
        board[idx[0], idx[1]] = word[0]
        used_coords.append((idx[0], idx[1]))

        if place_word(board, word[1:], get_surrounding(board, idx)):
            return True
        else:
            start_positions.remove(idx)

    return False

def choose_words(board, wordlist):
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
    return(words)

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
