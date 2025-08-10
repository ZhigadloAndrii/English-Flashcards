import tkinter as tk
from flashcards import Flashcards
from pathlib import Path

DATA_FILE = Path("data/words_unique.csv")


class FlashcardApp:
    def __init__(self, root, flashcards):
        self.root = root
        self.flashcards = flashcards
        self.current_card = None
        self.show_translation = False
        self.mode = "en_to_ru"

        root.title("English Flashcards")
        root.geometry("400x300")

        # Уровень слова
        self.level_label = tk.Label(root, text="", font=("Arial", 14), fg="blue")
        self.level_label.pack()

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

        # Кнопка смены режима
        self.btn_switch = tk.Button(root, text="Сменить режим", command=self.switch_mode)
        self.btn_switch.pack(pady=10)

        self.next_card()

    def switch_mode(self):
        if self.mode == "en_to_ru":
            self.mode = "ru_to_en"
        else:
            self.mode = "en_to_ru"
        self.next_card()

    def next_card(self):
        self.show_translation = False
        self.current_card = self.flashcards.choose_next()

        if self.mode == "en_to_ru":
            word = self.current_card["word"]
            translation = self.current_card["translation"]
        else:  # ru_to_en
            word = self.current_card["translation"]
            translation = self.current_card["word"]

        self.display_word = word
        self.display_translation = translation

        self.word_label.config(text=self.display_word)
        self.translation_label.config(text="")
        self.level_label.config(text=f"Level: {self.current_card.get('level', '')}")

    def toggle_translation(self):
        if self.current_card:
            if self.show_translation:
                self.translation_label.config(text="")
                self.show_translation = False
            else:
                self.translation_label.config(text=self.display_translation)
                self.show_translation = True

    def know_word(self):
        self.flashcards.mark_known(self.current_card)
        self.next_card()

    def unknown_word(self):
        self.flashcards.mark_unknown(self.current_card)
        self.next_card()


if __name__ == "__main__":
    if not DATA_FILE.exists():
        print(f"Файл {DATA_FILE} не найден.")
    else:
        flashcards = Flashcards(DATA_FILE)
        root = tk.Tk()
        app = FlashcardApp(root, flashcards)
        root.mainloop()
