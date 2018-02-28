"""
PlatformView: A visible Cheese or stool, which a cheese can sit on top of.
CheeseView: A visible Cheese object represented as a PlatformView.
StoolView: A visible stool.

Each PlatformView instance receives a Canvas instance. The Canvas class is a
class in the tkinter framework. The class is used for a place in a window
to draw shapes.

PlatformView objects draw themselves as rectangles on the canvas, to represent
side views of stools or rounds of cheese with particular sizes.

CheeseView objects can be moved and highlighted.
Note that CheeseView inherits from both Cheese and PlatformView

PlatformView objects receive a function to call in order to report to some
UI object (e.g. GUIController) that their rectangle was clicked on.
"""


# Copyright 2013, 2014, 2017, Gary Baumgartner, Dustin Wehr,
# Danny Heap, Bogdan Simion, Jacqueline Smith, Dan Zingaro, Yuan Xu
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


from tkinter import Canvas
from toah_model import Cheese


class PlatformView:
    """ Visible slab, could be a Cheese or Stool

    === Attributes ===
    @param Canvas canvas: tkinter class for drawing
    @param float thickness: vertical extent of platform
    """

    def __init__(self, width, click_handler, canvas,
                 thickness, x_center, y_center):
        """ Create a new PlatformView

        @param PlatformView self:
        @param float width:
            width in pixels of view
        @param function click_handler:
            function to react to mouse clicks
        @param Canvas canvas:
            space to draw on
        @param float thickness:
            vertical extent of platform
        @param float x_center:
            horizontal center of this platform
        @param float y_center:
            vertical center of platform
        """

        self.canvas = canvas
        self._width = width
        self.x_center = x_center
        self.y_center = y_center
        self.thickness = thickness

        # Create a rectangle on the canvas, and record the index that tkinter
        # uses to refer to it.
        self.index = canvas.create_rectangle(0, 0, 0, 0)
        self.canvas.itemconfigure(self.index)

        # Initial placement.
        self.place(x_center, y_center)

        # Tell the canvas to report when the rectangle is clicked.
        # The report is a call to click_handler, passing it this CheeseView
        # instance so the controller knows which one was clicked.
        self.canvas.tag_bind(self.index,
                             '<ButtonRelease>',
                             lambda _: click_handler(self))

    def place(self, x_center, y_center):
        """ Place rectangular image of this cheese/stool at (x_center, y_center)

        @param PlatformView self:
        @param float x_center:
            horizontal center of platform
        @param float y_center:
            vertical center of platform
        @rtype: None
        """
        # corners are half of size or thickness away
        self.canvas.coords(self.index,
                           round(x_center - self._width/2),
                           round(y_center - self.thickness/2),
                           round(x_center + self._width/2),
                           round(y_center + self.thickness/2))
        # record new center
        self.x_center = x_center
        self.y_center = y_center


class CheeseView(Cheese, PlatformView):
    """
    A visible Cheese
    """

    def __init__(self, size, width, click_handler, canvas, thickness,
                 x_center, y_center):
        """ Initialize a new CheeseView.

        @type self: CheeseView
        @type size: int
            relative size of cheese, with 1 smallest
        @type width: float
            horizontal extent of cheese, in pixels
        @type click_handler: function
            function to react to mouse clicks
        @type canvas: Canvas
            space to draw cheese on
        @type thickness: float
            vertical extent of cheese
        @type x_center: float
            horizontal center of cheese
        @type y_center: float
            vertical center or cheese
        """
        PlatformView.__init__(self, width, click_handler, canvas, thickness,
                              x_center, y_center)
        Cheese.__init__(self, size)

        # Initially unhighlighted.
        self.highlight(False)

    def highlight(self: 'CheeseView', highlighting: bool):
        """Set this CheeseView's colour to highlighted or not.

           highlighting - whether to highlight"""

        self.canvas.itemconfigure(self.index,
                                  fill=('red' if highlighting else 'orange'))


class StoolView(PlatformView):
    """ A visible Stool
    """

    def __init__(self, width, click_handler, canvas, thickness,
                 x_center, y_center):
        """ Create a new StoolView

        @type self: StoolView
        @type width: float
        @type click_handler: function
        @type canvas: Canvas
        @type thickness: float
        @type x_center: float
        @type y_center: float
        """
        PlatformView.__init__(self, width, click_handler, canvas, thickness,
                              x_center, y_center)
        self.canvas.itemconfigure(self.index, fill='black')


if __name__ == "__main__":
    # Leave lines below to see what python_ta checks.
    # File guiviewables_pyta.txt must be in same folder.
    import python_ta
    python_ta.check_all(config="guiviewables_pyta.txt")
