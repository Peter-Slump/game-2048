from game_2048.game import Game2048


class Game2048Curses(Game2048):

    KEY_QUIT = ord('q')
    KEY_DOWN = 66
    KEY_UP = 65
    KEY_LEFT = 68
    KEY_RIGHT = 67

    KEY_DIRECTION_MAPPING = {
        KEY_DOWN: Game2048.DIRECTION_DOWN,
        KEY_UP: Game2048.DIRECTION_UP,
        KEY_RIGHT: Game2048.DIRECTION_RIGHT,
        KEY_LEFT: Game2048.DIRECTION_LEFT
    }

    _std_scr = None
    _highest_value_threshold = 2048

    def __init__(self, auto_start=True, *args, **kwargs):

        super(Game2048Curses, self).__init__(*args, **kwargs)

        if auto_start:
            self._start()

    def _start(self):

        self._std_scr = curses.initscr()
        curses.cbreak()

        try:
            self._run()
        finally:
            curses.endwin()

    def _run(self):

        self._update_game()

        key_ = None

        while key_ != self.KEY_QUIT:

            key_ = self._std_scr.getch()

            if key_ in self.KEY_DIRECTION_MAPPING:
                self.move(self.KEY_DIRECTION_MAPPING[key_])

            self._update_game()

            if self._highest_value >= self._highest_value_threshold:
                self._highest_value_threshold *= 2

                self._update_message(
                    message='Congratulations your highest item is {highest}!. The new threshold is now {threshold}.'
                    .format(
                        highest=self._highest_value,
                        threshold=self._highest_value_threshold
                    )
                )
            else:
                self._update_message(message='Score: {score}'.format(score=self._score  ))

    def _update_message(self, message):

        self._std_scr.addstr(0, 0, message)

    def _update_game(self):

        offset = 1

        self._std_scr.addstr(offset, 0, (8 * '-') * self._grid_size)

        for row_i, row in enumerate(self._grid):
            str_ = ''
            for column in row:
                str_ += '{: ^6} |'.format(column if column else '')

            self._std_scr.addstr((row_i * 2) + offset + 1, 0, str_)
            self._std_scr.addstr((row_i * 2) + offset + 2, 0, (8 * '-') * self._grid_size)


if __name__ == '__main__':

    Game2048Curses()