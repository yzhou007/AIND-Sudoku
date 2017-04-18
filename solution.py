import itertools

assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [x + y for x in A for y in B]


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag1_units = [r + c for r, c in zip(rows, cols)]
diag2_units = [r + c for r, c in zip(rows, cols[::-1])]
diag_units = [diag1_units, diag2_units] # get the diagonal units
unitlist = row_units + column_units + square_units + diag_units # add the diagonal units to unitlist
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        # Get all boxes that have two digits in the unit
        pairs = [box for box in unit if len(values[box]) == 2]
        
        # Creat a list of possible twin pairs in the unit
        twins_possible = [pair for pair in itertools.combinations(pairs, 2)]
        
        # Loop through the list of possibe twins
        for pair in twins_possible:
            box1 = pair[0]
            box2 = pair[1]
            if values[box1] == values[box2]: # Find the naked twins
                for box in unit: 
                    if box != box1 and box != box2:
                        for digit in values[box1]:
                            # Remove the naked twin digits from the peers in the unit
                            assign_value(values, box, values[box].replace(digit,''))
                            
    return values
            
                        
                        
    
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = dict(zip(boxes, grid))
    for box in values:
        if values[box] == '.':
            assign_value(values, box, '123456789') 
    return values;


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_locations = [box for box in boxes if len(values[box]) == 1]
    for box in solved_locations:
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(values[box],''))
            #values[peer] = values[peer].replace(values[box],'')
    return values
    
def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            digit_locations = [box for box in unit if digit in values[box]]
            if len(digit_locations) == 1:
                assign_value(values, digit_locations[0], digit)
                #values[digit_locations[0]] = digit
    return values

def reduce_puzzle(values):
    terminate = False
    while not terminate:
        solved_nums_before = len([box for box in boxes if len(values[box]) == 1])
        values = eliminate(values);
        values = only_choice(values);
        values = naked_twins(values);
        solved_nums_after = len([box for box in boxes if len(values[box]) == 1])
        terminate = solved_nums_before == solved_nums_after
        if len([box for box in values if len(values[box]) == 0]):
            return False
    return values
    

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    
    if all(len(values[box]) == 1 for box in boxes):
        return values
    
    num, pos = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)
    for digit in values[pos]:
        values_copy = values.copy()
        values_copy[pos] = digit
        result = search(values_copy)
        if result:
            return result
    

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values

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
