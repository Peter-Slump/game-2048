import random

from game_2048.exceptions import Game2048NoFreeLocationsLeft


class Game2048(object):

    """
    This class represents the core of the 2048 game.

    You can supply a grid size while initializing. This makes it possible to
    create bigger grids than the default 4x4.

    You can reset the grid with the reset method (will be called by default
    in the __init__. While resetting it's possible to give the number of
    positions to pre-fill with random numbers.
    """

    DIRECTION_UP = 'up'
    DIRECTION_DOWN = 'down'
    DIRECTION_LEFT = 'left'
    DIRECTION_RIGHT = 'right'

    DIRECTIONS_VERTICAL = (
        DIRECTION_DOWN,
        DIRECTION_UP
    )

    DIRECTIONS_HORIZONTAL = (
        DIRECTION_LEFT,
        DIRECTION_RIGHT
    )

    DIRECTIONS_REVERSED = (
        DIRECTION_RIGHT,
        DIRECTION_DOWN
    )

    _grid_size = None
    _grid = None
    _score = None
    _highest_value = None

    def __init__(self, grid_size=4):
    
        self._grid_size = grid_size

        self.reset()

    def reset(self, initial_number=2):
        """
        Reset the game.

        This will empty the grid, reset the score and the highest value counter.

        Supply an initial number of positions to fill with random numbers.
        """

        # Move to _reset function
        self._grid = [[None for _ in range(self._grid_size)] for _ in range(self._grid_size)]

        for _ in range(initial_number):
            self.add_random_number(values=(2,))

        self._score = 0
        self._highest_value = 0

    def add_random_number(self, values=(2, 4)):
        """
        Add a random number on an empty spot in the grid.

        One of the values will be randomly chosen to put on a random free column.
        """

        available_locations = []
        for row_i in range(self._grid_size):
            for column_i in range(self._grid_size):
                if self._grid[row_i][column_i] is None:
                    available_locations.append((row_i, column_i))

        if not available_locations:
            raise Game2048NoFreeLocationsLeft()

        location = random.choice(available_locations)

        self._grid[location[0]][location[1]] = random.choice(values)

    def move(self, direction):
        """
        Move the grid and add a random number to the grid.

        Example:
        >>> game = Game2048()
        >>> game.move(direction=Game2048.DIRECTION_RIGHT)

        """

        if self.move_grid(direction=direction):
            self.add_random_number()

    def move_grid(self, direction):
        """
        Move the values in the grid to the given direction.

        Apply all rules for shifting places and calculating new values.

        Doctests:

        Test move up
        From:
        [
            [2,    None, None, None],
            [None, 2,    None, 2],
            [2,    2,    4,    2],
            [None, None, 8,    2],
        ]
        To:
        [
            [4,    4,    4,    4],
            [None, None, 8,    2],
            [None, None, None, None],
            [None, None, None, None],
        ]

        >>> game = Game2048()
        >>> game._grid = [[2, None, None, None], [None, 2, None, 2], [2, 2, 4, 2], [None, None, 8, 2]]
        >>> game.move_grid('up')
        True
        >>> game._grid
        [[4, 4, 4, 4], [None, None, 8, 2], [None, None, None, None], [None, None, None, None]]

        Test move down
        From:
        [
            [None, None, 8,    2],
            [2,    2,    4,    2],
            [None, 2,    None, 2],
            [2,    None, None, None],
        ]

        To:
        [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, 8,    2],
            [4,    4,    4,    4],
        ]

        >>> game._grid = [[None, None, 8, 2], [2, 2, 4, 2], [None, 2, None, 2], [2, None, None, None]]
        >>> game.move_grid('down')
        True
        >>> game._grid
        [[None, None, None, None], [None, None, None, None], [None, None, 8, 2], [4, 4, 4, 4]]

        Test move left
        From:
        [
            [2,    None, 2,    None],
            [None, 2,    2,    None],
            [None, None, 4,    8   ],
            [None, 2,    2,    2   ],
        ]

        To:
        [
            [4,    None, None, None],
            [4,    None, None, None],
            [4,    8,    None, None],
            [4,    2,    None, None],
        ]
        >>> game._grid = [[2, None, 2, None], [None, 2, 2, None], [None, None, 4, 8], [None, 2, 2, 2]]
        >>> game.move_grid('left')
        True
        >>> game._grid
        [[4, None, None, None], [4, None, None, None], [4, 8, None, None], [4, 2, None, None]]

        Test move right
        From:
        [
            [None, 2,    None, 2   ],
            [None, 2,    2,    None],
            [4,    8,    None, None],
            [2,    2,    2,    None],
        ]
        To:
        [
            [None, None, None, 4],
            [None, None, None, 4],
            [None, None, 4,    8],
            [None, None, 2,    4],
        ]
        >>> game._grid = [[None, 2, None, 2], [None, 2, 2, None], [4, 8, None, None], [2, 2, 2, None]]
        >>> game.move_grid('right')
        True
        >>> game._grid
        [[None, None, None, 4], [None, None, None, 4], [None, None, 4, 8], [None, None, 2, 4]]
        """
        if direction not in self.DIRECTIONS_HORIZONTAL + self.DIRECTIONS_VERTICAL:
            raise Exception('Invalid direction')

        reversed_ = direction in self.DIRECTIONS_REVERSED
        grid_changed = False

        # Create the range to loop through. Normally this will be a list from 0 - grid size. When reversed this will be
        # from grid size to zero.
        if reversed_:
            range_ = range(self._grid_size - 1, -1, -1)
        else:
            range_ = range(self._grid_size)

        # When horizontal loop through rows, else loop through columns.
        for primary_i in range_:

            # Cursor represents the location where the next not-None value should be placed or summed. Initially this
            # will be the first position in the range.
            cursor_i = range_[0]

            # Loop through columns when moving horizontally else loop through the rows.
            for secondary_i in range_:

                # Initially we don't have to move the cursor. Moving cursor happens at the bottom of the loop when
                # needed.
                move_cursor = False

                # New value represents the new value which should be placed on the currently handled position.
                new_value = None

                # Determine the values of the current handled position and the value at the cursor position.
                if direction in self.DIRECTIONS_VERTICAL:
                    current_value = self._grid[secondary_i][primary_i]
                    cursor_value = self._grid[cursor_i][primary_i]
                else:
                    current_value = self._grid[primary_i][secondary_i]
                    cursor_value = self._grid[primary_i][cursor_i]

                # No value in this position so we don't have to do anything.
                # Also if we are currently handling the cursor position we don't have to do anything.
                if current_value is None or cursor_i == secondary_i:
                    continue

                if current_value != cursor_value:
                    # Current value is not equal to the cursor value. We need to set the column value on the cursor
                    # position.

                    if cursor_value is not None:
                        # There is already a value on the cursor position so se need to shift the cursor to the next
                        # position which makes that the value will be placed on the next empty spot.
                        cursor_i += -1 if reversed_ else 1

                        if cursor_i == secondary_i:
                            # The cursor moved to the current position, we can just continue with the next position
                            continue

                    cursor_value = current_value
                    grid_changed = True

                else:
                    # Cursor and current values are equal so we have to sum them. And make sure that the cursor is moved
                    # to the next position after updating the grid.
                    cursor_value = current_value + cursor_value
                    grid_changed = True
                    move_cursor = True

                    # Update score
                    self._score += cursor_value

                    if cursor_value > self._highest_value:
                        # New value is higher than the highest value before in the grid.
                        self._highest_value = cursor_value

                # Update the grid with new values.
                if direction in self.DIRECTIONS_VERTICAL:
                    self._grid[secondary_i][primary_i] = new_value
                    self._grid[cursor_i][primary_i] = cursor_value
                else:
                    self._grid[primary_i][secondary_i] = new_value
                    self._grid[primary_i][cursor_i] = cursor_value

                # When required move the cursor one position.
                if move_cursor:
                    cursor_i += -1 if reversed_ else 1

        return grid_changed