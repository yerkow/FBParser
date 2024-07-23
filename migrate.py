import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",
    user="fbparser",
    password="fbparser",
    database="fbparser"
)

cursor = db_connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        post_url VARCHAR(255) NOT NULL,
        creation_time DATETIME,
        content TEXT,
        external_link VARCHAR(255),
        post_id VARCHAR(50),
        page_id VARCHAR(50)
    ) DEFAULT CHARSET=utf8mb4
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS info (
        id INT AUTO_INCREMENT PRIMARY KEY,
        tag VARCHAR(255)
    ) DEFAULT CHARSET=utf8mb4
""")


cursor.close()
db_connection.close()