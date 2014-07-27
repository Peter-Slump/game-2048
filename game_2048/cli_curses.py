import curses

from exceptions import Game2048NoFreeLocationsLeft
from game_2048.game import Game2048


class Game2048Curses(Game2048):

    KEY_QUIT = ord('q')
    KEY_RESET = ord('r')
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

    templates = {
        'score': 'Score: {score}',
        'level_complete': 'Congratulations your highest item is {highest}!. The new threshold is now {threshold}.',
        'logo': """
 ___   ___    __   ___
(__ \ / _ \  /. | ( _ )
 / _/( (_) )(_  _)/ _ \\
(____)\___/   (_) \___/

""",
        'help_text': 'Use the arrow keys to play. Press q for quit or r to restart.',
        'game_over': 'Game over! Your score is {score}. Press r to restart the game.'
    }

    _std_scr = None
    _highest_value_threshold = 2048

    _message = None

    _line_position = 0

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

        self._refresh_screen()

        key_ = None

        while key_ != self.KEY_QUIT:

            key_ = self._std_scr.getch()

            if key_ in self.KEY_DIRECTION_MAPPING:

                try:
                    self.move(self.KEY_DIRECTION_MAPPING[key_])
                except Game2048NoFreeLocationsLeft:
                    self._display_game_over_screen()
                    continue

                if self._highest_value >= self._highest_value_threshold:
                    self._highest_value_threshold *= 2

                    self._message = self.templates['level_complete'].format(highest=self._highest_value,
                                                                            threshold=self._highest_value_threshold)

            if key_ == self.KEY_RESET:
                self.reset()

            self._refresh_screen()

    def _update_game(self):

        offset = 1

        self._write_line((8 * '-') * self._grid_size)

        for row_i, row in enumerate(self._grid):
            str_ = ''
            for column in row:
                str_ += '{: ^6} |'.format(column if column else '')

            self._write_line(str_)
            self._write_line((8 * '-') * self._grid_size)

    def _update_logo(self):

        for line in self.templates['logo'].split("\n"):
            self._write_line(content=line)

    def _display_game_over_screen(self):

        self._line_position = 0
        self._std_scr.clear()

        self._update_logo()
        self._write_line(self.templates['game_over'].format(score=self._score))

    def _refresh_screen(self):

        self._line_position = 0
        self._std_scr.clear()

        self._update_logo()
        self._write_line(self.templates['score'].format(score=self._score))
        self._write_line(self._message or '')
        self._message = None
        self._update_game()

        self._line_position += 1

        self._write_line(content=self.templates['help_text'])

        self._write_line('')

    def _write_line(self, content, x_offset=0):

        self._std_scr.addstr(self._line_position, x_offset, content)
        self._line_position += 1


if __name__ == '__main__':

    Game2048Curses()