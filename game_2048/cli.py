from game_2048.exceptions import Game2048Error
from game_2048.game import Game2048


class Game2048CLI(Game2048):

    KEY_UP = 'w'
    KEY_DOWN = 's'
    KEY_LEFT = 'a'
    KEY_RIGHT = 'd'

    def __str__(self):
        str_ = ''

        for line in self._grid:
            for column in line:
                str_ += '{: ^6} |'.format(column)
            str_ += "\n"

        return str_

    def start(self):

        try:
            self._run()

        except Game2048Error as e:
            print 'Error: ', e

    def _run(self):

        self._display_game()

        while True:
            input_ = raw_input()

            if input_ == self.KEY_LEFT:
                self.move(self.DIRECTION_LEFT)
            elif input_ == self.KEY_RIGHT:
                self.move(self.DIRECTION_RIGHT)
            elif input_ == self.KEY_UP:
                self.move(self.DIRECTION_UP)
            elif input_ == self.KEY_DOWN:
                self.move(self.DIRECTION_DOWN)

            self._display_game()

    def _display_game(self):

        print chr(27) + "[2J"
        print self

