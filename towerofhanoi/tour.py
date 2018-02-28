"""
functions to run TOAH tours.
"""

# Copyright 2013, 2014, 2017 Gary Baumgartner, Danny Heap, Dustin Wehr,
# Bogdan Simion, Jacqueline Smith, Dan Zingaro, Yuan Xu
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2017.
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
# Copyright 2013, 2014 Gary Baumgartner, Danny Heap, Dustin Wehr


# you may want to use time.sleep(delay_between_moves) in your
# solution for 'if __name__ == "main":'
import time
from toah_model import TOAHModel


def tour_of_four_stools(model, delay_btw_moves=0.5, animate=False):
    """Move a tower of cheeses from the first stool in model to the fourth.

    @type model: TOAHModel
        TOAHModel with tower of cheese on first stool and three empty
        stools
    @type delay_btw_moves: float
        time delay between moves if console_animate is True
    @type animate: bool
        animate the tour or not
    """
    four_stools_hanoi(model, model.get_number_of_cheeses(), (0, 1, 2, 3))
    if animate:  # determine if it should animate in the console
        animate_hanoi(model, delay_btw_moves)


def four_stools_hanoi(model, cheeses, stools):
    """ Recursively move four cheeses using the indices in stools
    @type model: TOAHModel
    @type cheeses: int
        total cheeses
    @type stools: tuple
    @rtype: none
    """
    if cheeses <= 0:
        return None
    i = efficient_optimal_i_finder(cheeses)  # need to find a optimal i
    four_stools_hanoi(model, cheeses - i, (stools[0], stools[1], stools[3],
                                           stools[2]))
    three_stools_hanoi(model, i, (stools[0], stools[1], stools[3]))
    four_stools_hanoi(model, cheeses - i, (stools[2], stools[1], stools[0],
                                           stools[3]))


def three_stools_hanoi(model, cheeses, stools):
    """ Recursively move three cheeses in the model using indices in stools

    @type model: TOAHModel
    @type cheeses: int
        total cheeses
    @type stools: tuple
    @rtype: None
    """
    if cheeses <= 0:
        return None
    else:
        three_stools_hanoi(model, cheeses - 1, (stools[0], stools[2], stools[1]))
        model.move(stools[0], stools[2])
        three_stools_hanoi(model, cheeses - 1, (stools[1], stools[0], stools[2]))


def efficient_optimal_i_finder(n):
    """ find the optimal i for n cheeses using bottom up strategy

    @type n: int
        number of cheeses
    @rtype: int

    >>> efficient_optimal_i_finder(5)
    2
    """
    moves = [0] * (n + 1)
    moves[1] = (1, 1)  # base case
    ladder = 2
    while ladder < (n + 1):
        moves[ladder] = min([(2 * moves[ladder - i][0] + 2**i - 1, i)
                             for i in range(ladder - 1, 0, -1)])
        ladder += 1
    return moves[-1][1]


def animate_hanoi(reference_model, delay):
    """ animate the movements in the console window one by one;
     delay each movement by the given <delay>

    @type reference_model: TOAHModel
    @type delay: float
    @rtype: None
    """
    toah = TOAHModel(reference_model.get_number_of_stools())
    toah.fill_first_stool(reference_model.get_number_of_cheeses())
    seq = 0
    while seq < reference_model.number_of_moves():
        movement = reference_model.get_move_seq().get_move(seq)
        toah.move(movement[0], movement[1])
        time.sleep(delay)
        print(toah)
        seq += 1


if __name__ == '__main__':
    num_cheeses = 5
    delay_between_moves = 0.5
    console_animate = False
    # DO NOT MODIFY THE CODE BELOW.
    four_stools = TOAHModel(4)
    four_stools.fill_first_stool(number_of_cheeses=num_cheeses)

    tour_of_four_stools(four_stools,
                        animate=console_animate,
                        delay_btw_moves=delay_between_moves)
    print(four_stools.number_of_moves())
    # Leave files below to see what python_ta checks.
    # File tour_pyta.txt must be in same folder
    import python_ta

    python_ta.check_all(config="tour_pyta.txt")
