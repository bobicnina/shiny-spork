# shinySpork
FMF LVR 10% : Implementing a SAT Solver

Input: a file in <a href='http://www.satcompetition.org/2009/format-benchmarks2009.html'>DIMACS</a> format specifying a <a href='https://en.wikipedia.org/wiki/Conjunctive_normal_form'>CNF</a> formula

Output: a satisfying valuation (saved in the format illustrated by the examples in the Homework Files directory on the <a href='https://ucilnica.fmf.uni-lj.si/course/view.php?id=252at-benchmarks2009.html'>course webpage</a>) or  single entry 0 (zero). This signals that the program has not found a solution. (It need not mean that the input formula is unsatisfiable.) 

Folder Test Files contains example test files for SAT solvers. The input files are: sudoku_mini.txt, sudoku_hard.txt, sudoku_easy.txt and graph_colouring.txt. For each input file there is a corresponding _solution file containing
a satisfying valuation.

mysolver.py 'inputfilename.txt' 'outputfilename.txt' will run the solver on input file inputfilename.txt and will write its output in the file outputfilename.txt
