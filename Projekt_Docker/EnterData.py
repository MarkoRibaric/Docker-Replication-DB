import mysql.connector
from faker import Faker
import json
import time

fake = Faker()

db_config_regular = {
    'host': '127.0.0.1',
    'user': 'regular_user',
    'password': 'regularpw',
    'database': 'my_db',
    'port': 3310
}

connection_regular = mysql.connector.connect(**db_config_regular)
cursor_regular = connection_regular.cursor()

cursor_regular.execute('''
    CREATE TABLE IF NOT EXISTS mytable (
        id INT AUTO_INCREMENT PRIMARY KEY,
        data1 VARCHAR(255),
        data2 TEXT
    )
''')
connection_regular.commit()

try:
    print("Entering data into the regular server!")
    start_time_regular = time.time()
    for _ in range(100000):
        data1 = fake.word()
        data2 = fake.sentence()
        cursor_regular.execute("INSERT INTO mytable (data1, data2) VALUES (%s, %s)", (data1, data2))
    
    connection_regular.commit()
    processing_time_regular = time.time() - start_time_regular
    
    cursor_regular.execute("SELECT COUNT(*) FROM mytable;")
    row_count_regular = cursor_regular.fetchone()[0]
    processing_time_formatted_regular = "{:.4f} seconds".format(processing_time_regular)
    
    print(json.dumps({
        "message": "Entering data on Regular Server completed (might take up to a minute)",
        "processing_time": processing_time_formatted_regular,
        "row_count": row_count_regular
    }))

finally:
    cursor_regular.close()
    connection_regular.close()

db_config_replication = {
    'host': '127.0.0.1',
    'user': 'my_db_user',
    'password': 'S3cret',
    'database': 'my_db',
    'port': 3308
}

connection_replication = mysql.connector.connect(**db_config_replication)
cursor_replication = connection_replication.cursor()

cursor_replication.execute('''
    CREATE TABLE IF NOT EXISTS mytable (
        id INT AUTO_INCREMENT PRIMARY KEY,
        data1 VARCHAR(255),
        data2 TEXT
    )
''')
connection_replication.commit()

try:
    print("Entering data on replication server! (might take up to a minute)")
    start_time_replication = time.time()
    for _ in range(100000):
        data1 = fake.word()
        data2 = fake.sentence()
        cursor_replication.execute("INSERT INTO mytable (data1, data2) VALUES (%s, %s)", (data1, data2))
    
    connection_replication.commit()
    processing_time_replication = time.time() - start_time_replication
    
    cursor_replication.execute("SELECT COUNT(*) FROM mytable;")
    row_count_replication = cursor_replication.fetchone()[0]
    processing_time_formatted_replication = "{:.4f} seconds".format(processing_time_replication)
    
    print(json.dumps({
        "message": "Entering data on Replication Server completed",
        "processing_time": processing_time_formatted_replication,
        "row_count": row_count_replication
    }))

finally:
    cursor_replication.close()
    connection_replication.close()
