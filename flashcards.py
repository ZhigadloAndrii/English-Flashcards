import csv
import random


class Flashcards:
    def __init__(self, csv_file):
        self.words = self.load_words(csv_file)
        for w in self.words:
            w["weight"] = 1.0

    def load_words(self, csv_file):
        words = []
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                words.append({
                    "word": row["word"].strip(),
                    "translation": row["translation"].strip(),
                    "level": row["level"].strip()
                })
        return words

    def choose_next(self):
        """Выбирает слово с учетом веса"""
        total_weight = sum(w["weight"] for w in self.words)
        r = random.uniform(0, total_weight)
        cumulative = 0
        for w in self.words:
            cumulative += w["weight"]
            if r <= cumulative:
                return w
        return self.words[-1]

    def mark_known(self, word):
        word["weight"] = max(0.1, word["weight"] * 0.5)

    def mark_unknown(self, word):
        word["weight"] = min(10, word["weight"] * 1.5)
