import random
from database import get_all_words, update_weight, get_words_by_levels


class Flashcards:
    def __init__(self, levels=None):
        self.levels = levels
        if levels:
            self.words = get_words_by_levels(levels)
        else:
            self.words = get_all_words()

    def reload_words(self):
        """Перезагружает список слов из БД."""
        if hasattr(self, "levels") and self.levels:
            self.words = get_words_by_levels(self.levels)
        else:
            self.words = get_all_words()

    def choose_next(self):
        """Выбирает слово с учетом веса"""
        if not self.words:
            return None

        total_weight = sum(w["weight"] for w in self.words)
        r = random.uniform(0, total_weight)
        cumulative = 0
        for w in self.words:
            cumulative += w["weight"]
            if r <= cumulative:
                return w
        return self.words[-1]

    def mark_known(self, word):
        new_weight = max(0.1, word["weight"] * 0.5)
        update_weight(word["id"], new_weight)
        self.reload_words()

    def mark_unknown(self, word):
        new_weight = min(10, word["weight"] * 1.5)
        update_weight(word["id"], new_weight)
        self.reload_words()