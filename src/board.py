import random
import numpy as np
import pandas as pd

class Board:
    '''
    A class which holds the letter grid for the game and the associated wordlist
    which is given as a file path
    '''

    def __init__(self, size, wordlist_path):
        '''
        Initialize the Board object

        Parameters
        ----------
        size : list of int
            Rows and columns of the board
        wordlist_path : str
            Path to a wordlist .csv file, which has rows of <word,len(word)>
        '''

        wordlist = pd.read_csv(wordlist_path)
        print(f'Loaded words, for example {random.choice(wordlist["word"])}')

        self.size = size
        self.wordlist = pd.read_csv(wordlist_path)
        
        self.board = self.create_board(size)

    def create_board(self, size):
        '''
        Create an X-by-Y board, initialized with underscores '_'.

        Parameters
        ----------
        size : list of int
            Row and column count for the board

        Returns
        -------
        np.array
            2D board initialized with underscores
        '''

        board = np.chararray(size, unicode = True)
        board[:] = '_'

        return board

    def fill_board(self):
        fails = 0
        words = self.choose_words()
        
        while True:
            self.board = self.create_board(self.size)
            success = False

            for word in words:
                if self.place_word(word):
                    success = True
                else:
                    success = False
                    break
            
            if success:
                break
            else:    
                fails += 1

        print(f'Succeeded in creating a board after {fails} tries:\n')
        print(self.board)

    def check_free(self, idx):
        '''
        Check if the given cell is unoccupied on the board and the index values
        are not outside the board dimensions.

        Parameters
        ----------
        idx : list
            Row and column index to be checked on the board

        Returns
        -------
        bool
            True if cell is free and playable, False otherwise
        '''

        conditions = [idx[0] < self.board.shape[0],
                      idx[0] >= 0,
                      idx[1] < self.board.shape[1],
                      idx[1] >= 0]

        if not all(conditions):
            return False

        if self.board[idx[0], idx[1]] == '_':
            return True
        else:
            return False

    def get_surrounding(self, idx):
        '''
        Get neighbouring cells which are free to play
        (not occupied or outside the board).

        Parameters
        ----------
        idx : list
            Row and column index to be checked on the board

        Returns
        -------
        list of list of int
            List of valid [row, column] coordinate pairs around idx
        '''

        surrounding = [(idx[0] + dx, idx[1] + dy)
                       for dx in (-1, 0, 1)
                       for dy in (-1, 0, 1) 
                       if not (dx == 0 and dy == 0)]
        
        for i in range(len(surrounding) - 1, -1, -1):
            if not self.check_free(surrounding[i]):
                surrounding.pop(i)

        return surrounding

    def clear_coords(self, coords):
        '''
        Reset given coords on the board as underscores.

        Parameters
        ----------
        coords : list of list of int
            List of [row, column] coordinate pairs to clear from board
        
        Returns
        -------
        bool
            True in all cases
        '''

        for coord in coords:
            self.board[coord[0], coord[1]] = '_'
        
        return True

    def starting_slots(self):
        '''
        Check valid starting slots for the board.

        Returns
        -------
        list of tuple of int
            List of valid starting point (row, column) coordinate pairs on board
        '''

        free = [(x, y) for x in range(self.board.shape[0])
                       for y in range(self.board.shape[1])
                       if self.board[x, y] == '_']
        return free

    def place_word(self, word, start_positions=None):
        '''
        Recursively place the given word on the board, trying out all possible
        start_positions in the process.

        Parameters
        ----------
        word : str
            A word to be placed on the board, a single character is clipped from the
            beginning for each recursive layer
        start_positions : list of list of int, optional
            The set of character placement locations to be tested. In the beginning
            the parameter is chosen by the starting_slots function, but it is
            updated for each recursion to hold the empty neighbouring cells,
            by default None

        Returns
        -------
        bool
            True if word placement succeeded, False otherwise.
        '''

        if len(word) == 0:
            return True
        
        used_coords = []
        free = False

        if start_positions is None:
            start_positions = self.starting_slots()
        
        while free == False:
            if len(start_positions) == 0:
                self.clear_coords(used_coords)
                return False
            
            idx = random.choice(start_positions)
        
            self.board[idx[0], idx[1]] = word[0]
            used_coords.append((idx[0], idx[1]))

            if self.place_word(word[1:], self.get_surrounding(idx)):
                return True
            else:
                start_positions.remove(idx)

        return False

    def choose_words(self):
        '''
        Choose words from the list so that their total length equals the number
        of cells in board. The minimum word length is currently hard-coded as 3.

        Returns
        -------
        list of str
            List of words chosen for the game
        '''

        words = []
        chars = self.board.shape[0] * self.board.shape[1]

        while sum([len(word) for word in words]) < chars:
            maxlen = chars - sum([len(word) for word in words])

            _wordlist = self.wordlist.loc[self.wordlist['length'] <= maxlen]

            word = _wordlist.sample(1)['word'].iloc[0]

            if maxlen - len(word) in [1, 2]:
                continue
            else:
                words.append(word)
        
        print(f'Words: {words}')
        return words
