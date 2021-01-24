# Module Imports
import pymysql
import sys
import uuid

# import mariadb

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
USER = 100
PROFILE = 95
GAME = 90
ROUND = 85
MATCH = 80


# id : 4-20자의 영문 소문자, 숫자, (_),(-)만 가능 : 이거 나중에 email값으로 바꿔도 될 듯
# pw : 8~16자 영문 대 소문자, 숫자, 특수문자
# device_num : 20자?

# country : korea(0)
def create_table(mode):
    # create table : user, game,

    sql = str()
    if mode == USER:
        sql = "CREATE TABLE IF NOT EXISTS user (" \
              " id char(20) UNIQUE, " \
              " password char(16), " \
              " name char(20), " \
              " country int, " \
              " device char(20) UNIQUE, " \
              " time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP," \
              " locked boolean," \
              " token char(36) UNIQUE" \
              ")"  # 실행할 sql문 cur.execute(sql) # 커서로 sql문 실행
    elif mode == PROFILE:
        sql = "CREATE TABLE IF NOT EXISTS profile (" \
              " user_token char(36)," \
              " country int," \
              " win unsigned int," \
              " total_count unsigned int," \
              " photo int," \
              " time datetime," \
              "FOREIGN KEY (user_token) REFERENCES user(token)" \
              ")"  # 실행할 sql문 cur.execute(sql) # 커서로 sql문 실행
    elif mode == MATCH:
        sql = "CREATE TABLE IF NOT EXISTS game (" \
              "id char(4)," \
              " userName char(10)," \
              " email char(15)," \
              " birthYear int" \
              ")"  # 실행할 sql문 cur.execute(sql) # 커서로 sql문 실행
    elif mode == GAME:
        sql = "CREATE TABLE IF NOT EXISTS round (" \
              "id char(4)," \
              " userName char(10)," \
              " email char(15)," \
              " birthYear int" \
              ")"  # 실행할 sql문 cur.execute(sql) # 커서로 sql문 실행
    cur.execute(sql)
    conn.commit()


# insert
def join(id, pw, name, country, device):
    try:
        sql = "INSERT INTO user (id, password, name, country, device, locked, token) values (%s, %s, %s, %s, %s, %s, %s)"
        val = (id, pw, name, country, device, False, str(uuid.uuid4()))
        cur.execute(sql, val)
        rows = cur.fetchall()
        conn.commit()
        return True, str()
    except pymysql.err.IntegrityError as error:
        # print(error.args[1])
        return False, error.args[1]


# select(search)
def login(id, pw, device):
    sql = "select token from user where id=%s and password=%s and device=%s"
    cur.execute(sql, (id, pw, device))
    # DB결과를 모두 가져올 때 사용
    rows = cur.fetchall()
    return rows[0][0]


def drop_table(mode):
    try:
        # drop table
        sql = str()
        if mode == USER:
            sql = "DROP TABLE user"
        elif mode == PROFILE:
            sql = "DROP TABLE profile"
        elif mode == GAME:
            sql = "DROP TABLE game"
        elif mode == MATCH:
            sql = "DROP TABLE match"
        cur.execute(sql)
        conn.commit()
        conn.close()
    except pymysql.err.OperationalError as error:
        print(error.args[1])


# create_table(USER)
# join("aaa", "1434", "kkk", 1, "MAC123")
# drop_table(USER)
print(login("aaa", "1434", "MAC123"))
# conn.close()
