import multiprocessing
import time
import shutil
import os
import mysql.connector
import logging
from logging.handlers import RotatingFileHandler
from parser import parse_with_nologin
from datetime import datetime

# Настройка логирования
def setup_logging():
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_file = datetime.now().strftime('log_%Y-%m-%d.txt')

    file_handler = RotatingFileHandler(log_file, maxBytes=10**6, backupCount=5)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)

    logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

# Функция для получения тегов из базы данных
def get_tags_from_db(dbhost, dbuser, dbpassword, db):
    try:
        connection = mysql.connector.connect(
            host=dbhost,
            user=dbuser,
            password=dbpassword,
            database=db
        )
        cursor = connection.cursor()
        cursor.execute("SELECT tag FROM info")
        result = cursor.fetchall()
        return [row[0] for row in result]  # Извлекаем теги из результата
    except mysql.connector.Error as err:
        logging.error(f"Ошибка: {err}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Функция для удаления профиля GoLogin
def delete_gologin_profile(profile_path):
    if os.path.exists(profile_path):
        try:
            shutil.rmtree(profile_path)
            logging.info(f"Профиль GoLogin удален: {profile_path}")
        except Exception as e:
            logging.error(f"Ошибка при удалении профиля GoLogin: {e}")

# Функция для выполнения задачи с повторами в случае ошибки
def worker(index, tag_queue, profile, facebook_email, facebook_password, dbhost, dbuser, dbpassword, db, gl_token, select_browser, extra_params, retries=3, delay=5):
    profile_path = f'C:\\Users\\asdfg\\AppData\\Local\\Temp\\gologin_{profile}'  # Путь к папке профиля GoLogin
    while True:
        try:
            tag = tag_queue.get(timeout=5)  # Получаем тег из очереди
            attempt = 0
            while attempt < retries:
                try:
                    parse_with_nologin(index, tag, profile, facebook_email, facebook_password, dbhost, dbuser, dbpassword, db, gl_token, select_browser, extra_params)
                    logging.info(f"Рабочий {index} успешно обработал тег: {tag}")
                    break  # Успешное завершение обработки
                except Exception as e:
                    attempt += 1
                    logging.error(f"Рабочий {index} неудачно завершил попытку {attempt} для тега {tag}. Ошибка: {e}")
                    if attempt < retries:
                        logging.info(f"Повторная попытка для рабочего {index} через {delay} секунд...")
                        time.sleep(delay)
                    else:
                        logging.error(f"Рабочий {index} не справился после {retries} попыток для тега {tag}.")
                        delete_gologin_profile(profile_path)
                        tag_queue.put(tag)  # Возвращаем тег в очередь для повторной обработки
                        break
        except Exception as e:
            logging.error(f"Ошибка при получении тега из очереди: {e}")
            break

# Основная функция для запуска процессов
def main():
    # Настройка логирования
    setup_logging()

    # Параметры подключения к базе данных
    dbhost = 'localhost'
    dbuser = 'fbparser'
    dbpassword = 'fbparser'
    db = 'fbparser'

    # Параметры браузера
    select_browser = 2  # 1 = Google Chrome (не headless), 2 = GoLogin Antidetect, 3 = Google Chrome (headless)
    extra_params = [
        '--disable-notifications',
        '--disable-images',
        '--headless=new'
    ]
    gl_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NjllOWZmM2MzNjc2YjZkNWIzYmU5NTAiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NjllYTA4ODExNmUzNDMxNzcxMWE0ZGYifQ.gnu-Qmsxzo2ZKvbRi93AcyhRKInr4B7Jt9OS9EmwLRs'

    # Получение тегов из базы данных
    tags = get_tags_from_db(dbhost, dbuser, dbpassword, db)

    if not tags:
        logging.error("Теги не получены из базы данных.")
        return

    # Данные профилей, email и паролей
    profiles = [
        "669ea07d251669cb3a6e309e",
        "669ea07b1f41219bb9aaa139",
        "669e9ff4c3676b6d5b3be9a6",
    ]
    facebook_emails = [
        'thirtyfourwave@gmail.com',
        'thirtyfourwave@gmail.com',
        'thirtyfourwave@gmail.com',
    ]
    facebook_passwords = [
        'iMasTesting2024',
        'iMasTesting2024',
        'iMasTesting2024',
    ]

    # Создание менеджера и очереди тегов
    with multiprocessing.Manager() as manager:
        tag_queue = manager.Queue()
        for tag in tags:
            tag_queue.put(tag)

        # Количество потоков
        num_processes = len(profiles)
        processes = []
        for i in range(num_processes):
            profile = profiles[i % len(profiles)]
            facebook_email = facebook_emails[i % len(facebook_emails)]
            facebook_password = facebook_passwords[i % len(facebook_passwords)]
            process = multiprocessing.Process(
                target=worker,
                args=(i, tag_queue, profile, facebook_email, facebook_password, dbhost, dbuser, dbpassword, db, gl_token, select_browser, extra_params)
            )
            processes.append(process)
            process.start()
            logging.info(f"Процесс {i} запущен с PID: {process.pid}")

        for index, process in enumerate(processes):
            process.join()
            logging.info(f"Процесс {index} с PID: {process.pid} завершен")

if __name__ == "__main__":
    main()
