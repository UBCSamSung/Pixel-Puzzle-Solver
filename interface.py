import tkinter as tk
from tkinter.constants import *
import numpy as np
import random


class Application(tk.Frame):
    def __init__(self, master=None):
        # import images
        self.tile_plain=tk.PhotoImage(file="images/tile_plain.gif")
        self.tile_clicked=tk.PhotoImage(file="images/tile_clicked.gif")
        self.tile_wrong=tk.PhotoImage(file="images/tile_wrong.gif")
        self.tile_flag=tk.PhotoImage(file="images/tile_flag.gif")
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        self.label=tk.Label(self, text="Pixel Puzzle Solver")
        self.label.pack(side="top")
        self.board=self.create_board()
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")
    
    def create_board(self):
        self.buttons=[]
        board = tk.Frame(self)
        board.pack()
        n=10
        for i in range(0,n+1):
            for j in range(0,n+1):
                button_id=len(self.buttons)
                coordinate=(i,j)
                if coordinate==(0,0):
                    continue
                widget=tk.Button(board, image=self.tile_plain)
                widget.bind(sequence="<Button-1>", func=self.left_click(id))
                widget.bind(sequence="<Button-3>", func=self.right_click(id))
                widget.grid(row=coordinate[1],column=coordinate[0], sticky=N)
                button = {
                    "widget":widget,
                    "id":button_id,
                    "state":0,
                    "coordinate":coordinate
                }
                self.buttons.append(button)
        return board
        
    def left_click(self, button_index):
        # TODO
        pass
    
    def right_click(self, button_index):
        # TODO
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pixel Puzzle Solver")
    app = Application(master=root)
    app.mainloop()