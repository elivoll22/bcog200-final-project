import tkinter as tk
import random

card_values = [
    "A",
    "A",
    "B",
    "B",
    "C",
    "C",
    "D",
    "D",
    "E",
    "E",
    "F",
    "F",
    "G",
    "G",
    "H",
    "H",
]

random.shuffle(card_values)

class ConFig:
    window_height = 600
    window_width = 800

    instructions_bg_color = "white"
    instructions_font_color = "black"
    instructions_font_size = 18
    instructions_font = "helvetica"
    instruction_delay = 1000 

class CardGame:
    def __init__(self, card_values):
        self.deck = card_values
        random.shuffle(self.deck)

    def select_card(self):
        if not self.deck:



        # root = tk.Tk()
        # root.title("Memory Game")
        # root.mainloop()

        # grid size
        # create list of card pairs
        # shuffle and arrange cards in a grid
        # track which cards are face up and which are hidden
        # implement a function to handle clicks:
        #     flip the card and reveal its Value
        #     if two cards are flipped, check if they match
        #     if not, flip them back after a short delay
        # keep track of matched pairs
        # use buttons to represent face-down card_valueswhen clicked, change the buttons texty to reveal the card_game