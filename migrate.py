import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",
    user="fbparser",
    password="fbparser",
    database="fbparser",
    charset = 'utf8mb4',
    collation = 'utf8mb4_unicode_ci'
)

cursor = db_connection.cursor()
cursor.execute("SET NAMES utf8mb4;")
cursor.execute("SET CHARACTER SET utf8mb4;")
cursor.execute("SET character_set_connection=utf8mb4;")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        post_url VARCHAR(255) NOT NULL,
        creation_time DATETIME,
        content TEXT,
        external_link VARCHAR(255),
        post_id VARCHAR(50),
        page_id VARCHAR(50)
    ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS info (
        id INT AUTO_INCREMENT PRIMARY KEY,
        tag VARCHAR(255)
    ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")


cursor.close()
db_connection.close()