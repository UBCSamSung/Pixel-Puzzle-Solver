# Pixel Puzzle Solver
## Goal: Create a solver for Pixel Puzzle
* Introduction:
    * [Pixel Puzzle](https://en.wikipedia.org/wiki/Nonogram) (also known as "*Nonogram*") is an interesting puzzle game where player is challenged to find all the boolean assignment in a n by n grid with clues indicating the number of consecutive truth assignment in the corresponding row/column
    * Here, I demostrate three incrementally optimized approaches to solving such puzzle as well as the technical difficulty at each stage. 
    * [Here](https://www.puzzle-nonograms.com/) is a example of web-based pixel puzzle you can try out
    * To try out one of the sample puzzle, run `python solver_C < input/medium.txt` at `\Pixel Puzzle Solver` directory
* Requirement:
    * Python 3.7.1
    * Tkinter
    * Numpy
1. Solver A: **Brute force** solver
    * Classic **brute force** solver similiar to Sudoku solver
    * Iterate every possible state by backtracking
    * Computational complexity: 2^(n*n) where n is size of puzzle
    * Computationally infeasible when grid size is **5** or more
```
Sample output:
>python solver_A.py < puzzles/easy2.txt
rowHint:
[[1], [1], [3]]
colHint:
[[1], [3], [1]]
solved board:
[[0. 1. 0.]
 [0. 1. 0.]
 [1. 1. 1.]]
iterations: 41
```
2. Solver B: [**WalkSat**](https://en.wikipedia.org/wiki/WalkSAT) Approach
    * Convert the problem into **satisfactory problem** and solve with **stochastic local search**
    * Treat each clue as a **constraint** clause
    * Treat each cell as an atom **assignment**
    * Optimized by perform basic deduction on obvious pattern
        * eg. for each given line, when clue is [9] in n=10 puzzle, we can deduce that all but the first and last cell must be assigned value of 1
    * 90% greedy 10% random seems to be good mix of greediness
    * Computationally infeasible when grid size is **10** or more
 ```
 Sample output:
iteration: 1867
min unsatisfied predicates: 0
current board:
[[0 0 1 1 1 1 1 1 0 0]
 [0 1 1 0 0 0 0 1 1 0]
 [1 1 0 0 0 0 0 0 1 1]
 [1 0 1 0 0 0 1 1 0 1]
 [1 1 1 1 1 1 0 1 0 1]
 [1 1 0 0 0 1 1 1 0 1]
 [1 0 0 0 0 1 0 0 1 1]
 [1 0 0 1 1 0 0 0 1 0]
 [1 1 0 1 1 0 0 1 1 0]
 [0 1 1 0 0 0 1 1 0 0]]
solved board:
[[0 0 1 1 1 1 1 1 0 0]
 [0 1 1 0 0 0 0 1 1 0]
 [1 1 0 0 0 0 0 0 1 1]
 [1 0 1 0 0 0 1 1 0 1]
 [1 1 1 1 1 1 0 1 0 1]
 [1 1 0 0 0 1 1 1 0 1]
 [1 0 0 0 0 1 0 0 1 1]
 [1 0 0 1 1 0 0 0 1 0]
 [1 1 0 1 1 0 0 1 1 0]
 [0 1 1 0 0 0 1 1 0 0]]
 ```
 3. Solver C: **Human-assisted Walksat** Approach
    * Extension of Solver B with **TkInter** interface to allow manual correction during local search
    * Control:
        1. Left click a cell to mark it as **True**
        1. Right click a cell to mark it as **False**
        1. Middle click a cell to mark it as **Unsure**
    * Rationale:
        * The deduction logic required in Pixel Puzzle is non-trivial to implement but is trivial for average puzzle solver. See [Solving Pixel Puzzle Using Rule-Based Techniques and Best First Search](https://www.researchgate.net/publication/232648861_Solving_Pixel_Puzzle_Using_Rule-Based_Techniques_and_Best_First_Search) for such implementation
        * Therefore, we can reduce [**search space**](https://en.wikipedia.org/wiki/Search_space) by perform [easy deduction](https://en.wikipedia.org/wiki/Nonogram#Solution_techniques) at human level 
        * The algorithm perform stochastic local search **simutaneously** with user utilizing the [**anytime**](https://en.wikipedia.org/wiki/Anytime_algorithm) property of WalkSat algorithm.
    * Able to solve puzzles unsolvable by Solver A and Solver B
    * Demo (n=10):
    
    ![Demo](/demo/size_10_fast.gif)
    * Demo (n=15 with manual correction):
    
    ![Demo2](/demo/size_15_fast.gif)