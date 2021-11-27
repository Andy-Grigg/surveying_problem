import colorama
import lxml.etree as ET

from src.model import GridModel


class GridView:
    TOP_LEFT_CHAR = u"\u250c"
    TOP_RIGHT_CHAR = u"\u2510"
    TOP_CHAR = u"\u252c"
    BOTTOM_LEFT_CHAR = u"\u2514"
    BOTTOM_RIGHT_CHAR = u"\u2518"
    BOTTOM_CHAR = u"\u2534"
    LEFT_CHAR = u"\u251c"
    RIGHT_CHAR = u"\u2524"
    VERTICAL_CHAR = u"\u2502"
    HORIZ_CHAR = u"\u2500"
    VERTEX_CHAR = u"\u253c"

    def __init__(self, grid: GridModel):
        self._grid = grid

    @property
    def size(self):
        return self._grid.size

    @property
    def number_of_sites(self) -> int:
        return len(self._grid.cells)

    @property
    def density(self) -> float:
        return self.number_of_sites / (self.size * self.size)

    @property
    def location_probability(self):
        return self._grid.location_probability

    @property
    def seed(self):
        return self._grid.seed

    def get_neighbors(self, grid_element):
        return self._grid.get_neighbors(grid_element)

    def get_reservoirs(self):
        return self._grid.find_reservoirs()

    @property
    def to_xml(self) -> ET.Element:
        root = ET.Element("grid")
        sortable_grid = list(self._grid.cells)
        sortable_grid.sort()
        for location in sortable_grid:
            y_element = ET.Element("y")
            x_element = ET.Element("x")
            x_element.text, y_element.text = map(str, location)
            location_element = ET.Element("el")
            location_element.extend([x_element, y_element])
            root.append(location_element)
        return root

    def to_ascii_art(self):
        """Render the grid. Relies on a fixed-width font."""

        if self._grid.size > 100:
            print("Too big to render!")
            return

        # Use the size of the grid to figure out how much to pad row and column indices by
        num_chars_in_label = len(str(self._grid.size))

        # Generate column headers
        print(
            self.TOP_LEFT_CHAR
            + (self.HORIZ_CHAR * num_chars_in_label + self.TOP_CHAR) * self._grid.size
            + self.HORIZ_CHAR * num_chars_in_label
            + self.TOP_RIGHT_CHAR
        )
        column_heading_numbers = [
            str(y).zfill(num_chars_in_label) for y in list(range(0, self._grid.size))
        ]
        header = self.VERTICAL_CHAR.join(column_heading_numbers) + self.VERTICAL_CHAR
        print(
            self.VERTICAL_CHAR + " " * num_chars_in_label + self.VERTICAL_CHAR + header
        )

        cell_separator = self.VERTEX_CHAR + self.HORIZ_CHAR * num_chars_in_label
        row_divider = (
            self.LEFT_CHAR
            + self.HORIZ_CHAR * num_chars_in_label
            + cell_separator * self._grid.size
            + self.RIGHT_CHAR
        )

        print(row_divider)

        # Initialize the first row
        row = self.VERTICAL_CHAR + str(0).zfill(num_chars_in_label) + self.VERTICAL_CHAR
        current_row = 0

        # TODO: Make this not rely on a particular creation order
        for y_coord in list(range(0, self._grid.size)):
            for x_coord in list(range(0, self._grid.size)):
                # TODO: Somehow highlight different wells with different colors
                marker = (
                    colorama.Fore.RED + "x" + colorama.Style.RESET_ALL
                    if (x_coord, y_coord) in self._grid.cells
                    else " "
                )
                if y_coord == current_row:
                    row = row + marker * num_chars_in_label + self.VERTICAL_CHAR
                else:
                    current_row = y_coord
                    print(row)
                    print(row_divider)
                    row = (
                        self.VERTICAL_CHAR
                        + str(y_coord).zfill(num_chars_in_label)
                        + self.VERTICAL_CHAR
                        + marker * num_chars_in_label
                        + self.VERTICAL_CHAR
                    )
        print(row)
        print(
            self.BOTTOM_LEFT_CHAR
            + (self.HORIZ_CHAR * num_chars_in_label + self.BOTTOM_CHAR)
            * self._grid.size
            + self.HORIZ_CHAR * num_chars_in_label
            + self.BOTTOM_RIGHT_CHAR
        )

    def __str__(self) -> str:
        return str(self._grid)
