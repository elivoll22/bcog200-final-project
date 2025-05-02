import tkinter as tk
import os
import random

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
back_image = ["images/back_image.png"]


card_images *= 2
random.shuffle(card_images)


class StartPage(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Game")
        self.root.geometry("800x600")
        self.root.configure(bg="purple")
        self.background_label = tk.Label(
            self.root,
            text="Memory Game",
            font=("Helvetica", 32, "bold"),
            bg="purple",
            fg="white",
        )
        self.background_label.pack(expand=True)
        self.start_button = tk.Button(
            self.root,
            text="Start Game",
            font=("Helvetica", 16),
            command=self.start_game,
        )
        self.start_button.pack(pady=20)

    def start_game(self):
        self.background_label.destroy()
        self.start_button.destroy()
        game = CardGame(self.root)
        game.root.mainloop()


class CardGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Flip Game")

        self.game_frame = tk.Frame(root, background="#fae6f7")
        self.game_frame.pack(fill="both", expand=True)

        self.card_images = [tk.PhotoImage(file=image) for image in card_images]
        self.back_image = tk.PhotoImage(file=back_image)

        self.cards = []
        self.selected_cards = []
        self.matched_pairs = 0
        self.moves = 0

        self.moves_label = tk.Label(
            self.game_frame,
            text=f"Moves: {self.moves}",
            font=("Helvetica", 14),
            bg="#efcbf5",
        )
        self.moves_label.pack(pady=10)

        self.win_label = tk.Label(
            self.game_frame, text="You won!", font=("Helvetica", 32), bg="#fae6f7"
        )

        self.restart_button = tk.Button(
            self.game_frame,
            text="Restart",
            font=("Heletica", 14),
            bg="lightgrey",
            command=self.restart_game,
        )
        self.restart_button.pack(pady=10)

        self.click_card = tk.Button

        self.setup_game_board()

    def setup_game_board(self):
        for i in range(4):
            for j in range(4):
                card = tk.Button(
                    self.game_frame,
                    image=self.back_image,
                    command=lambda row=i, col=j: self.flip_card(row, col),
                )
                card.grid(row=i + 1, column=j, padx=5, pady=5)
                self.cards.append(card)

    def flip_card(self, i, j):
        index = i * 4 + j
        if index not in self.selected_cards and len(self.selected_cards) < 2:
            card = self.cards[
                index
            ]  # gets the button that responds to the card being flipped
            card.config(image=self.card_images[index])
            self.selected_cards.append((index, card))

            if len(self.selected_cards) == 2:
                self.root.after(1000, self.check_match)
                self.moves += 1
                self.moves_label.config(text=f"Moves: {self.moves}")

    def check_match(self):
        if not self.selected_cards:
            return

        idx1, idx2 = (
            self.selected_cards[0][0],
            self.selected_cards[1][0],
        )  # extracting the cards selected
        card1, card2 = (
            self.selected_cards[0][1],
            self.selected_cards[1][1],
        )  # give actual card buttons

        if card_images[idx1] != card_images[idx2]:
            card1.config(image=back_image)
            card2.config(image=back_image)
        else:
            self.matched_pairs += 1
            card1.config(state=tk.DISABLED)
            card2.config(state=tk.DISABLED)

        self.selected_cards.clear()

        if self.matched_pairs == len(card_images) // 2:
            self.show_win_message()

    def show_win_message(self):
        self.win_label.pack(pady=10)

    def restart_game(self):
        for card in self.cards:
            card.config(image=back_image, state=tk.NORMAL)
        self.moves = 0
        self.matched_pairs = 0
        self.moves_label.config(text=f"Moves: {self.moves}")
        self.win_label.pack_forget()
        random.shuffle(card_images)
        self.card_images = [tk.PhotoImage(file=image) for image in card_images]


if __name__ == "__main__":
    root = tk.Tk()
    # start_page = StartPage(root=root)
    start_page = CardGame(root=root)
    start_page.root.mainloop()
