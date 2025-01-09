import os
import gzip
import glob

def unzip_archive(zip_path):
    print('\nРазархивирование резервной копии...')
    with gzip.open(zip_path, 'rb') as f_in:
        with open("temp.db", 'wb') as f_out:
            f_out.write(f_in.read())
    os.remove(zip_path)
    os.rename("temp.db", "prechecks.db")
    print('Разархивирование завершено')


def get_path_db():
    try_counter = 0
    while True:
        try:
            print("Ищем файл БД...")
            current_dir = os.getcwd()
            db_path = glob.glob("*.db")[0]
            if db_path:
                print(f"База данных найдена: {db_path}")
            return db_path
        except IndexError:
            try:
                print("Файл БД не найден, пробуем найти архив с БД... ")
                zip_path = glob.glob("*.gz")[0]
                if zip_path:
                    print(f"Архив найден: {zip_path}")
                    unzip_archive(zip_path)
                    continue
            except IndexError:
                print("Архив БД не найден, пробуем сканировать текущий каталог повторно...")
                pass

            print("База данных отсутствует в текущем каталоге. Пожалуйста, поместите БД в текущий каталог, рядом со скриптом")
            print(f"Повторная попытка сканирования...{try_counter}/10")
            time.sleep(5)
            try_counter += 1
            if try_counter == 5:
                break

    return db_path


def get_id():
    while True:
        try:
            record_id = input('ID записи > ')
            break
        except ValueError:
            print("Пожалуйста, введите корректный числовой ID.")

    return record_id
    