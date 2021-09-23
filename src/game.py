# Copyright (c) 2021 Johnathan P. Irvin
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from random import choice

class Game:
    @property
    def answer(self) -> int:
        """
        The answer to the game.

        Returns:
            int: The answer to the game.
        """
        return self._answer

    @property
    def attempts(self) -> int:
        """
        The number of attempts remaining.

        Returns:
            int: The number of attempts remaining.
        """
        return self._attempts

    @property
    def is_over(self) -> bool:
        """
        Checks if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self._attempts == 0


    def __init__(self, attempts: int = 10, range: range = range(1, 10)) -> None:
        """
        Initializes a new instance of the Game class.

        Args:
            attempts (int, optional): The total guess attempts. . Defaults to 10.
            range (range, optional): The range in which to guess. Defaults to range(1, 10).
        """
        self._max_attempts = attempts
        self._attempts = attempts
        self._range = range
        self._answer = self._generate_answer()

    def _generate_answer(self) -> int:
        """
        Generates a new answer.

        Returns:
            int: The new answer.
        """
        return choice(self._range)

    def new_game(self) -> None:
        """
        Starts a new game.
        """
        self._attempts = self._max_attempts
        self._answer = self._generate_answer()

    def guess(self, guess: int) -> bool:
        """
        Guesses the answer.

        Args:
            guess (int): The guess.

        Returns:
            bool: True if the guess is correct, False otherwise.
        """
        if guess == self._answer:
            self.new_game()
            return True
            
        self._attempts -= 1
        return False
