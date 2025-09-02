import sqlite3
from pathlib import Path
import csv

DB_FILE = Path("data/flashcards.db")


def init_db(csv_file):
    """Создаёт БД и заполняет словами из CSV, если БД пустая."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # Создаём таблицу, если нет
    cur.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            translation TEXT NOT NULL,
            level TEXT,
            weight REAL DEFAULT 1.0
        )
    """)

    # Проверяем, есть ли данные
    cur.execute("SELECT COUNT(*) FROM words")
    if cur.fetchone()[0] == 0:
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute("""
                    INSERT INTO words (word, translation, level, weight)
                    VALUES (?, ?, ?, 1.0)
                """, (row["word"].strip(), row["translation"].strip(), row["level"].strip()))
        print("База данных заполнена из CSV.")

    conn.commit()
    conn.close()


def get_all_words():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM words")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_weight(word_id, new_weight):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("UPDATE words SET weight = ? WHERE id = ?", (new_weight, word_id))
    conn.commit()
    conn.close()


def get_words_by_levels(levels):
    """Получить слова по списку уровней"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    query = "SELECT * FROM words WHERE level IN ({})".format(",".join("?" for _ in levels))
    cur.execute(query, levels)
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]
