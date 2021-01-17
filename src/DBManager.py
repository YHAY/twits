# Module Imports
import pymysql
import sys

# Connect to MariaDB Platform
try:
    conn = pymysql.connect(
        host='localhost',
        user='admin',
        password='admin',
        db='example_db',
        charset='utf8'
    )  # 접속정보

except pymysql.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

# create table
sql = "CREATE TABLE IF NOT EXISTS userTable (id char(4), userName char(10), email char(15), birthYear int)" # 실행할 sql문 cur.execute(sql) # 커서로 sql문 실행
cur.execute(sql)
conn.commit()

# drop table
drop_table = "DROP TABLE userTable";
cur.execute(drop_table)
conn.commit()

# select(search)


# insert

conn.close()