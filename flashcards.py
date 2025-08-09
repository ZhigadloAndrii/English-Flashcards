import csv
import random


class Flashcards:
    def __init__(self, csv_file):
        self.words = self.load_words(csv_file)
        self.index = 0
        random.shuffle(self.words)  # перемешаем порядок

    def load_words(self, csv_file):
        words = []
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                words.append({
                    "word": row["word"].strip(),
                    "translation": row["translation"].strip()
                })
        return words

    def get_current(self):
        """Возвращает текущее слово и перевод"""
        if self.index < len(self.words):
            return self.words[self.index]
        return None

    def next_card(self):
        """Переход к следующей карточке"""
        self.index += 1
        if self.index >= len(self.words):
            return None
        return self.get_current()

    def total(self):
        return len(self.words)

    def remaining(self):
        return self.total() - self.index
