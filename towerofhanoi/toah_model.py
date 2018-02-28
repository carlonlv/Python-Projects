
"""
TOAHModel:  Model a game of Tour of Anne Hoy
Cheese:   Model a cheese with a given (relative) size
IllegalMoveError: Type of exceptions thrown when an illegal move is attempted
MoveSequence: Record of a sequence of (not necessarily legal) moves. You will
need to return MoveSequence object after solving an instance of the 4-stool
Tour of Anne Hoy game, and we will use that to check the correctness of your
algorithm.
"""


# Copyright 2013, 2014, 2017 Gary Baumgartner, Danny Heap, Dustin Wehr,
# Bogdan Simion, Jacqueline Smith, Dan Zingaro, Ritu Chaturvedi, Samar Sabie,
# Yuan Xu
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
#


class TOAHModel:
    """ Model a game of Tour Of Anne Hoy.

    Model stools holding stacks of cheese, enforcing the constraint
    that a larger cheese may not be placed on a smaller one.
    """

    def __init__(self, number_of_stools):
        """ Create new TOAHModel with empty stools
        to hold stools of cheese.

        @param TOAHModel self:
        @param int number_of_stools:
        @rtype: None

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> (M.get_number_of_stools(), M.number_of_moves()) == (4,0)
        True
        >>> M.get_number_of_cheeses()
        5
        """
        self._move_seq = MoveSequence([])
        self.number_of_stools = number_of_stools
        self._stools = []
        for _ in range(number_of_stools):
            self.get_stool().append([])

    def get_stool(self):
        """get the _stool list in self
        @type self: TOAHModel
        @rtype: list

        >>> model = TOAHModel(4)
        >>> len(model.get_stool()) == 4
        True
        """
        return self._stools

    def add(self, cheese, stool_index):
        """add the cheese to the stool_index position in self
        @type self: TOAHModel
        @type cheese: Cheese
        @type stool_index: int
        @rtype: None

        >>> model = TOAHModel(4)
        >>> cheese = Cheese(3)  # size is 3
        >>> model.add(cheese, 0)
        >>> len(model.get_stool()[0]) == 1
        True
        """
        if len(self.get_stool()) >= stool_index:
            self.get_stool()[stool_index].append(cheese)

    def get_cheese_location(self, cheese):
        """get the stool index position where the given cheese is in
        @type self: TOAHModel
        @type cheese: Cheese
        @rtype: int

        >>> model = TOAHModel(4)
        >>> cheese = Cheese(3)  # size is 3
        >>> model.add(cheese, 0)
        >>> model.get_cheese_location(cheese)
        0
        """
        for i, cheese_list in enumerate(self.get_stool()):
            if cheese in cheese_list:
                return i

    def get_top_cheese(self, stool_index):
        """get the cheese from the stool with the given stool_index in self
        @type self: TOAHModel
        @type stool_index: int
        @rtype: Cheese

        >>> model = TOAHModel(4)
        >>> cheese = Cheese(3)  # size is 3
        >>> model.add(cheese, 0)
        >>> isinstance(model.get_top_cheese(0), Cheese)
        True
        """
        if len(self.get_stool()) >= stool_index:
            cheese_list = self.get_stool()[stool_index]
            if cheese_list:
                return cheese_list[-1]

    def move(self, init_stool, final_stool):
        """move from the init_stool index to the final_stool index in self
        @type self: TOAHModel
        @type init_stool: int
        @type final_stool: int
        @rtype: None

        >>> model = TOAHModel(4)
        >>> cheese = Cheese(3)  # size is 3
        >>> cheese2 = Cheese(2)
        >>> model.add(cheese, 0)
        >>> model.add(cheese2, 0)
        >>> model.move(0, 1)
        >>> model.get_move_seq().get_move(0)
        (0, 1)
        """
        if self.get_stool()[init_stool]:
            top_cheese = self.get_stool()[init_stool].pop()
            if (not self.get_stool()[final_stool]) or \
                    (top_cheese.size < self.get_stool()[final_stool][-1].size):
                self.get_stool()[final_stool].append(top_cheese)
                self._move_seq.add_move(init_stool, final_stool)
            else:
                self.get_stool()[init_stool].append(top_cheese)
                raise IllegalMoveError('Bigger cheese cannot be stacked on'
                                       ' the small one')
        else:
            raise IllegalMoveError('No cheeses on the stools')

    def number_of_moves(self):
        """return a number of moves in self
        @type self: TOAHModel
        @rtype: int

        >>> model = TOAHModel(4)
        >>> cheese = Cheese(3)  # size is 3
        >>> model.add(cheese, 0)
        >>> model.move(0, 1)
        >>> model.number_of_moves() == 1
        True
        """
        return self._move_seq.length()

    def fill_first_stool(self, number_of_cheeses):
        """fill the number_of_cheeses in the first stool in self

        @type self: TOAHModel
        @type number_of_cheeses: int
        @rtype: None

        >>> model = TOAHModel(4)
        >>> model.fill_first_stool(2)
        >>> model.get_number_of_cheeses() == 2
        True
        """
        cheese_size = number_of_cheeses
        while cheese_size != 0:
            self.get_stool()[0].append(Cheese(cheese_size))
            cheese_size -= 1

    def get_number_of_cheeses(self):
        """return amount of cheeses the TOAHModel has in self
        @type self: TOAHModel
        @rtype: int

        >>> model = TOAHModel(4)
        >>> model.add(Cheese(3), 0)
        >>> model.get_number_of_cheeses() == 1
        True
        """
        total_cheeses = 0
        for cheese_list in self.get_stool():
            total_cheeses += len(cheese_list)
        return total_cheeses

    def get_number_of_stools(self):
        """return a number of stools in the TOAHModel self

        @type self: TOAHModel
        @rtype: int

        >>> model = TOAHModel(4)
        >>> model.get_number_of_stools() == 4
        True
        """
        return self.number_of_stools

    def get_move_seq(self):
        """ Return the move sequence in self

        @type self: TOAHModel
        @rtype: MoveSequence

        >>> toah = TOAHModel(2)
        >>> toah.get_move_seq() == MoveSequence([])
        True
        """
        return self._move_seq

    def __eq__(self, other):
        """ Return whether TOAHModel self is equivalent to other.

        Two TOAHModels are equivalent if their current
        configurations of cheeses on stools look the same.

        *******
        More precisely, for all h,s, the h-th cheese on the s-th
        stool of self should be equivalent the h-th cheese on the s-th
        stool of other

        @type self: TOAHModel
        @type other: TOAHModel
        @rtype: bool

        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(7)
        >>> m1.move(0, 1)
        >>> m1.move(0, 2)
        >>> m1.move(1, 2) # the third stool has 2 cheeses
        >>> m2 = TOAHModel(4)
        >>> m2.fill_first_stool(7)
        >>> m2.move(0, 3)
        >>> m2.move(0, 2)
        >>> m2.move(3, 2) # the third stool has 2 cheeses
        >>> m1 == m2
        True
        """
        return isinstance(self, TOAHModel) == isinstance(other, TOAHModel) and \
               len(self.get_stool()) == len(other._stools) and \
               all([self.get_stool()[i] == other._stools[i]
                    for i in range(len(self.get_stool()))])

    def _cheese_at(self, stool_index, stool_height):
        # """ Return (stool_height)th from stool_index stool, if possible.
        #
        # @type self: TOAHModel
        # @type stool_index: int
        # @type stool_height: int
        # @rtype: Cheese | None
        #
        # >>> M = TOAHModel(4)
        # >>> M.fill_first_stool(5)
        # >>> M._cheese_at(0,3).size
        # 2
        # >>> M._cheese_at(0,0).size
        # 5
        # """
        if 0 <= stool_height < len(self.get_stool()[stool_index]):
            return self.get_stool()[stool_index][stool_height]
        else:
            return None

    def __str__(self):
        """
        Depicts only the current state of the stools and cheese.

        @param TOAHModel self:
        @rtype: str
        """
        all_cheeses = []
        for height in range(self.get_number_of_cheeses()):
            for stool in range(self.get_number_of_stools()):
                if self._cheese_at(stool, height) is not None:
                    all_cheeses.append(self._cheese_at(stool, height))
        max_cheese_size = max([c.size for c in all_cheeses]) \
            if len(all_cheeses) > 0 else 0
        stool_str = "=" * (2 * max_cheese_size + 1)
        stool_spacing = "  "
        stools_str = (stool_str + stool_spacing) * self.get_number_of_stools()

        def _cheese_str(size):
            # helper for string representation of cheese
            if size == 0:
                return " " * len(stool_str)
            cheese_part = "-" + "--" * (size - 1)
            space_filler = " " * int((len(stool_str) - len(cheese_part)) / 2)
            return space_filler + cheese_part + space_filler

        lines = ""
        for height in range(self.get_number_of_cheeses() - 1, -1, -1):
            line = ""
            for stool in range(self.get_number_of_stools()):
                c = self._cheese_at(stool, height)
                if isinstance(c, Cheese):
                    s = _cheese_str(int(c.size))
                else:
                    s = _cheese_str(0)
                line += s + stool_spacing
            lines += line + "\n"
        lines += stools_str

        return lines


class Cheese:
    """ A cheese for stacking in a TOAHModel

    === Attributes ===
    @param int size: width of cheese
    """

    def __init__(self, size):
        """ Initialize a Cheese to diameter size.

        @param Cheese self:
        @param int size:
        @rtype: None

        >>> c = Cheese(3)
        >>> isinstance(c, Cheese)
        True
        >>> c.size
        3
        """
        self.size = size

    def __eq__(self, other):
        """ Is self equivalent to other?

        We say they are if they're the same
        size.

        @param Cheese self:
        @param Cheese|Any other:
        @rtype: bool

        >>> c1 = Cheese(2)
        >>> c2 = Cheese(3)
        >>> c1 == c2
        False
        """
        return (isinstance(self, TOAHModel) == isinstance(other, TOAHModel)
                and self.size == other.size)


class IllegalMoveError(Exception):
    """ Exception indicating move that violate TOAHModel
    """
    pass


class MoveSequence(object):
    """ Sequence of moves in TOAH game
    """

    def __init__(self, moves):
        """ Create a new MoveSequence self.

        @param MoveSequence self:
        @param list[tuple[int]] moves:
        @rtype: None

        >>> m1 = MoveSequence([(0,1), (1, 2)])
        >>> [m1.get_move(0), m1.get_move(1)]
        [(0, 1), (1, 2)]
        """
        # moves - a list of integer pairs, e.g. [(0,1),(0,2),(1,2)]
        self._moves = moves

    def get_move(self, i):
        """ Return the move at position i in self

        @param MoveSequence self:
        @param int i:
        @rtype: tuple[int]

        >>> ms = MoveSequence([(1, 2)])
        >>> ms.get_move(0) == (1, 2)
        True
        """
        return self._moves[i]

    def add_move(self, src_stool, dest_stool):
        """ Add move from src_stool to dest_stool to MoveSequence self.

        @param MoveSequence self:
        @param int src_stool:
        @param int dest_stool:
        @rtype: None
        """
        self._moves.append((src_stool, dest_stool))

    def length(self):
        """ Return number of moves in self.

        @param MoveSequence self:
        @rtype: int

        >>> ms = MoveSequence([(1, 2)])
        >>> ms.length()
        1
        """
        return len(self._moves)

    def generate_toah_model(self, number_of_stools, number_of_cheeses):
        """ Construct TOAHModel from number_of_stools and number_of_cheeses
         after moves in self.

        Takes the two parameters for
        the game (number_of_cheeses, number_of_stools), initializes the game
        in the standard way with TOAHModel.fill_first_stool(number_of_cheeses),
        and then applies each of the moves in this move sequence.

        @param MoveSequence self:
        @param int number_of_stools:
        @param int number_of_cheeses:
        @rtype: TOAHModel


        >>> toah = TOAHModel(2)
        >>> toah.fill_first_stool(2)
        >>> ms = MoveSequence([])
        >>> toah == ms.generate_toah_model(2, 2)
        True
        """
        model = TOAHModel(number_of_stools)
        model.fill_first_stool(number_of_cheeses)
        for move in self._moves:
            model.move(move[0], move[1])
        return model

    def __eq__(self, other):
        """check if self have the same tuple of moves as other
        @type self: MoveSequence
        @type other: Any
        @rtype: bool

        >>> MoveSequence([(0,1)]) ==  MoveSequence([(2, 0)])
        False
        """
        return isinstance(self, MoveSequence) == \
               isinstance(other, MoveSequence) and \
               self.length() == other.length() and \
               all([self.get_move(i) == other.get_move(i)
                    for i in range(len(self._moves))])


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)
    # Leave lines below to see what python_ta checks.
    # File toahmodel_pyta.txt must be in same folder.
    import python_ta

    python_ta.check_all(config="toahmodel_pyta.txt")
    import doctest

    doctest.testmod()
