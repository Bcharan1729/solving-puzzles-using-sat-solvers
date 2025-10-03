"""
Sokoban Solver using SAT (Boilerplate)
--------------------------------------
Instructions:
- Implement encoding of Sokoban into CNF.
- Use PySAT to solve the CNF and extract moves.
- Ensure constraints for player movement, box pushes, and goal conditions.

Grid Encoding:
- 'P' = Player
- 'B' = Box
- 'G' = Goal
- '#' = Wall
- '.' = Empty space
"""

from pysat.formula import CNF
from pysat.solvers import Solver

# Directions for movement
DIRS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}


class SokobanEncoder:
    def __init__(self, grid, T):
        """
        Initialize encoder with grid and time limit.

        Args:
            grid (list[list[str]]): Sokoban grid.
            T (int): Max number of steps allowed.
        """
        self.grid = grid
        self.T = T
        self.N = len(grid)
        self.M = len(grid[0])
        self.goals = []
        self.boxes = []
        self.walls=[]
        self.player_start = None

        # TODO: Parse grid to fill self.goals, self.boxes, self.player_start
        self._parse_grid()

        self.num_boxes = len(self.boxes)
        self.cnf = CNF()

    def _parse_grid(self):
        """Parse grid to find player, boxes, and goals."""
        # TODO: Implement parsing logic
        for i in range(0,self.N):
            for j in range(0,self.M):
                if(self.grid[i][j]=='B'):
                    self.boxes.append((i)*10+(j))
                if(self.grid[i][j]=='G'):
                    self.goals.append((i)*10+(j))
                if(self.grid[i][j]=='P'):
                    self.player_start=(i)*10+(j)
                if(self.grid[i][j]=='#'):
                    self.walls.append((i)*10+(j))

    # ---------------- Variable Encoding ----------------
    def var_player(self, y, x, t):
        """
        Variable ID for player at (x, y) at time t.
        """
        # TODO: Implement encoding scheme
        if y<0 or y>=self.N or x<0 or x>=self.M:
            return 800
        else:
            return t*1000+1*100+y*10+x
           

    def var_box(self, y, x, t):
        """
        Variable ID for box  at (x, y) at time t.
        """
        # TODO: Implement encoding scheme
        if y<0 or y>=self.N or x<0 or x>=self.M:
            return -800
        else:
            return t*1000+1*200+y*10+x
    
    def var_wall(self,y,x,t):

        return t*1000+3*100+y*10+x

    # ---------------- Encoding Logic ----------------
    def encode(self):
        """
        Build CNF constraints for Sokoban:
        - Initial state
        - Valid moves (player + box pushes)
        - Non-overlapping boxes
        - Goal condition at final timestep
        """
        # TODO: Add constraints for:
        # 1. Initial conditions
        #a=[b+100 for b in self.walls]
        #c=[d+200 for d in self.walls]
        #self.cnf.append(-a)
        #self.cnf.append(-c)
        self.cnf.append([-800])
        #print("player_start:") 
        #print(self.player_start)
        #print("boxes:")
        #print(self.boxes)
        #print("goals:")
        #print(self.goals)
        #print("walls:")
        #print(self.walls)
        #print(self.cnf.clauses)
        
        if(len(self.walls)):
            for t in range(0,self.T+1): 
                for x in self.walls :
                           #assigning the walls as true(wher # is ther in the given grid) in every step 
                    self.cnf.append([t*1000+300+x])

        print(self.cnf.clauses)

        for i in range(0,self.M):
            for j in range(0,self.N):
                if i*10+j in self.boxes:
                    self.cnf.append([i*10+j+200])
                else:
                    self.cnf.append([-200-i*10-j])
                if (i*10+j)==self.player_start:
                    self.cnf.append([100+i*10+j])
                else:
                    self.cnf.append([-100-i*10-j])


        print(self.cnf.clauses)

        #for i in range(0,self.N):
         #   for j in range(0,self.M):
          #      if(i*10+j!=self.player_start):
           #         self.cnf.append([-i*10-j-100])
        # 2. Player movement
        #movement of the player it depends only on the player position for now does not depends on box or any walls
        #its like if P(i,j) is true then in next step P(i+1,j) or P(i-1,j) or P(i,j+1) or P(i,j-1) or P(i,j) will be true
        for t in range(0,self.T):           
            for i in range(0,self.N):
                for j in range(0,self.M):
                    self.cnf.append([self.var_player(i,j,t+1),self.var_player(i+1,j,t+1),self.var_player(i-1,j,t+1),self.var_player(i,j+1,t+1),self.var_player(i,j-1,t+1),-self.var_player(i,j,t)])  
            if len(self.walls):
                for x in self.walls:
                    self.cnf.append([-((t+1)*1000+100+x)])
            
        
        

        
        #print(self.cnf.clauses)
        # 3. Box movement (push rules)
        for t in range(0,self.T):
            for i in range(0,self.N):
                for j in range(0,self.M):
                    B=[]
                    """for l in {self.var_box(i+1,j,t),self.var_player(i+2,j,t),self.var_player(i+1,j,t+1),-self.var_box(i,j,t)}:
                        for m in {self.var_box(i-1,j,t),self.var_player(i-2,j,t),self.var_player(i-1,j,t+1),-self.var_box(i,j,t)}:
                            for o in {self.var_box(i,j+1,t),self.var_player(i,j+2,t),self.var_player(i,j+1,t+1),-self.var_box(i,j,t)}:
                                for p in {self.var_box(i,j-1,t),self.var_player(i,j-2,t),self.var_player(i,j-1,t+1),-self.var_box(i,j,t)}:
                                    B.append([l,m,p,o])
                    for k in range(0,len(B)):
                        self.cnf.append([-self.var_box(i,j,t+1),self.var_box(i,j,t)]+B[k])
                    for k in range(0,len(B)):
                        self.cnf.append([-self.var_box(i,j,t+1),-self.var_player(i,j,t+1)]+B[k])"""
                    for l in {self.var_box(i+1,j,t+1),self.var_player(i-1,j,t),-self.var_box(i+1,j,t),self.var_player(i,j,t+1)}:
                        for m in {self.var_box(i-1,j,t+1),self.var_player(i+1,j,t),-self.var_box(i-1,j,t),self.var_player(i,j,t+1)}:
                            for n in {self.var_box(i,j-1,t+1),self.var_player(i,j+1,t),-self.var_box(i,j-1,t),self.var_player(i,j,t+1)}:
                                for o in {self.var_box(i,j+1,t+1),self.var_player(i,j-1,t),-self.var_box(i,j+1,t),self.var_player(i,j,t+1)}:
                                    B.append([l,m,n,o])
                    for k in range(0,len(B)):
                        self.cnf.append([-self.var_box(i,j,t),self.var_box(i,j,t+1)]+B[k])
                    C=[]
                    for l in {self.var_box(i,j,t+1),self.var_box(i+1,j,t),self.var_player(i+2,j,t),self.var_player(i+1,j,t+1)}:
                        for m in {self.var_box(i,j,t+1),self.var_box(i-1,j,t),self.var_player(i-2,j,t),self.var_player(i-1,j,t+1)}:
                            for n in {self.var_box(i,j,t+1),self.var_box(i,j-1,t),self.var_player(i,j-2,t),self.var_player(i,j-1,t+1)}:
                                for o in {self.var_box(i,j,t+1),self.var_box(i,j+1,t),self.var_player(i,j+2,t),self.var_player(i,j+1,t+1)}:
                                    C.append([l,m,n,o])
                    for k in range(0,len(C)):
                        self.cnf.append([self.var_box(i,j,t),-self.var_box(i,j,t+1)]+C[k])
                    
        # 4. Non-overlap constraints
        for t in range(0,self.T):
            for i in range(0,self.N):
                for j in range(0,self.M):
                    self.cnf.append([-self.var_player(i,j,t+1),-self.var_box(i,j,t+1)])
                    if (10*i+j in self.walls):
                        self.cnf.append([-self.var_wall(i,j,t+1),-self.var_box(i,j,t+1)])

        for t in range (0,self.T+1):              #no two cells can have player simultaneously
            for i in range(0,self.M*10+self.N):
                for j in range(i+1,self.M*10+self.N):
                    if (i%10>self.N-1 or j%10>self.N-1) :
                        continue
                    self.cnf.append([-t*1000-100-i,-t*1000-100-j])

        # 5. Goal conditions
            for x in self.goals:
                self.cnf.append([self.T*1000+2*100+x])
        # 6. Other conditions
        return self.cnf
        


def decode(model, encoder):
    """
    Decode SAT model into list of moves ('U', 'D', 'L', 'R').

    Args:
        model (list[int]): Satisfying assignment from SAT solver.
        encoder (SokobanEncoder): Encoder object with grid info.

    Returns:
        list[str]: Sequence of moves.
    """
    N, M, T = encoder.N, encoder.M, encoder.T
    n=encoder.num_boxes
    goals=encoder.goals

    # TODO: Map player positions at each timestep to movement directions
    current_position=[]
    for t in range(0,T+1):
        for i in range(0,N):
            for j in range(0,M):
                if(model[t*1000+100+i*10+j-1]>0):
                    current_position.append([i,j])
    print(current_position)
    player=[]
    boxes=[]
    for x in model:
        if abs(x)%1000-100>=0 and abs(x)%1000-100<100 and x>0:
            player.append(x)
        if abs(x)%1000-200>=0 and abs(x)%1000-200<100 and x>0:
            boxes.append(x)  
    ans=0
    ANS=[]
    for x in range(0,T+1):
        alpha=0
        for i in range(0,len(boxes)):
            if boxes[i]-boxes[i]%1000==x*1000:
                print(boxes[i])
                if boxes[i]%100  in goals:
                    alpha=alpha+1
        if alpha==n:
            ans=x
            break
    for i in range(0,ans):
        if (player[i]-player[i+1])%10==0:
            if player[i]%100>player[i+1]%100:
                ANS.append("U")
            else :
                ANS.append("D")
        else:
            if player[i]%100>player[i+1]%100:
                ANS.append("L")
            else:
                ANS.append("R")
    #return ANS
    print(ANS)


def solve_sokoban(grid, T):
    """
    DO NOT MODIFY THIS FUNCTION.

    Solve Sokoban using SAT encoding.

    Args:
        grid (list[list[str]]): Sokoban grid.
        T (int): Max number of steps allowed.

    Returns:
        list[str] or "unsat": Move sequence or unsatisfiable.
    """
    encoder = SokobanEncoder(grid, T)
    cnf = encoder.encode()

    with Solver(name='g3') as solver:
        solver.append_formula(cnf)
        print("start")
        print(len(encoder.cnf.clauses))
        if not solver.solve():
            print("not solve")
            return -1

        model = solver.get_model()
        if not model:
            print("not model")
            return -1
        print("decode")
        #print(model)
        return decode(model, encoder)
    
def parse_input(input_path):
    with open(input_path) as f:
        first_line = f.readline().strip().split()
        T = int(first_line[0])
        board = []
        for line in f:  # reads until EOF
            row = line.strip().split()
            if row:  # skip empty lines if any
                board.append(row)
    return board, T

Parse=parse_input("./inputs1/testcase3.txt")
print(Parse)
solve_sokoban(Parse[0],Parse[1])
    
