import colorama
import lxml.etree as ET

from src.model import GridModel, Cell


class GridView:
    def __init__(self, grid: GridModel):
        self._grid = grid

    def __str__(self) -> str:
        return str(self._grid)

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

        # Use the size of the grid to figure out how much to pad row and column indices by
        ascii_table = AsciiGrid(self._grid.cells, self._grid.size).draw()
        print(ascii_table)


class AsciiGrid:
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
    NEWLINE = "\n"

    def __init__(self, grid: set[Cell], grid_size: int, horizontal_lines: bool = False):
        self.cells = grid
        self.grid_size = grid_size
        self.coord_list = list(range(0, self.grid_size))  # Square grid only, so a single list of coords
        self.num_chars_in_label = len(str(grid_size - 1))
        self.horizontal_lines = horizontal_lines

    def draw(self) -> str:
        if self.grid_size > 100:
            return "Too big to render!"

        result = self._top_row()
        result += "".join([self._data_row(row_number) for row_number in self.coord_list])
        result += self._bottom_line()
        return result

    def _top_row(self) -> str:
        return self._top_line() + self.NEWLINE + self._table_header() + self.NEWLINE

    def _top_line(self) -> str:
        top_line = (
            self.TOP_LEFT_CHAR
            + (self.HORIZ_CHAR * self.num_chars_in_label + self.TOP_CHAR) * self.grid_size
            + self.HORIZ_CHAR * self.num_chars_in_label
            + self.TOP_RIGHT_CHAR
        )
        return top_line

    def _table_header(self) -> str:
        column_heading_numbers = [
            str(y).zfill(self.num_chars_in_label) for y in list(range(0, self.grid_size))
        ]
        column_headings = self.VERTICAL_CHAR.join(column_heading_numbers) + self.VERTICAL_CHAR
        header = self.VERTICAL_CHAR + " " * self.num_chars_in_label + self.VERTICAL_CHAR + column_headings
        return header

    def _row_divider(self) -> str:
        cell_separator = self.VERTEX_CHAR + self.HORIZ_CHAR * self.num_chars_in_label
        row_divider = (
                self.LEFT_CHAR
                + self.HORIZ_CHAR * self.num_chars_in_label
                + cell_separator * self.grid_size
                + self.RIGHT_CHAR
        )
        return row_divider

    def _data_row(self, row_number: int) -> str:
        if row_number == 0 or self.horizontal_lines:
            row = self._row_divider() + self.NEWLINE
        else:
            row = ""
        row += self.VERTICAL_CHAR + str(row_number).zfill(self.num_chars_in_label) + self.VERTICAL_CHAR
        for column_number in self.coord_list:
            row += self._cell(column_number, row_number) * self.num_chars_in_label + self.VERTICAL_CHAR
        return row + self.NEWLINE

    def _cell(self, x_coord, y_coord) -> str:
        # TODO: Somehow highlight different wells with different colors
        marker = (
            colorama.Fore.RED + "x" + colorama.Style.RESET_ALL
            if (x_coord, y_coord) in self.cells
            else " "
        )
        return marker

    def _bottom_line(self) -> str:
        return(
            self.BOTTOM_LEFT_CHAR
            + (self.HORIZ_CHAR * self.num_chars_in_label + self.BOTTOM_CHAR)
            * self.grid_size
            + self.HORIZ_CHAR * self.num_chars_in_label
            + self.BOTTOM_RIGHT_CHAR
        )
