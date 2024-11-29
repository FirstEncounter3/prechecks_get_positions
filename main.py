import sqlite3
import csv
import json
import os


def get_path_and_id():
    while True:
        db_path = input('Путь до базы > ')
        if os.path.exists(db_path):
            break
        else:
            print("Неверный путь. Пожалуйста, попробуйте снова.")

    while True:
        try:
            record_id = int(input('ID записи > '))
            break
        except ValueError:
            print("Пожалуйста, введите корректный числовой ID.")

    return db_path, record_id


def get_positions(db_path, record_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT positions FROM DeferredChecks WHERE _id = ?", (record_id,))
        positions = cursor.fetchone()
    return json.loads(positions[0]) if positions else None


def prepare_positions(db_path, record_id):
    result_object = {}
    result_list_of_objects = []

    original_list = get_positions(db_path, record_id)

    for elem in original_list:
        result_object["Наименование"] = elem["name"]
        result_object["Цена"] = elem["price"]
        result_object["Количество"] = elem["quantity"]
        result_object["Код товара"] = elem["productCode"]
        result_object["Сумма"] = str(elem["price"] * elem["quantity"]).replace(".", ",")
        result_list_of_objects.append(result_object)
        result_object = {}

    return result_list_of_objects


def write_to_csv(db_path, record_id):
    object_to_write = prepare_positions(db_path, record_id)

    with open(str(record_id) + ".csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=object_to_write[0].keys())

        writer.writeheader()
        writer.writerows(object_to_write)



if __name__ == "__main__":
    db_path, record_id = get_path_and_id()
    write_to_csv(db_path, record_id)