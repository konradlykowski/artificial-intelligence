from collections import defaultdict

import re

rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a, b):
    return [s + t for s in a for t in b]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units_left = [[(rows[len(rows) - i - 1] + cols[i]) for i in range(8, -1, -1)]]
diagonal_units_right = [[(rows[i] + cols[i]) for i, _ in enumerate(rows)]]
diagonal_units = diagonal_units_left + diagonal_units_right
unitlist = row_units + column_units + square_units + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

units_row = dict((s, [u for u in row_units if s in u]) for s in boxes)
peers_row = dict((s, set(sum(units_row[s], [])) - set([s])) for s in boxes)

units_column = dict((s, [u for u in column_units if s in u]) for s in boxes)
peers_column = dict((s, set(sum(units_column[s], [])) - set([s])) for s in boxes)

units_square = dict((s, [u for u in square_units if s in u]) for s in boxes)
peers_square = dict((s, set(sum(units_square[s], [])) - set([s])) for s in boxes)

units_diagonal_right = dict((s, [u for u in diagonal_units_right if s in u]) for s in boxes)
peers_diagonal_right = dict((s, set(sum(units_diagonal_right[s], [])) - set([s])) for s in boxes)

units_diagonal_left = dict((s, [u for u in diagonal_units_left if s in u]) for s in boxes)
peers_diagonal_left = dict((s, set(sum(units_diagonal_left[s], [])) - set([s])) for s in boxes)

assignments = []


def naked_twins(values):
    """
    Iterate find_naked_twins() and naked_twins_eliminate().
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.

    :param values: The sudoku in dictionary form
    :return: The sudoku in dictionary form
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        for start_box in [box for box in values.keys() if len(values[box]) == 2]:
            for one_dimension_peers in [peers_column, peers_row, peers_square]:
                find_naked_twins(start_box, values, one_dimension_peers)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after

    return values


def find_naked_twins(start_box, values, one_dimension_peers):
    """
    Find naked twins and remove them from boxes. Operation done only for one type of peers (ie. search only columns)
    Input:
    :param start_box: Starting point
    :param values: The sudoku in dictionary form
    :param one_dimension_peers: Predefined peers - for example columns, rows, squares
    :return: None
    """
    reverted_index_values = defaultdict()
    reverted_index_values[values[start_box]] = reverted_index_values.get(values[start_box], []) + [start_box]
    for peer in [peer for peer in one_dimension_peers[start_box] if len(values[peer]) == 2]:
        reverted_index_values[values[peer]] = reverted_index_values.get(values[peer], []) + [peer]

    naked_twin = [naked_twin for naked_twin in reverted_index_values.keys() if
                  len(reverted_index_values[naked_twin]) > 1]
    naked_twins_eliminate(start_box, naked_twin, one_dimension_peers, values)


def naked_twins_eliminate(start_box, naked_twin, one_dimension_peers, values):
    """
    Remove naked_twins within all other boxes from one_dimension_peer
    :param start_box: starting point
    :param naked_twin: naked twin to compare with others
    :param one_dimension_peers: One dimensional peer (ie just column)
    :param values: The sudoku in dictionary form
    :return:
    """
    for naked in naked_twin:
        for peer in one_dimension_peers[start_box]:
            if values[peer] != naked:
                values[peer] = re.sub(naked[0] + "|" + naked[1], '', values[peer])


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """
    BFS implementation for traverse the sudoku movement tree
    :param values: A sudoku in dictionary form.
    :return: A sudoku in dictionary form or boolean if failed
    """
    values = reduce_puzzle(values)
    if values is False:
        return False  ## Failed earlier

    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
