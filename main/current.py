import sqlite3
import json
import pandas as pd
import re
from typing import Dict, List, Optional, Any

def create_tables(conn: sqlite3.Connection) -> None:
    """Создание таблиц если они не существуют"""
    cursor = conn.cursor()
    
    # Таблица категорий
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cooking_category (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL UNIQUE
    )
    ''')
    
    # Таблица типов (кухни)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cooking_type (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL UNIQUE
    )
    ''')
    
    # Таблица ингредиентов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cooking_ingredient (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL UNIQUE
    )
    ''')
    
    # Таблица блюд (добавлено поле type_id)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cooking_dish (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(200) NOT NULL,
        description TEXT NOT NULL,
        instructions TEXT NOT NULL,
        cooktime INTEGER NULL,
        category_id INTEGER NULL,
        type_id INTEGER NULL,
        starred BOOLEAN NOT NULL DEFAULT 0,
        FOREIGN KEY (category_id) REFERENCES cooking_category (id),
        FOREIGN KEY (type_id) REFERENCES cooking_type (id)
    )
    ''')
    
    # Таблица связи блюд и ингредиентов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cooking_dishingredient (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dish_id INTEGER NOT NULL,
        ingredient_id INTEGER NOT NULL,
        quantity VARCHAR(100) NOT NULL,
        FOREIGN KEY (dish_id) REFERENCES cooking_dish (id),
        FOREIGN KEY (ingredient_id) REFERENCES cooking_ingredient (id),
        UNIQUE(dish_id, ingredient_id)
    )
    ''')
    
    conn.commit()

def get_or_create_category(conn: sqlite3.Connection, category_name: str) -> Optional[int]:
    """Получить или создать категорию"""
    if not category_name:
        return None
        
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM cooking_category WHERE name = ?', (category_name,))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        cursor.execute('INSERT INTO cooking_category (name) VALUES (?)', (category_name,))
        conn.commit()
        return cursor.lastrowid

def get_or_create_type(conn: sqlite3.Connection, type_name: str) -> Optional[int]:
    """Получить или создать тип (кухню)"""
    if not type_name:
        return None
        
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM cooking_type WHERE name = ?', (type_name,))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        cursor.execute('INSERT INTO cooking_type (name) VALUES (?)', (type_name,))
        conn.commit()
        return cursor.lastrowid

def get_or_create_ingredient(conn: sqlite3.Connection, ingredient_name: str) -> int:
    """Получить или создать ингредиент"""
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM cooking_ingredient WHERE name = ?', (ingredient_name,))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        cursor.execute('INSERT INTO cooking_ingredient (name) VALUES (?)', (ingredient_name,))
        conn.commit()
        return cursor.lastrowid

def parse_cooktime(cooktime_str: str) -> Optional[int]:
    """Парсинг времени приготовления и конвертация в минуты"""
    if pd.isna(cooktime_str) or not str(cooktime_str).strip():
        return None
    
    cooktime_str = str(cooktime_str).strip().lower()
    
    try:
        # Если время уже в числовом формате (только цифры)
        if cooktime_str.isdigit():
            return int(cooktime_str)
        
        # Разные форматы времени
        time_patterns = [
            # Формат: "1 час 30 минут"
            (r'(\d+)\s*час\w*\s*(\d+)\s*минут\w*', lambda h, m: int(h) * 60 + int(m)),
            # Формат: "2 часа 15 мин"
            (r'(\d+)\s*час\w*\s*(\d+)\s*мин\w*', lambda h, m: int(h) * 60 + int(m)),
            # Формат: "1 ч 30 м"
            (r'(\d+)\s*ч\s*(\d+)\s*м', lambda h, m: int(h) * 60 + int(m)),
            # Формат: "1.5 часа"
            (r'(\d+\.?\d*)\s*час\w*', lambda h: int(float(h) * 60)),
            # Формат: "2,5 ч"
            (r'(\d+,\d+)\s*ч', lambda h: int(float(h.replace(',', '.')) * 60)),
            # Формат: "90 минут"
            (r'(\d+)\s*минут\w*', lambda m: int(m)),
            # Формат: "45 мин"
            (r'(\d+)\s*мин\w*', lambda m: int(m)),
            # Формат: "1 час" (только часы)
            (r'(\d+)\s*час\w*', lambda h: int(h) * 60),
            # Формат: "3 ч" (только часы)
            (r'(\d+)\s*ч', lambda h: int(h) * 60),
            # Просто число (последнее, так как может ложно срабатывать)
            (r'(\d+)', lambda m: int(m)),
        ]
        
        for pattern, converter in time_patterns:
            match = re.search(pattern, cooktime_str)
            if match:
                groups = match.groups()
                if len(groups) == 2:
                    return converter(*groups)
                else:
                    return converter(groups[0])
        
        # Если ничего не найдено, попробуем извлечь все цифры
        numbers = re.findall(r'\d+', cooktime_str)
        if numbers:
            # Если есть несколько чисел, предположим что это часы и минуты
            if len(numbers) >= 2:
                return int(numbers[0]) * 60 + int(numbers[1])
            else:
                return int(numbers[0])
                
    except (ValueError, TypeError, AttributeError) as e:
        print(f"Ошибка парсинга времени '{cooktime_str}': {e}")
    
    return None

def clean_json_string(json_str: str) -> str:
    """Очистка JSON строки от некорректных символов"""
    if pd.isna(json_str):
        return '[]'
    
    json_str = str(json_str).strip()
    if not json_str or json_str == 'nan':
        return '[]'
    
    # Заменяем одинарные кавычки на двойные
    json_str = json_str.replace("'", "\"")
    # Заменяем None на null
    json_str = json_str.replace('None', 'null')
    # Убираем лишние пробелы
    json_str = re.sub(r'\s+', ' ', json_str)
    
    return json_str

def process_ingredients(conn: sqlite3.Connection, ingredients_json: str, dish_id: int, 
                       ingredients_cache: Dict[str, int]) -> int:
    """Обработка ингредиентов для блюда"""
    success_count = 0
    cursor = conn.cursor()
    
    try:
        json_str_clean = clean_json_string(ingredients_json)
        ingredients_data = json.loads(json_str_clean)
        
        if not isinstance(ingredients_data, list):
            return 0
        
        for ingredient_data in ingredients_data:
            if not isinstance(ingredient_data, dict):
                continue
                
            ingredient_name = ingredient_data.get('name', '')
            quantity = ingredient_data.get('value', '')
            
            if pd.isna(ingredient_name) or not str(ingredient_name).strip():
                continue
            
            ingredient_name = str(ingredient_name).strip()
            quantity = str(quantity).strip() if not pd.isna(quantity) else ''
            
            # Получаем или создаем ингредиент
            if ingredient_name not in ingredients_cache:
                ingredient_id = get_or_create_ingredient(conn, ingredient_name)
                ingredients_cache[ingredient_name] = ingredient_id
            else:
                ingredient_id = ingredients_cache[ingredient_name]
            
            # Вставляем связь блюдо-ингредиент
            cursor.execute('''
            INSERT OR IGNORE INTO cooking_dishingredient 
            (dish_id, ingredient_id, quantity)
            VALUES (?, ?, ?)
            ''', (dish_id, ingredient_id, quantity))
            
            success_count += 1
            
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
    except Exception as e:
        print(f"Ошибка обработки ингредиентов: {e}")
    
    return success_count

def import_from_csv(csv_file_path: str, db_file_path: str = 'db.sqlite3') -> None:
    """Импорт данных из CSV в SQLite с использованием Pandas"""
    
    # Подключаемся к базе данных
    conn = sqlite3.connect(db_file_path)
    create_tables(conn)
    
    try:
        # Читаем CSV файл с помощью Pandas
        print("Чтение CSV файла...")
        df = pd.read_csv(csv_file_path, delimiter=';', encoding='utf-8')
        
        # Заменяем NaN на пустые строки
        df = df.fillna('')
        
        print(f"Прочитано {len(df)} записей")
        
        # Создаем кэши для избежания дублирования
        categories_cache: Dict[str, int] = {}
        types_cache: Dict[str, int] = {}
        ingredients_cache: Dict[str, int] = {}
        
        processed_count = 0
        error_count = 0
        total_ingredients = 0
        
        cursor = conn.cursor()
        
        for index, row in df.iterrows():
            try:
                # Обрабатываем категорию
                category_name = str(row.get('category', '')).strip()
                category_id = None
                if category_name and category_name != 'nan':
                    if category_name not in categories_cache:
                        category_id = get_or_create_category(conn, category_name)
                        categories_cache[category_name] = category_id
                    else:
                        category_id = categories_cache[category_name]
                
                # Обрабатываем тип (кухню) из поля cuisine
                cuisine_name = str(row.get('cuisine', '')).strip()
                type_id = None
                if cuisine_name and cuisine_name != 'nan':
                    if cuisine_name not in types_cache:
                        type_id = get_or_create_type(conn, cuisine_name)
                        types_cache[cuisine_name] = type_id
                    else:
                        type_id = types_cache[cuisine_name]
                
                # Объединяем description и note
                description = str(row.get('description', '')).strip()
                note = str(row.get('note', '')).strip()
                full_description = description
                if note and note != 'nan':
                    full_description += f"\n\nПримечание: {note}"
                
                # Обрабатываем время приготовления
                cooktime_str = str(row.get('cooktime', ''))
                cooktime = parse_cooktime(cooktime_str)
                
                # Вставляем блюдо (добавлено поле type_id)
                cursor.execute('''
                INSERT INTO cooking_dish 
                (title, description, instructions, cooktime, category_id, type_id, starred)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(row.get('title', '')).strip(),
                    full_description,
                    str(row.get('instruction', '')).strip(),
                    cooktime,
                    category_id,
                    type_id,
                    0  # starred = False
                ))
                dish_id = cursor.lastrowid
                
                # Обрабатываем ингредиенты
                ingredients_json = row.get('ingredients', '[]')
                ingredients_count = process_ingredients(conn, ingredients_json, dish_id, ingredients_cache)
                total_ingredients += ingredients_count
                
                processed_count += 1
                
                if processed_count % 100 == 0:
                    print(f"Обработано {processed_count} блюд, {total_ingredients} ингредиентов...")
                    
            except Exception as e:
                print(f"Ошибка обработки строки {index + 2}: {e}")
                error_count += 1
                continue
        
        conn.commit()
        print(f"\nИмпорт завершен!")
        print(f"Успешно обработано блюд: {processed_count}")
        print(f"Добавлено ингредиентов: {total_ingredients}")
        print(f"Ошибок: {error_count}")
        
        # Выводим статистику
        cursor.execute("SELECT COUNT(*) FROM cooking_dish")
        total_dishes = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM cooking_ingredient")
        total_ingredients = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM cooking_dishingredient")
        total_relations = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM cooking_type")
        total_types = cursor.fetchone()[0]
        
        print(f"\nВ базе теперь:")
        print(f"  - Блюд: {total_dishes}")
        print(f"  - Типов (кухонь): {total_types}")
        print(f"  - Ингредиентов: {total_ingredients}")
        print(f"  - Связей блюд-ингредиентов: {total_relations}")
            
    except FileNotFoundError:
        print(f"Файл {csv_file_path} не найден!")
    except Exception as e:
        print(f"Общая ошибка: {e}")
        conn.rollback()
    finally:
        conn.close()

def test_connection(db_file_path: str = 'db.sqlite3') -> bool:
    """Тестирование подключения к базе"""
    try:
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("Таблицы в базе данных:")
        for table in tables:
            print(f"  - {table[0]}")
        conn.close()
        return True
    except Exception as e:
        print(f"Ошибка подключения к базе: {e}")
        return False

if __name__ == "__main__":
    csv_file_path = 'main\\result.csv'  # Укажите путь к вашему CSV файлу
    db_file_path = "main\\db.sqlite3"  # Путь к вашей SQLite базе
    
    print("Тестирование подключения к базе...")
    if test_connection(db_file_path):
        print("Подключение успешно!")
        import_from_csv(csv_file_path, db_file_path)
    else:
        print("Не удалось подключиться к базе данных")