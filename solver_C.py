# Python 3.7.1

# Human-assisted WalkSat

import numpy as np
import random
import time
import tkinter as tk

def main():
    t=int(input())
    for _ in range(t):
        n=int(input())
        rowHints=[[int(x) for x in input().strip().split()] for _ in range(n)]
        colHints=[[int(x) for x in input().strip().split()] for _ in range(n)]
        solver=Solver(n, rowHints, colHints)
        solver.solve()

class Application(tk.Frame):
    def __init__(self, board, rowHints, colHints, master=None):
        # import images
        self.tile_plain=tk.PhotoImage(file="images/tile_plain.gif")
        self.tile_clicked=tk.PhotoImage(file="images/tile_clicked.gif")
        self.tile_wrong=tk.PhotoImage(file="images/tile_wrong.gif")
        self.tile_flag=tk.PhotoImage(file="images/tile_flag.gif")

        super().__init__(master)
        self.master = master

        # solver related object
        self.board = board
        self.rowHints=rowHints
        self.colHints=colHints
        self.certain_coordinates = set()
        self.decisions = [set(),set(),set()]

        self.pack()
        self.create_widgets()
        self.update()
    
    def create_widgets(self):
        self.label=tk.Label(self, text="Pixel Puzzle Solver")
        self.label.pack(side="top")
        self.iteration=0
        self.iteration_label=tk.Label(self, text="iteration count")
        self.iteration_label.pack(side="top")
        self.grid=self.create_grid()
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.exit)
        self.quit.pack(side="bottom")
    
    def create_grid(self):
        self.cells={}
        grid = tk.Frame(self)
        grid.pack()
        n=self.board.shape[0]
        for i in range(0,n+1):
            for j in range(0,n+1):
                coordinate=(j-1,i-1)
                if coordinate==(-1,-1):
                    continue
                if coordinate[1]==-1:
                    widget=tk.Label(grid, text=self.rowHints[coordinate[0]])
                    widget.grid(row=coordinate[0]+1,column=coordinate[1]+1)
                    continue
                if coordinate[0]==-1:
                    widget=tk.Label(grid, text='\n'.join(str(x) for x in self.colHints[coordinate[1]]))
                    widget.grid(row=coordinate[0]+1,column=coordinate[1]+1)
                    continue
                widget=tk.Button(grid, image=self.tile_plain)
                widget.bind(sequence="<Button-1>", func=self.left_click_wrapper(coordinate))
                widget.bind(sequence="<Button-2>", func=self.middle_click_wrapper(coordinate))
                widget.bind(sequence="<Button-3>", func=self.right_click_wrapper(coordinate))
                widget.grid(row=coordinate[0]+1,column=coordinate[1]+1)
                button = {
                    "widget":widget,
                    "state":0,
                    "coordinate":coordinate
                }
                self.cells[coordinate]=button
        return grid
    
    def left_click_wrapper(self, coordinate):
        return lambda button:self.left_click(coordinate)

    def left_click(self, coordinate):
        self.decisions[1].add(coordinate)

    def middle_click_wrapper(self, coordinate):
        return lambda button:self.middle_click(coordinate)

    def middle_click(self, coordinate):
        self.decisions[2].add(coordinate)

    def right_click(self, coordinate):
        self.decisions[0].add(coordinate)

    def right_click_wrapper(self, coordinate):
        return lambda button:self.right_click(coordinate)
    

    def update_cells(self):
        n=self.board.shape[0]
        for i in range(n):
            for j in range(n):
                coordinate=(j,i)
                entry=self.board[j,i]
                cell=self.cells[coordinate]
                if coordinate in self.certain_coordinates:
                    cell['state']=entry+2
                else:
                    cell['state']=entry
                self.update_cell(cell)
    
    def update_cell(self, cell):
        state=cell['state']
        widget=cell['widget']
        switcher = {
            0: self.tile_plain,
            1: self.tile_flag,
            2: self.tile_clicked,
            3: self.tile_wrong,
        }
        widget.config(image=switcher[state])
    
    def get_decisions(self):
        decision = self.decisions
        self.certain_coordinates = (self.certain_coordinates | decision[0] | decision[1]) - decision[2]
        self.decisions = [set(),set(),set()]
        return decision
    
    def update(self):
        self.update_cells()
        super().update()
    
    def update_label(self, text):
        self.iteration_label.config(text=text)
    
    def exit(self):
        self.master.destroy()
        self.master=None
    

class Solver():
    def __init__(self, n, rowHints, colHints):
        board=np.random.randint(0,2,[n,n])
        self.n = n
        self.rowHints = rowHints
        self.colHints = colHints
        self.board = board
        self.deduce()
        root = tk.Tk()
        root.title("Pixel Puzzle Solver")
        self.app = Application(master=root, board=board, rowHints=rowHints, colHints=colHints)
        self.app.certain_coordinates = self.certainAtoms
        self.is_quit=False
        time.sleep(10)

    def solve(self):
        board=self.board
        colHints = self.colHints
        rowHints = self.rowHints
        n = self.n
        self.iteration=0
        minUnsatCount=2*n
        while self.is_quit==False:
            self.iteration+=1
            verbose=self.iteration%10==1
            if self.iteration%10000==1:
                print("restart")
                for i in range(n):
                    for j in range(n):
                        if (j,i) not in self.certainAtoms:
                            board[j,i]=random.randint(0,1)
            if verbose:
                self.draw()
                # print("iteration:", self.iteration)
                print("min unsatisfied predicates:", minUnsatCount)
                # print("current board:")
                # print(board)
            pickedAtoms=self.find_unsatisfied_predicate(board, rowHints, colHints)
            if pickedAtoms==None:
                self.draw()
                self.app.update_label("Solved in {} iterations".format(self.iteration))
                self.app.mainloop()
                self.app.update
                return
            pickableAtoms=list(set(pickedAtoms or [])-self.certainAtoms)
            if (pickableAtoms==[]):
                self.app.update_label("Inconsistent")
                self.app.update()
                print("Inconsistent", pickedAtoms)
                continue
            beGreedy=random.choice([1]*9+[0]*1)
            pickedAtom=None
            if beGreedy:
                best_atom_flip, minUnsatCount=self.find_best_atom_flip(board, rowHints, colHints, pickableAtoms)
                if best_atom_flip!=-1:
                    pickedAtom=pickableAtoms[best_atom_flip]
            if pickedAtom==None:
                pickedAtom=random.choice(pickableAtoms)
            y,x=pickedAtom
            board[y,x]=int(not board[y,x])
            # break

    def deduce(self):
        self.certainAtoms = set()
        positiveAtoms=self.positive_deduce(self.n, self.rowHints, self.colHints)
        negativeAtoms=self.negative_deduce(self.n, self.rowHints, self.colHints)
        self.assign_atoms(set(positiveAtoms), set(negativeAtoms), set())

    def positive_deduce(self, n, rowHints, colHints):
        atoms=set()
        for axis, hints in enumerate([colHints, rowHints]):
            for index, hint in enumerate(hints):
                m=max(hint)
                if m>n//2:
                    for i in range(n):
                        if i+m>n-1 and i-m<0:
                            atoms.add((i,index) if axis==0 else (index,i))
        return atoms
    
    def negative_deduce(self, n, rowHints, colHints):
        atoms=set()
        for axis, hints in enumerate([colHints, rowHints]):
            for index, hint in enumerate(hints):
                m=max(hint)
                if m==0:
                    for i in range(n):
                        atoms.add((i,index) if axis==0 else (index,i))
        return atoms

    def find_best_atom_flip(self, board, rowHints, colHints, pickedAtoms):
        bestAtomIndex=-1
        minUnsatCount=self.count_unsatisfied_predicate(board, rowHints, colHints)
        for index, atom in enumerate(pickedAtoms):
            y,x=atom
            board[y,x]=int(not board[y,x])
            currUnsatCount=self.count_unsatisfied_predicate(board,rowHints,colHints)
            if currUnsatCount<minUnsatCount:
                bestAtomIndex=index
                minUnsatCount=currUnsatCount
            board[y,x]=int(not board[y,x])
        return bestAtomIndex, minUnsatCount

    def find_unsatisfied_predicate(self, board, rowHints, colHints):
        predicates=[]
        for axis, hints in enumerate([colHints, rowHints]):
            for index, hint in enumerate(hints):
                line=board[:,index] if axis==0 else board[index,:]
                if self.check_line(line, hint)==False:
                    predicates.append([(i,index) if axis==0 else (index,i) for i in range(board.shape[0])])
        if predicates==[]:
            return None
        else:
            return random.choice(predicates)

    def count_unsatisfied_predicate(self, board, rowHints, colHints):
        count=0
        for axis, hints in enumerate([colHints, rowHints]):
            for index, hint in enumerate(hints):
                line=board[:,index] if axis==0 else board[index,:]
                if self.check_line(line, hint)==False:
                    count+=1
        return count

    def check_line(self, line, hint):
        segments=self.get_segments(line)
        if segments==[]:
            segments=[0]
        if len(segments)!=len(hint):
            return False
        for i in range(len(segments)):
            if int(segments[i])!=hint[i]:
                return False
        return True

    def get_segments(self, line):
        # [a,b,0,c,d] => [2,2]
        return [len(part) for part in (''.join([str(int(x)) for x in line]).split('0')) if len(part)>0]

    def assign_atoms(self, positives, negatives, neutrals):
        if positives==negatives==neutrals==set():
            return
        certain_atoms = self.certainAtoms
        for atom in positives:
            y,x=atom
            self.board[y,x]=1
        for atom in negatives:
            y,x=atom
            self.board[y,x]=0
        certain_atoms = certain_atoms | positives | negatives - neutrals   
        self.certainAtoms=certain_atoms

    def draw(self):
        if self.app.master==None:
            exit(0)
        self.app.iteration=self.iteration
        self.app.update_label("Iteration: "+str(self.iteration))
        self.app.update()
        positives, negatives, neutrals=self.app.get_decisions()
        self.assign_atoms(positives, negatives, neutrals)
        

if __name__ == "__main__":
    main()