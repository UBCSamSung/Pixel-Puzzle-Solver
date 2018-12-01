# Brute Force Approach
# Able to solve 3x3 game board (512 states)
# Cannot solve 10x10 game board 1e30 state

import numpy as np
def main():
    t=int(input())
    for _ in range(t):
        n=int(input())
        rowHint=[[int(x) for x in input().strip().split()] for _ in range(n)]
        colHint=[[int(x) for x in input().strip().split()] for _ in range(n)]
        solve(n, rowHint, colHint)

def solve(n, rowHint, colHint):
    def helper_solve(curr_y, curr_x):
        print("y"*curr_y+"x"*curr_x)
        if curr_y==n:
            print("solved board:")
            print(board)
            return True
        for assignment in [1,0]:
            # print("y: {}, x: {}, val: {}".format(curr_y, curr_x, assignment))
            board[curr_y, curr_x]=assignment
            # print("current board:")
            # print(board)
            if not check_line(board[curr_y, :], rowHint[curr_y], strict=((curr_x+1)==n)):
                # print("inconsistent row", rowHint[curr_y])
                continue
            if not check_line(board[:, curr_x], colHint[curr_x], strict=((curr_y+1)==n)):
                # print("inconsistent col", rowHint[curr_x])
                continue
            if curr_x+1<n:
                next_x=curr_x+1
                next_y=curr_y
            else:
                next_y=curr_y+1
                next_x=0
            if helper_solve(next_y, next_x)==True:
                return True
        return False
    board=np.zeros([n,n])
    print("rowHint:")
    print(rowHint)
    print("colHint:")
    print(colHint)
    # print("board:")
    # print(board)
    helper_solve(0, 0)


def check_line(line, hint, strict=False):
    segments=get_segments(line)
    # print("segments:", segments)
    # print("strict:", strict)
    if strict:
        if len(segments)!=len(hint):
            return False
        for i in range(len(segments)):
            if int(segments[i])!=hint[i]:
                return False
    else:
        if len(segments)>len(hint):
            return False
        if segments==[]:
            return True
        if max(segments)>max(hint):
            return False
    return True

def get_segments(line):
    # [a,b,0,c,d] => [2,2]
    return [len(part) for part in (''.join([str(int(x)) for x in line]).split('0')) if len(part)>0]
    
if __name__ == "__main__":
    # print(get_segments([1,2,3,0,0,2,3,0,1]))
    main()