# shinySpork
FMF LVR 10% : Implementing a SAT Solver

Input: a file in <a href='http://www.satcompetition.org/2009/format-benchmarks2009.html'>DIMACS</a> format specifying a <a href='https://en.wikipedia.org/wiki/Conjunctive_normal_form'>CNF</a> formula

Output: a satisfying valuation (saved in the format illustrated by the examples in the Homework Files directory on the <a href='https://ucilnica.fmf.uni-lj.si/course/view.php?id=252at-benchmarks2009.html'>course webpage</a>) or  single entry 0 (zero). This signals that the program has not found a solution. (It need not mean that the input formula is unsatisfiable.) 

Efficiency of SAT solver is improved by modifying the search strategy. At point, where we have to set value for variable, algorithm selects the variable that occurs most often.

Folder Test Files contains example test files for SAT solvers. The input files are: sudoku_mini.txt, sudoku_hard.txt, sudoku_easy.txt and graph_colouring.txt. For each input file there is a corresponding _solution file containing
a satisfying valuation.

How to use SAT solver?
<code>shinySpork.py 'inputfilename.txt' 'outputfilename.txt'</code> will run the solver on input file inputfilename.txt and will write its output in the file <code>outputfilename.txt</code> 
Generate solution and save it to DIMACS format and check if generated solution is correct. It is also possible to run it in script as <code>status, _ = shinySpork(problem, solution)</code> In case that solution file does not exists, SAT solver will write solution to given file.
Example:
<pre><code>python3 shinySpork.py 'TestFiles/graph_colouring.txt'
python3 shinySpork.py 'TestFiles/graph_colouring.txt' 'TestFiles/graph_colouring_solution.txt'
status, _ = shinySpork('TestFiles/graph_colouring.txt','TestFiles/graph_colouring_solution.txt')</code></pre>
