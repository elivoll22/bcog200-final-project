import tkinter as tk
import os
import random
from PIL import Image, ImageTk
from tkinter import PhotoImage


card_images = [
    "images/bob.png",
    "images/coochie.png",
    "images/fischoeder.png",
    "images/gene.png",
    "images/linda.png",
    "images/louise.png",
    "images/teddy.png",
    "images/tina.png",
]
back_image = "images/back_image.png"


class StartPage(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Game")
        self.root.geometry("800x600")
        self.root.configure(bg="purple")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        self.background_label = tk.Label(
            self.root,
            text="Memory Game",
            font=("Helvetica", 32, "bold"),
            bg="purple",
            fg="white",
        )

        self.background_label.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.start_button = tk.Button(
            self.root,
            text="Start Game",
            font=("Helvetica", 16),
            command=self.start_game,
            padx=10,
            pady=2,
        )

        self.start_button.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)

    def start_game(self):
        self.background_label.destroy()
        self.start_button.destroy()
        self.game = CardGame(self.root)


class CardGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Flip Game")
        self.game_frame = tk.Frame(root, background="#fae6f7")
        self.game_frame.grid(row=0, column=0, sticky="nsew")

        self.game_frame.grid_columnconfigure(0, weight=1)
        self.game_frame.grid_rowconfigure(0, weight=0)  # Moves label
        self.game_frame.grid_rowconfigure(1, weight=0)  # Cards row 1
        self.game_frame.grid_rowconfigure(2, weight=0)  # Cards row 2
        self.game_frame.grid_rowconfigure(3, weight=0)  # Cards row 3
        self.game_frame.grid_rowconfigure(4, weight=0)  # Cards row 4
        self.game_frame.grid_rowconfigure(5, weight=0)  # Win label
        self.game_frame.grid_rowconfigure(6, weight=0)  # Restart button
        self.game_frame.grid_rowconfigure(7, weight=1)

        self.cards = []
        self.selected_cards = []
        self.matched_pairs = 0
        self.moves = 0
        self.card_data = []
        self.front_images = []
        self.back_img = None

        self.moves_label = tk.Label(
            self.game_frame,
            text=f"Moves: {self.moves}",
            font=("Helvetica", 14),
            bg="#efcbf5",
        )

        self.moves_label.grid(row=0, column=0, columnspan=4, pady=20)

        self.win_label = tk.Label(
            self.game_frame, text="You won!", font=("Helvetica", 32), bg="#fae6f7"
        )

        self.restart_button = tk.Button(
            self.game_frame,
            text="Restart",
            font=("Helvetica", 14),
            bg="lightgrey",
            command=self.restart_game,
        )

        self.restart_button.grid(row=6, column=0, columnspan=4, pady=20)

        self.load_images()
        self.show_cards()

    def load_images(self):
        self.front_images = []
        for img_path in card_images:
            try:
                image = Image.open(img_path)
                image = image.resize((100, 100))
                photo = ImageTk.PhotoImage(image)
                self.front_images.append(photo)
            except FileNotFoundError:
                print(f"Error: Image not found at {img_path}")

        try:
            back_image_pil = Image.open(back_image)
            back_image_pil = back_image_pil.resize((100, 100))
            self.back_img = ImageTk.PhotoImage(back_image_pil)
        except FileNotFoundError:
            print(f"Error: Back image not found at {back_image}")

    def show_cards(self):
        selected_images = card_images * 2
        random.shuffle(selected_images)
        self.card_data = []

        for i in range(16):
            img_path = selected_images[i]
            try:
                image = Image.open(img_path)
                image = image.resize((100, 100))
                photo = ImageTk.PhotoImage(image)
            except FileNotFoundError:
                print(f"Error loading image: {img_path}")
                photo = None

            button = tk.Button(
                self.game_frame,
                image=self.back_img,
                command=lambda idx=i: self.flip_card(idx),
                width=100,
                height=100,
                padx=10,
                pady=10,
            )
            button.grid(row=i // 4 + 1, column=i % 4, padx=10, pady=10)
            self.card_data.append(
                {
                    "image_path": img_path,
                    "image": photo,
                    "button": button,
                    "flipped": False,
                    "matched": False,
                }
            )

    def flip_card(self, idx):
        card = self.card_data[idx]
        if card["flipped"] or card["matched"] or not card["image"]:
            return

        card["button"].config(image=card["image"])
        card["flipped"] = True
        self.selected_cards.append(idx)

        if len(self.selected_cards) == 2:
            self.root.after(1000, self.check_match)

    def check_match(self):
        if len(self.selected_cards) != 2:
            return

        idx1, idx2 = self.selected_cards
        card1_path = self.card_data[idx1]["image_path"]
        card2_path = self.card_data[idx2]["image_path"]

        if card1_path == card2_path:
            self.card_data[idx1]["matched"] = True
            self.card_data[idx2]["matched"] = True
            self.card_data[idx1]["button"].config(state=tk.DISABLED)
            self.card_data[idx2]["button"].config(state=tk.DISABLED)
            self.matched_pairs += 1
        else:
            self.card_data[idx1]["button"].config(image=self.back_img)
            self.card_data[idx2]["button"].config(image=self.back_img)
            self.card_data[idx1]["flipped"] = False
            self.card_data[idx2]["flipped"] = False

        self.selected_cards.clear()
        self.moves += 1
        self.moves_label.config(text=f"Moves: {self.moves}")

        if self.matched_pairs == len(card_images):
            self.win_label.grid(row=5, column=0, columnspan=4, pady=30)

    def restart_game(self):
        self.destroy()
        self.__init__(self.root)
        # self.moves = 0
        # self.matched_pairs = 0
        # self.moves_label.config(text=f"Moves: {self.moves}")
        # self.win_label.pack_forget()
        # self.load_images()

        # for widget in self.game_frame.winfo_children():
        #     if isinstance(widget, tk.Button):
        #         widget.destroy()

        # self.show_cards()


if __name__ == "__main__":
    root = tk.Tk()
    start_page = StartPage(root)
    # start_page.grid(row=0, column=0, sticky="nsew")  # Place StartPage in root
    # root.grid_columnconfigure(0, weight=1)
    # root.grid_rowconfigure(0, weight=1)
    root.mainloop()
