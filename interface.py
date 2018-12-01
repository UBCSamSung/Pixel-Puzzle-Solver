from tkinter import Tk, Grid, Frame, Button
from tkinter.constants import *

def main():
    #Create & Configure root 
    root = Tk()
    Grid.rowconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 0, weight=1)

    #Create & Configure frame 
    frame=Frame(root)
    frame.grid(row=0, column=0, sticky=N+S+E+W)

    #Create a 5x10 (rows x columns) grid of buttons inside the frame
    n=10
    for row_index in range(n+1):
        Grid.rowconfigure(frame, row_index, weight=1)
        for col_index in range(n+1):
            Grid.columnconfigure(frame, col_index, weight=1)
            if row_index==0 and col_index==0:
                continue
            btn = Button(frame) #create a button inside frame
            btn.grid(row=row_index, column=col_index, sticky=N+S+E+W)  

    root.mainloop()

if __name__ == "__main__":
    main()