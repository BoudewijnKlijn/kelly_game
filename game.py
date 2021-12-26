import itertools
import random
import time
import logging


STARTUP_MESSAGE = "Welcome to Kelly game.\nYou are given the same bet for some number of times.\n" \
                  "On average you gain 7% per turn.\n"
Q_WIN_PROB = "Enter a win probability (e.g. 60 means 60%):"
Q_GAIN_PERCENT = "Enter how much you receive if you win (after giving away complete bet, 120 = +20%):"
Q_NUMBER_OF_TURNS = "Enter how many turns you want to play:"
AVERAGE_GAIN = 107
START_CAPITAL = 100
Q_START_CAPITAL = f"You start the game with {START_CAPITAL} euro."
Q_CHOOSE_BET = "Enter bet for this turn:"


class Game:
    def __init__(self):
        # Display start message.
        print(STARTUP_MESSAGE)
        print(Q_START_CAPITAL)
        self.capital = START_CAPITAL
        self.average_gain = AVERAGE_GAIN
        self.turn = 0
        self.random_state = int(time.time())
        logging.basicConfig(filename='log.txt', filemode="a", level=logging.DEBUG)
        self.logger = logging.getLogger('GAME')

        # Init random state.
        random.seed(self.random_state)

        # Ask for chance to win.
        self.p = self.ask_number(Q_WIN_PROB, 50, 100)
        # self.p = 60  # DEFAULT
        self.p /= 100

        # Calculate the chance to lose.
        self.q = 1 - self.p

        # Ask for gain if you win per turn.
        self.win_return = self.ask_number(Q_GAIN_PERCENT, self.average_gain, 200)
        # self.win_return = 200  # DEFAULT

        # Calculate lose percent.
        self.lose_return = self.average_gain - self.p * self.win_return

        # Ask number of times to play.
        self.total_turns = self.ask_number(Q_NUMBER_OF_TURNS, 1, 100)

    def __repr__(self):
        return f"Game({self.capital=}, {self.average_gain=}, {self.p=}, {self.q=}, " \
               f"{self.win_return=}, {self.lose_return=}, {self.total_turns=}, {self.turn=}, " \
               f"{self.random_state=})"

    @staticmethod
    def ask_number(question, low, high):
        """Ask for a number within a range."""
        default_message = f"Please enter an integer number: {low} < int(number) <= {high}."
        while True:
            try:
                response = int(input(question))
            except ValueError:
                print(default_message)
                continue
            if low < response <= high:
                print(f"Using {response}.")
                return response
            else:
                print(default_message)

    def do_turn(self):
        # Display current game state.
        print(self)
        self.logger.info(self)

        # Request bet.
        bet = self.ask_number(Q_CHOOSE_BET, 0, self.capital)
        self.logger.info(f"Bet: {bet}")

        r = random.random()
        self.capital -= bet
        if r < self.p:
            print(f"You won!", end=' ')
            self.logger.info("Win")
            received = bet * self.win_return / 100
        else:
            print(f"You lost!", end=' ')
            self.logger.info("Lose")
            received = bet * self.lose_return / 100

        print(f"Bet: {bet:.2f}. Received back: {received:.2f}")
        self.capital += received

    def play(self):
        self.logger.info(f"Game starts.")
        for self.turn in itertools.count(1):
            self.do_turn()
            if self.capital <= 0:
                print(f"GAME OVER (you lost all your money)")
                break
            if self.turn >= self.total_turns:
                print("Game ends.", self)
                break
        self.logger.info(self)
        self.logger.info(f"Game ends.")


if __name__ == '__main__':
    game = Game()
    game.play()
