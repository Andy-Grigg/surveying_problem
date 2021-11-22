""" Display a grid on the terminal using box drawing symbols"""

import colorama

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


def display_set_as_grid(grid):
    """Render the grid. Relies on a fixed-width font."""

    if grid.size > 100:
        print("Too big to render!")
        return

    # Use the size of the grid to figure out how much to pad row and column indices by
    num_chars_in_label = len(str(grid.size))

    # Generate column headers
    print(
        TOP_LEFT_CHAR
        + (HORIZ_CHAR * num_chars_in_label + TOP_CHAR) * grid.size
        + HORIZ_CHAR * num_chars_in_label
        + TOP_RIGHT_CHAR
    )
    column_heading_numbers = [
        str(y).zfill(num_chars_in_label) for y in list(range(0, grid.size))
    ]
    header = VERTICAL_CHAR.join(column_heading_numbers) + VERTICAL_CHAR
    print(VERTICAL_CHAR + " " * num_chars_in_label + VERTICAL_CHAR + header)

    cell_separator = VERTEX_CHAR + HORIZ_CHAR * (num_chars_in_label)
    row_divider = (
        LEFT_CHAR
        + HORIZ_CHAR * (num_chars_in_label)
        + cell_separator * grid.size
        + RIGHT_CHAR
    )

    print(row_divider)

    # Initialize the first row
    row = VERTICAL_CHAR + str(0).zfill(num_chars_in_label) + VERTICAL_CHAR
    current_row = 0

    # TODO: Make this not rely on a particular creation order
    for y_coord in list(range(0, grid.size)):
        for x_coord in list(range(0, grid.size)):
            # TODO: Somehow highlight different wells with different colors
            marker = (
                colorama.Fore.RED + "x" + colorama.Style.RESET_ALL
                if (x_coord, y_coord) in grid.to_set_of_tuples
                else " "
            )
            if y_coord == current_row:
                row = row + marker * num_chars_in_label + VERTICAL_CHAR
            else:
                current_row = y_coord
                print(row)
                print(row_divider)
                row = (
                    VERTICAL_CHAR
                    + str(y_coord).zfill(num_chars_in_label)
                    + VERTICAL_CHAR
                    + marker * num_chars_in_label
                    + VERTICAL_CHAR
                )
    print(row)
    print(
        BOTTOM_LEFT_CHAR
        + (HORIZ_CHAR * num_chars_in_label + BOTTOM_CHAR) * grid.size
        + HORIZ_CHAR * num_chars_in_label
        + BOTTOM_RIGHT_CHAR
    )
