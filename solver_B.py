# Python 3.7.1

# WalkSat Approach

import numpy as np
import random

def main():
    t=int(input())
    for _ in range(t):
        n=int(input())
        rowHints=[[int(x) for x in input().strip().split()] for _ in range(n)]
        colHints=[[int(x) for x in input().strip().split()] for _ in range(n)]
        solve(n, rowHints, colHints)

def solve(n, rowHints, colHints):
    # TODO
    # Board is n by n where each entry is Board[row index, col index]
    # Each hint is a predicate
    board=np.random.randint(0,2,[n,n])
    positiveAtoms=positive_deduce(n, rowHints, colHints)
    negativeAtoms=negative_deduce(n, rowHints, colHints)
    for atom in positiveAtoms:
        y,x=atom
        board[y,x]=1
    for atom in negativeAtoms:
        y,x=atom
        board[y,x]=0
    certainAtoms=set(sorted(list(set(positiveAtoms or []).union(set(negativeAtoms or [])))))
    print("rowHints:")
    print(rowHints)
    print("colHints:")
    print(colHints)
    print("certainAtoms:")
    print(certainAtoms)
    iteration=0
    minUnsatCount=2*n
    # bestBoard=board[:]
    # bestScore=2*n
    while True:
        # find a unsatisfied predicate
        iteration+=1
        verbose=iteration%100==1 or True
        if iteration%10000==1:
            print("restart")
            for i in range(n):
                for j in range(n):
                    if (j,i) not in certainAtoms:
                        board[j,i]=random.randint(0,1)
        if verbose:
            print("iteration:", iteration)
            print("min unsatisfied predicates:", minUnsatCount)
            print("current board:")
            print(board)
        pickedAtoms=find_unsatisfied_predicate(board, rowHints, colHints)
        if pickedAtoms==None:
            print("solved board:")
            print(board)
            return
        pickableAtoms=list(set(pickedAtoms or [])-certainAtoms)
        if (pickableAtoms==[]):
            print("!!!", pickedAtoms)
            return
        beGreedy=random.choice([1]*9+[0]*1)
        pickedAtom=None
        if beGreedy:
            best_atom_flip, minUnsatCount=find_best_atom_flip(board, rowHints, colHints, pickableAtoms)
            # if minUnsatCount<bestScore:
            #     bestScore=minUnsatCount
            #     bestBoard=board[:]
            if best_atom_flip!=-1:
                pickedAtom=pickableAtoms[best_atom_flip]
        if pickedAtom==None:
            pickedAtom=random.choice(pickableAtoms)
        y,x=pickedAtom
        board[y,x]=int(not board[y,x])
        # break

def positive_deduce(n, rowHints, colHints):
    atoms=set()
    for axis, hints in enumerate([colHints, rowHints]):
        for index, hint in enumerate(hints):
            m=max(hint)
            if m>n//2:
                for i in range(n):
                    if i+m>n-1 and i-m<0:
                        atoms.add((i,index) if axis==0 else (index,i))
    return atoms
def negative_deduce(n, rowHints, colHints):
    atoms=set()
    for axis, hints in enumerate([colHints, rowHints]):
        for index, hint in enumerate(hints):
            m=max(hint)
            if m==0:
                for i in range(n):
                    atoms.add((i,index) if axis==0 else (index,i))
    return atoms

def find_best_atom_flip(board, rowHints, colHints, pickedAtoms):
    bestAtomIndex=-1
    minUnsatCount=count_unsatisfied_predicate(board, rowHints, colHints)
    for index, atom in enumerate(pickedAtoms):
        y,x=atom
        board[y,x]=int(not board[y,x])
        currUnsatCount=count_unsatisfied_predicate(board,rowHints,colHints)
        if currUnsatCount<minUnsatCount:
            bestAtomIndex=index
            minUnsatCount=currUnsatCount
        board[y,x]=int(not board[y,x])
    return bestAtomIndex, minUnsatCount

def find_unsatisfied_predicate(board, rowHints, colHints):
    predicates=[]
    for axis, hints in enumerate([colHints, rowHints]):
        for index, hint in enumerate(hints):
            line=board[:,index] if axis==0 else board[index,:]
            if check_line(line, hint)==False:
                predicates.append([(i,index) if axis==0 else (index,i) for i in range(board.shape[0])])
    if predicates==[]:
        return None
    else:
        return random.choice(predicates)

def count_unsatisfied_predicate(board, rowHints, colHints):
    count=0
    for axis, hints in enumerate([colHints, rowHints]):
        for index, hint in enumerate(hints):
            line=board[:,index] if axis==0 else board[index,:]
            if check_line(line, hint)==False:
                count+=1
    return count

def check_line(line, hint):
    segments=get_segments(line)
    if segments==[]:
        segments=[0]
    if len(segments)!=len(hint):
        return False
    for i in range(len(segments)):
        if int(segments[i])!=hint[i]:
            return False
    return True

def get_segments(line):
    # [a,b,0,c,d] => [2,2]
    return [len(part) for part in (''.join([str(int(x)) for x in line]).split('0')) if len(part)>0]

if __name__ == "__main__":
    main()