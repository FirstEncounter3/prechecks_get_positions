import sqlite3
import csv
import json
import os

from db import get_path_db, get_id


def get_path_and_id():
    db_path = get_path_db()
    record_id = get_id()
    return db_path, record_id


def get_positions(db_path, record_id):
    list_record_ids = record_id.split(",")
    result_list = []
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        placeholders = ', '.join('?' for _ in list_record_ids)
        query = f"SELECT positions FROM DeferredChecks WHERE _id IN ({placeholders})"
        
        cursor.execute(query, list_record_ids)
        results = cursor.fetchall()
        
        for positions in results:
            if positions:
                result_list.extend(json.loads(positions[0]))

    return result_list


def create_object(db_path, record_id):
    original_list = get_positions(db_path, record_id)
    result_list_of_objects = []
    ids = record_id.split(",")

    for index, elem in enumerate(original_list):
        try:
            result_object = {}
            result_object["Наименование"] = elem["name"]
            result_object["Цена"] = elem["price"]
            result_object["Количество"] = elem["quantity"]
            result_object["Код товара"] = elem["productCode"]
            result_object["Штрихкод"] = f'{elem.get("barcode")}'
            result_object["Сумма"] = str(elem["price"] * elem["quantity"]).replace(".", ",")
            result_list_of_objects.append(result_object)

        except KeyError as e:
            print(f"Данные о позиции {elem} отсутствуют в базе данных. Ошибка: {e}")

    return result_list_of_objects


def write_to_csv(db_path, record_id):
    object_to_write = create_object(db_path, record_id)
    ids = record_id.split(",")
    print(object_to_write)

    if not object_to_write:
        print("Нет данных для записи в CSV.")
        return

    try:
        with open(f"{record_id}.csv", "w", newline="", encoding="utf-8") as file:
            fieldnames = list(object_to_write[0].keys())
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for elem in object_to_write:
                writer.writerow(elem)

    except PermissionError:
        print("Ошибка доступа к файлу. Проверьте, что файл не открыт в другом приложении.")
    except Exception as e:
        print(f"Произошла ошибка при записи в CSV: {e}")



if __name__ == "__main__":
    db_path, record_id = get_path_and_id()
    # print(create_object(db_path, record_id))
    write_to_csv(db_path, record_id)
