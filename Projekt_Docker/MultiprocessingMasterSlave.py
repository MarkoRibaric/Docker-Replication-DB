import mysql.connector
from multiprocessing import Process, Queue
from mysql.connector import pooling
import time

total_rows = 100000

def initialize_connection_pool(host, port, user, password, db, pool_size=5):
    return mysql.connector.pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=pool_size,
        host=host,
        port=port,
        user=user,
        password=password,
        database=db
    )

def read_from_database(pool, start, end, result_queue):
    connection = pool.get_connection()
    cursor = connection.cursor()
    query = f"SELECT * FROM mytable WHERE id >= {start} AND id <= {end}"
    start_time = time.time()
    cursor.execute(query)
    result = cursor.fetchall()
    end_time = time.time()

    cursor.close()
    connection.close()

    elapsed_time = end_time - start_time
    result_queue.put((elapsed_time, len(result)))

if __name__ == "__main__":
    host1, port1, user1, password1, db1 = '127.0.0.1', 3309, 'my_db_user', 'S3cret', 'my_db'
    host2, port2, user2, password2, db2 = '127.0.0.1', 3308, 'my_db_user', 'S3cret', 'my_db'
    
    mid_point = total_rows // 2

    result_queue = Queue()

    connection_pool1 = initialize_connection_pool(host1, port1, user1, password1, db1)
    connection_pool2 = initialize_connection_pool(host2, port2, user2, password2, db2)

    process1 = Process(target=read_from_database, args=(connection_pool1, 1, mid_point, result_queue))
    process2 = Process(target=read_from_database, args=(connection_pool2, mid_point + 1, total_rows, result_queue))

    start_time = time.time()

    process1.start()
    process2.start()

    process1.join()
    process2.join()

    end_time = time.time()

    time1, lines1 = result_queue.get()
    time2, lines2 = result_queue.get()

    total_elapsed_time = end_time - start_time
    print(f"Total time elapsed: {total_elapsed_time:.2f} seconds")
    print(f"Time for process 1: {time1:.2f} seconds, Lines retrieved: {lines1}")
    print(f"Time for process 2: {time2:.2f} seconds, Lines retrieved: {lines2}")
