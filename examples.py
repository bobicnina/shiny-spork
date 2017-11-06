Mini 4*4 Sudoku from lecture
''' print('\t Sudoku 4*4')
status, _ = shinySpork('tests/sudoku_mini.txt','tests/sudoku_mini_solution.txt')
if status is True:
    print('\t We found a satisfying valuation.')
else:
    print('\t Solution is wrong!') '''

Another 9*9 Sudoku puzzle, this time at 'very easy' level
''' print('\tSudoku 9*9')
status, _ = shinySpork("tests/sudoku_easy.txt','tests/sudoku_easy_solution.txt')
if status is True:
    print('\t We found a satisfying valuation.')
else:
    print('\t Solution is wrong!') '''

The 9*9 Sudoku puzzle at 'very hard' level from the lecture
''' print('\t Sudoku 9*9')
status, _ = shinySpork('tests/sudoku_hard.txt','tests/sudoku_hard_solution.txt')
if status is True:
    print('\t We found a satisfying valuation.')
else:
    print('\t Solution is wrong!') '''

Graph 3-colouring
''' print('\t Graph 3-colouring')
status, _ = shinySpork('tests/graph_colouring.txt','tests/graph_colouring_solution.txt')
if status is True:
    print('\t We found a satisfying valuation.')
else:
    print('\t Solution is wrong!') '''
