import csv
from mtranslate import translate
import time
from pathlib import Path

INPUT_FILE = Path("data/oxford-5000.csv")
OUTPUT_FILE = Path("data/words_unique.csv")


def translate_unique_words(input_file, output_file):
    seen = set()
    rows = []

    # Читаем и удаляем дубли по слову
    with open(input_file, newline='', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        for row in reader:
            word = row["word"].strip()
            if word not in seen:
                seen.add(word)
                rows.append(row)

    print(f"Убрано повторов. Осталось {len(rows)} слов.")

    # Переводим и сохраняем
    fieldnames = ["word", "class", "level", "translation"]

    with open(output_file, 'w', newline='', encoding='utf-8') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            word = row["word"].strip()
            word_class = row["class"].strip()
            level = row["level"].strip()

            try:
                translation = translate(word, "ru", "en")
                print(f"{word} → {translation}")
            except Exception as e:
                print(f"Ошибка перевода '{word}': {e}")
                translation = ""

            writer.writerow({
                "word": word,
                "class": word_class,
                "level": level,
                "translation": translation
            })

            time.sleep(0.5)  # защита от блокировки

    print(f"Перевод завершён. Файл сохранён: {output_file}")

if __name__ == "__main__":
    translate_unique_words(INPUT_FILE, OUTPUT_FILE)