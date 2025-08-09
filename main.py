import tkinter as tk
from tkinter import messagebox
from flashcards import Flashcards
from pathlib import Path

DATA_FILE = Path("data/words_unique.csv")


class FlashcardApp:
    def __init__(self, root, flashcards):
        self.root = root
        self.flashcards = flashcards
        self.show_translation = False

        root.title("English Flashcards")
        root.geometry("400x300")

        # Слово
        self.word_label = tk.Label(root, text="", font=("Arial", 24))
        self.word_label.pack(pady=20)

        # Перевод
        self.translation_label = tk.Label(root, text="", font=("Arial", 18), fg="gray")
        self.translation_label.pack(pady=10)

        # Кнопки
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=20)

        self.btn_show = tk.Button(self.btn_frame, text="Показать перевод", command=self.toggle_translation)
        self.btn_show.grid(row=0, column=0, padx=5)

        self.btn_known = tk.Button(self.btn_frame, text="Знаю", command=self.know_word)
        self.btn_known.grid(row=0, column=1, padx=5)

        self.btn_unknown = tk.Button(self.btn_frame, text="Не знаю", command=self.next_card)
        self.btn_unknown.grid(row=0, column=2, padx=5)

        self.update_card()

    def update_card(self):
        card = self.flashcards.get_current()
        if card is None:
            messagebox.showinfo("Готово!", "Вы прошли все карточки.")
            self.root.quit()
            return
        self.show_translation = False
        self.word_label.config(text=card["word"])
        self.translation_label.config(text="")

    def toggle_translation(self):
        card = self.flashcards.get_current()
        if card:
            if self.show_translation:
                self.translation_label.config(text="")
                self.show_translation = False
            else:
                self.translation_label.config(text=card["translation"])
                self.show_translation = True

    def know_word(self):
        self.next_card()

    def next_card(self):
        self.flashcards.next_card()
        self.update_card()


if __name__ == "__main__":
    if not DATA_FILE.exists():
        print(f"Файл {DATA_FILE} не найден.")
    else:
        flashcards = Flashcards(DATA_FILE)
        root = tk.Tk()
        app = FlashcardApp(root, flashcards)
        root.mainloop()
