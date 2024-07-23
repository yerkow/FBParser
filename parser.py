import datetime
import logging
import random
import re
import time
from random import randrange
from urllib.parse import unquote

import mysql.connector
from bs4 import BeautifulSoup
from gologin import GoLogin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeDriverService
from webdriver_manager.chrome import ChromeDriverManager


def parse_with_nologin(index, tag, profile, dbhost, dbuser, dbpassword, db, gl_token, select_browser, extra_params):
    global gl
    global chrome_options

    db_connection = None
    cursor = None
    driver = None
    driver_version = '125.0.6422.41'

    try:
        # Подключение к базе данных MySQL
        db_connection = mysql.connector.connect(
            host=dbhost,
            user=dbuser,
            password=dbpassword,
            database=db
        )

        cursor = db_connection.cursor()

        if select_browser == 1:
            chrome_options = Options()
            chrome_options.add_argument("--disable-notifications")
            # chrome_options.add_argument("--disable-infobars")
            # # chrome_options.add_argument("start-maximized")
            # chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-images")
            # chrome_options.add_argument("--disable-css")
            # chrome_options.add_argument("headless")

        elif select_browser == 2:
            gl = GoLogin({
                "token": gl_token,
                "profile_id": profile,
                'extra_params': extra_params,
                # 'extra_params': ['--headless=new','--disable-notifications', '--disable-images'],
                'port': random.randint(3500, 9999),
            })

            # Настройка WebDriver (в данном случае Chrome)
            chrome_options = Options()
            debugger_address = gl.start()
            chrome_options.add_experimental_option("debuggerAddress", debugger_address)

        elif select_browser == 3:
            chrome_options = Options()
            chrome_options.add_argument("--disable-notifications")
            # chrome_options.add_argument("--disable-infobars")
            # # chrome_options.add_argument("start-maximized")
            # chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-images")
            # chrome_options.add_argument("--disable-css")
            chrome_options.add_argument("headless")

        driver = webdriver.Chrome(service=ChromeDriverService(ChromeDriverManager(driver_version = driver_version).install()), options=chrome_options)
        # Открытие страницы
        # driver.get("http://facebook.com")
        # # driver.maximize_window()
        # wait = WebDriverWait(driver, 30)
        # time.sleep(randrange(1, 15))
        #
        # # Вход в аккаунт
        # print(f"P - {index} | {tag}: Выполняем вход в аккаунт...")
        # email_field = wait.until(ec.visibility_of_element_located((By.NAME, 'email')))
        # email_field.send_keys(facebook_email)
        # pass_field = wait.until(ec.visibility_of_element_located((By.NAME, 'pass')))
        # pass_field.send_keys(facebook_password)
        # pass_field.send_keys(Keys.RETURN)
        #
        # time.sleep(10)

        # Поиск постов по тегу
        driver.get(
            f'https://www.facebook.com/search/posts?q={tag}&filters=eyJyZWNlbnRfcG9zdHM6MCI6IntcIm5hbWVcIjpcInJlY2VudF9wb3N0c1wiLFwiYXJnc1wiOlwiXCJ9In0%3D')
        time.sleep(randrange(1, 15))
        print(f"P - {index} | {tag}: Поиск постов по тегу.. #{tag}")
        ### SCROLLING

        # SCROLL_PAUSE_TIME = 0.5
        # Get scroll height
        # last_height = driver.execute_script("return document.body.scrollHeight")
        # while True:
        #     # Scroll down to bottom
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     # Wait to load page
        #     time.sleep(SCROLL_PAUSE_TIME)
        #     # Calculate new scroll height and compare with last scroll height
        #     new_height = driver.execute_script("return document.body.scrollHeight")
        #     if new_height == last_height:
        #         break
        #     last_height = new_height

        #
        # Пауза загрузки страницы
        print(f"P - {index} | {tag}: Скроллим ленту..")
        SCROLL_PAUSE_TIME = randrange(5, 10)
        scroll_stop_limit = 50
        scroll_stop = 1
        # while True:
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(SCROLL_PAUSE_TIME)
        #     if scroll_stop == 50:
        #         break
        #     scroll_stop += 1

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"P - {index} | {tag}: Скроллим ленту: {scroll_stop + 1} из {scroll_stop_limit}")
            time.sleep(SCROLL_PAUSE_TIME)
            if scroll_stop == scroll_stop_limit:
                break
            scroll_stop += 1

        # Получение и парсинг HTML-кода страницы
        print(f"P - {index} | {tag}: Получаем код страницы..")
        page_source = driver.page_source
        time.sleep(1)
        soup = BeautifulSoup(page_source, "html.parser")

        # Функция для урезания URL до базовой части
        def trim_url_simple(url):
            index = url.find('__cft__')
            if index != -1:
                return url[:index]
            return url

        def trim_decoded_url(url):
            index = url.find('fbclid')
            if index != -1:
                return url[:index]
            return url

        # Функция для фильтрации ссылок на /videos/
        # def filter_video_links(post_links):
        #     filtered_links = []
        #     for post_link in post_links:
        #         post_href = post_link.get("href")
        #         if '/videos/' not in post_href:
        #             post_href_cutted = trim_url_simple(post_href)
        #             filtered_links.append(post_href_cutted)
        #
        #         if '/photo/' not in post_href:
        #             post_href_cutted = trim_url_simple(post_href)
        #             filtered_links.append(post_href_cutted)
        #
        #         if '/watch/' not in post_href:
        #             post_href_cutted = trim_url_simple(post_href)
        #             filtered_links.append(post_href_cutted)
        #
        #     return filtered_links

        def filter_video_links(post_links):
            filtered_links = []
            filters = ['/videos/', '/photo/', '/watch/']

            for post_link in post_links:
                post_href = post_link.get("href")

                if not any(f in post_href for f in filters):
                    post_href_cutted = trim_url_simple(post_href)
                    filtered_links.append(post_href_cutted)

            return filtered_links

        # поиск ссылок по классу на странице с поиском тега, брать классы с <a> с тегом role = link и aria-label: true
        post_links = soup.findAll('a', {
            'class': 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 xo1l8bm',
            "aria-label": True})
        filtered_links = filter_video_links(post_links)

        # # Запись отфильтрованных ссылок в файл
        # with open('post_links.txt', 'w', encoding='utf-8') as file:
        #     for post_href_cutted in filtered_links:
        #         file.write(post_href_cutted + '\n')

        # Функция для получения HTML-кода поста
        def get_html_content(url):
            driver.get(url)
            time.sleep(1)
            return driver.page_source

        # Функция для парсинга внешней ссылки из HTML-кода поста
        def parse_external_link(html_content):
            news_soup = BeautifulSoup(html_content, 'html.parser')
            # берутся классы со страницы где есть ссылка на внешний источник, у тега а с атрибутом role=link
            external_link = news_soup.find('a', {
                'class': 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lliihq x1lku1pv'})
            if external_link:
                return external_link.get("href")
            else:
                return None

        # Функция для парсинга времени создания поста из HTML-кода
        def parse_post_time(html_content):
            news_soup = BeautifulSoup(html_content, 'html.parser')
            script_tags = news_soup.find_all('script')
            creation_time = None
            for script in script_tags:
                script_text = script.text.strip()
                match = re.search(r'"creation_time":(\d+)', script_text)
                if match:
                    creation_time = int(match.group(1))
                    break
            return creation_time

        # Функция для парсинга содержимого поста из HTML-кода
        # def parse_post_content(html_content):
        #     news_soup = BeautifulSoup(html_content, 'html.parser')
        #     # берется из основного текста, 1 общий класс между всеми текстами
        #     posts_content = news_soup.findAll('div', class_='xtlvy1s')
        #     if not posts_content:
        #         # берутся из текста с хэштегами
        #         posts_content = news_soup.findAll('div', class_='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a')
        #     news_texts = [div.get_text(strip=True) for div in posts_content]
        #     news_content = "\n".join(news_texts)
        #     return news_content

        def parse_post_content(html_content):
            news_soup = BeautifulSoup(html_content, 'html.parser')

            # ищем в первом объекте
            posts_content1 = news_soup.findAll('div', class_='xtlvy1s') or []

            # ищем во втором объекте
            posts_content2 = news_soup.findAll('div', class_='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a')

            posts_content3 = news_soup.findAll('div', class_='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs') or []

            posts_content4 = news_soup.findAll('span',
                                               class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x1lkfr7t x1lbecb7 x1s688f xzsf02u x1yc453h') or []

            posts_content5 = news_soup.findAll('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6 x1120s5i') or []

            posts_content6 = news_soup.findAll('span',
                                               class_='html-span xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs x3nfvp2 x1j61x8r x1fcty0u xdj266r xat24cr xgzva0m xhhsvwb xxymvpz xlup9mm x1kky2od')

            # объединяем результаты
            posts_content = posts_content1 + posts_content2 + posts_content3 + posts_content4 + posts_content5 + posts_content6

            # news_texts = [div.get_text(strip=True) for div in posts_content]
            # news_content = "\n".join(news_texts)

            news_texts = [element.get_text(strip=True) for element in posts_content if element]

            # Объединяем все тексты в одну строку
            news_content = "\n".join(news_texts)

            # #исключение постов только с картинкой
            # valid_posts_content = [div for div in posts_content if div.get_text(strip=True)]
            #
            # news_texts = [div.get_text(strip=True) for div in valid_posts_content]
            # news_content = "\n".join(news_texts)

            return news_content

        # Функция для парсинга метаданных из HTML-кода
        def parse_metadata(html_content):
            news_soup = BeautifulSoup(html_content, 'html.parser')
            script_tags = news_soup.find_all('script')
            post_id = None
            page_id = None
            page_id_count = 0
            for script in script_tags:
                script_text = script.text.strip()
                match_post_id = re.search(r'"post_id":"(\d+)"', script_text)
                if match_post_id:
                    post_id = match_post_id.group(1)

                match_page_id = re.finditer(r'\"page_id\":\"(\d+)\"', script_text)
                for match in match_page_id:
                    page_id_count += 1
                    if page_id_count == 3:
                        page_id = match.group(1)
                        break

                # match_page_id = re.search(r'"pageID":"(\d+)"', script_text)
                # if match_page_id:
                #     page_id = match_page_id.group(1)

                if not match_page_id:
                    match_group_id = re.search(r'"groupID":"(\d+)"', script_text)
                    if match_group_id:
                        page_id = match_group_id.group(1)

                if page_id is None:
                    match_owning_id = re.search(r'"owning_profile_id":"(\d+)"', script_text)
                    if match_owning_id:
                        page_id = match_owning_id.group(1)

                if post_id and page_id:
                    break
            return post_id, page_id

        # # Перебор ссылок из файла и сохранение данных в базу
        # with open('post_links.txt', 'r', encoding='utf-8') as file:
        #     post_urls = file.readlines()

        print(f"P - {index} | {tag}: ВСЕГО НАЙДЕНО ССЫЛОК: {len(filtered_links)}")

        link_count = 1

        for post_href_cutted in filtered_links:
            if post_href_cutted:  # Проверка, что ссылка не пустая
                # Проверка наличия ссылки в базе
                cursor.execute("SELECT COUNT(*) FROM posts WHERE post_url = %s", (post_href_cutted,))
                result = cursor.fetchone()
                if result[0] > 0:
                    print(
                        f"P - {index} | {tag}| {len(filtered_links)}: Ссылка {post_href_cutted} уже присутствует в базе, пропускаем...")
                    continue
                print(f"P - {index} | {tag}| {len(filtered_links)}: Парсинг контента с {post_href_cutted})")

                # Получение HTML-кода поста
                html_content = get_html_content(post_href_cutted)

                # Парсинг времени создания поста
                creation_time_unix = parse_post_time(html_content)
                # creation_time = datetime.datetime.fromtimestamp(creation_time_unix)

                # logging.basicConfig(level=logging.DEBUG)

                # Example of how creation_time_unix might be set
                # creation_time_unix = some_function_that_returns_timestamp()

                logging.debug(f"creation_time_unix: {creation_time_unix}")

                if creation_time_unix is not None:
                    creation_time = datetime.datetime.fromtimestamp(creation_time_unix)
                else:
                    creation_time = None
                    print(f"P - {index} | {tag}: {creation_time_unix}")
                    logging.error("creation_time_unix is None, cannot convert to datetime")

                # Парсинг содержимого поста
                content = parse_post_content(html_content)

                # Парсинг внешней ссылки
                external_link = parse_external_link(html_content)

                if external_link:
                    if '__cft__' in external_link:
                        parsed_url = trim_url_simple(external_link)
                    else:
                        parsed_url = external_link.split('u=')[1].split('&')[0]

                    decoded_url = unquote(parsed_url)
                    cutted_decoded_url = trim_decoded_url(decoded_url)
                    print(f"P - {index} | {tag} | {len(filtered_links)}: Ссылка на внешний источник присутствует. Ссылка: {decoded_url}")
                else:
                    parsed_url = None
                    decoded_url = None
                    cutted_decoded_url = None

                # Парсинг метаданных
                post_id, page_id = parse_metadata(html_content)

                # Вставка данных в базу данных
                query = """
                        INSERT INTO posts (post_url, creation_time, content, external_link, post_id, page_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                data = (post_href_cutted, creation_time, content, cutted_decoded_url, post_id, page_id)
                cursor.execute(query, data)
                db_connection.commit()

    except Exception as e:
        print(f"Error occurred: {e}")
        logging.error(f"Error occurred: {e}")
    finally:
        if select_browser == 2:
            gl.stop()
        if cursor:
            cursor.close()
        if db_connection:
            db_connection.close()
        if driver:
            driver.quit()
