"""
sudoku_solver.py

Implement the function `solve_sudoku(grid: List[List[int]]) -> List[List[int]]` using a SAT solver from PySAT.
"""

from pysat.formula import CNF
from pysat.solvers import Solver
from typing import List
import random

def solve_sudoku(grid: List[List[int]]) -> List[List[int]]:
    """Solves a Sudoku puzzle using a SAT solver. Input is a 2D grid with 0s for blanks."""
    cnf = CNF()
    for i in range(1,10) :
        for n in range(1,10) :
            cnf.append(list(range(100*i+n+10,100*i+n+100,10)))

    for j in range(1,10) :
        for n in range(1,10) :
            cnf.append(list(range(10*j+n+100,10*j+n+1000,100)))

    for i in range(1,10) :
        for j in range(1,10) :
            for x in range(1,10) :
                for y in range(x+1,10):
                    cnf.append([-(100*i+10*j+x),-(100*i+10*j+y)])
    for i in {1,4,7}:
        for j in {1,4,7}:
            for k in range(1,10):        
                cnf.append([i*100+j*10+k,i*100+(j+1)*10+k,i*100+(j+2)*10+k,(i+1)*100+j*10+k,(i+1)*100+(j+1)*10+k,(i+1)*100+(j+2)*10+k,(i+2)*100+j*10+k,(i+2)*100+(j+1)*10+k,(i+2)*100+(j+2)*10+k])

    for i in range(1,10):
        for j in range(1,10):
            if(grid[i-1][j-1]!=0):
                cnf.append([i*100+j*10+grid[i-1][j-1]])

    with Solver(name='glucose3') as solver:
        solver.append_formula(cnf.clauses)
        if solver.solve():
            model = solver.get_model()
        else :
            print("unsat")
    for i in range(1,10):
            for j in range(1,10):
                for k in range(1,10):
                    if model[i*100+j*10+k-1]>0:
                        grid[i-1][j-1]=k

    return grid
        



    # TODO: implement encoding and solving using PySAT
    