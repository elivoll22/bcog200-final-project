import tkinter as tk
import os
import random
from PIL import Image, ImageTk

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
        tk.Frame.__init__(self, root, bg="purple")
        self.root = root
        self.grid(row=0, column=0, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        start_frame = tk.Frame(self, bg="purple")
        start_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = tk.Label(
            start_frame,
            text="Memory Game",
            font=("Helvetica", 32, "bold"),
            bg="purple",
            fg="white",
        )
        title_label.pack(pady=20)

        start_button = tk.Button(
            start_frame,
            text="Start Game",
            font=("Helvetica", 16),
            command=self.start_game,
            padx=10,
            pady=5,
        )
        start_button.pack()

    def start_game(self):
        self.destroy()
        self.game = CardGame(self.root)


class CardGame:
    def __init__(self, root):
        self.root = root
        self.game_frame = tk.Frame(root, background="#fae6f7")
        self.game_frame.grid(row=0, column=0, sticky="nsew")

        for r in range(8):
            self.game_frame.grid_rowconfigure(r, weight=0)
        for c in range(4):
            self.game_frame.grid_columnconfigure(c, weight=1)

        self.cards = []
        self.selected_cards = []
        self.matched_pairs = 0
        self.moves = 0
        self.card_data = []
        self.front_images = []
        self.back_img = None
        self.blocked = False

        self.moves_label = tk.Label(
            self.game_frame,
            text=f"Moves: {self.moves}",
            font=("Helvetica", 14),
            bg="#efcbf5",
        )
        self.moves_label.grid(row=0, column=0, columnspan=4, pady=20)

        self.restart_button = tk.Button(
            self.game_frame,
            text="Restart Game",
            font=("Helvetica", 14),
            command=self.restart_game,
            padx=10,
            pady=5,
        )
        self.restart_button.grid(row=8, column=0, columnspan=4, pady=20)

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
        if self.blocked:
            return

        card = self.card_data[idx]
        if card["flipped"] or card["matched"] or not card["image"]:
            return

        card["button"].config(image=card["image"])
        card["flipped"] = True
        self.selected_cards.append(idx)

        if len(self.selected_cards) == 2:
            self.blocked = True
            self.root.after(1000, self.check_match)

    def check_match(self):
        if len(self.selected_cards) != 2:
            return

        idx1, idx2 = self.selected_cards
        card1 = self.card_data[idx1]
        card2 = self.card_data[idx2]

        if card1["image_path"] == card2["image_path"]:
            card1["matched"] = True
            card2["matched"] = True
            card1["button"].config(state=tk.DISABLED)
            card2["button"].config(state=tk.DISABLED)
            self.matched_pairs += 1
        else:
            card1["button"].config(image=self.back_img)
            card2["button"].config(image=self.back_img)
            card1["flipped"] = False
            card2["flipped"] = False

        self.selected_cards.clear()
        self.moves += 1
        self.moves_label.config(text=f"Moves: {self.moves}")
        self.blocked = False

    def restart_game(self):
        # Destroy the current game frame
        self.game_frame.destroy()
        # Create a new instance of the CardGame
        self.__init__(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Memory Game")
    root.geometry("800x600")
    root.configure(bg="purple")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    StartPage(root)
    root.mainloop()
