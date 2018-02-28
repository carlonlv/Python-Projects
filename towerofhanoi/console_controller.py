"""
ConsoleController: User interface for manually solving
Anne Hoy's problems from the console.
"""

# Copyright 2014, 2017 Dustin Wehr, Danny Heap, Bogdan Simion,
# Jacqueline Smith, Dan Zingaro, Yuan Xu
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


from toah_model import TOAHModel, IllegalMoveError


def move(model, origin, dest):
    """ Apply move from <origin> to <dest> in model.

    May raise an IllegalMoveError.

    @param TOAHModel model:
        model to modify
    @param int|str origin:
        stool number (index from 0) of cheese to move
    @param int|str dest:
        stool number you want to move cheese to
    @rtype: None
    """
    from_ = int(origin)
    to = int(dest)
    if (0 <= from_ < len(model.get_stool())) and \
            (0 <= to < len(model.get_stool())) and from_ != to:
        model.move(from_, to)
    else:
        raise IllegalMoveError('This is a invalid input')


def extract_input(input_):
    """extract the input_
    @type input_: str
    @rtype: tuple
    """
    result = input_.strip().split()
    return result[0], result[-1]


def show_instruction():
    """display instruction on console window
    @rtype: None
    """
    goal = 'Move all the cheeses from the first stack to the end stack;\n'
    introduction = 'Here is the instruction for you to follow: \n'
    instruction_body = '\t 1. First digit is initial stool index, add a space,'\
                       ' and second digit is final stool index ' \
                       '(Extra spaces will be omitted by the program) \n'
    example = '\t 2. For example: move from stool index 0 to 3:' \
              ' 0 3 (Stool index starts at zero and counts up)\n'
    notes = '\t 3. After each move, press enter.. \n'
    rules = '\t 4. RULES:You cannot stack a bigger' \
            ' cheese onto a smaller cheese!!!! and input PROPER EXPRESSION \n'
    begin = '\t 5. You can start the game by input the move now: \n'
    end = "\t 6. Type 'end' to end the game or finish the game \n"
    template = '{} {} {} {} {} {} {} {}'
    print(template.format(goal, introduction, instruction_body,
                          example, notes, rules, begin, end))


def display_won_message(won_message):
    """ check if the user won the game by <won_message>
    @type won_message: bool
    @rtype: None

    >>> display_won_message(won_message=True)
    You Won the Game!!
    """
    if won_message:
        print('You Won the Game!!')
    else:
        print('You ended the game...')


class ConsoleController:
    """ Controller for text console.
    """

    def __init__(self, number_of_cheeses, number_of_stools):
        """ Initialize a new ConsoleController self.

        @param ConsoleController self:
        @param int number_of_cheeses:
        @param int number_of_stools:
        @rtype: None

        >>> c = ConsoleController(2, 4)
        >>> c.number_of_cheeses, c.number_of_stools
        (2, 4)
        """
        self.number_of_cheeses = number_of_cheeses
        self.number_of_stools = number_of_stools

    def play_loop(self):
        """ Play Console-based game.

        @param ConsoleController self:
        @rtype: None

        TODO:
        -Start by giving instructions about how to enter moves (which is up to
        you). Be sure to provide some way of exiting the game, and indicate
        that in the instructions.
        -Use python's built-in function input() to read a potential move from
        the user/player. You should print an error message if the input does
        not meet the specifications given in your instruction or if it denotes
        an invalid move (e.g. moving a cheese onto a smaller cheese).
        You can print error messages from this method and/or from
        ConsoleController.move; it's up to you.
        -After each valid move, use the method TOAHModel.__str__ that we've
        provided to print a representation of the current state of the game.
        """
        show_instruction()
        won_message = False
        toah = TOAHModel(self.number_of_stools)
        model = toah.get_move_seq(). \
            generate_toah_model(self.number_of_stools, self.number_of_cheeses)
        print(model)
        movement = input("Input your move: ")
        while movement != "end":
            try:
                result = extract_input(movement)
                move(model, result[0], result[1])
            except IllegalMoveError as message:
                print(message)
            except ValueError:
                print('This is a invalid input')
            except IndexError:
                print('This is a invalid input')
            except TypeError:
                print('This is a invalid input')
            else:
                print(model)
            if len(model.get_stool()[-1]) == self.number_of_cheeses:
                movement = "end"
                won_message = True
            else:
                movement = input("Input your move: ")
        display_won_message(won_message)


if __name__ == '__main__':
    # You should initiate game play here. Your game should be playable by
    # running this file.
    game_scene = ConsoleController(3, 4)
    game_scene.play_loop()
    # # Leave lines below as they are, so you will know what python_ta checks.
    # You will need consolecontroller_pyta.txt in the same folder.
    import python_ta
    python_ta.check_all(config="consolecontroller_pyta.txt")
