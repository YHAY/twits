import pymysql
import sys
import uuid

# import mariadb



# Get Cursor

USER = 100
PROFILE = 95
GAME = 90
ROUND = 85
MATCH = 80


# id : 4-20자의 영문 소문자, 숫자, (_),(-)만 가능 : 이거 나중에 email값으로 바꿔도 될 듯
# pw : 8~16자 영문 대 소문자, 숫자, 특수문자
# device_num : 20자?

class DBManager:
    def __init__(self):
        # Connect to MariaDB Platform
        try:
            self.conn = pymysql.connect(
                host='localhost',
                user='admin',
                password='admin',
                db='example_db',
                charset='utf8'
            )  # 접속정보

        except pymysql.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        self.cur = self.conn.cursor()
        # create tables
        sql = "show tables"
        self.cur.execute(sql)
        self.conn.commit()
        rows = self.cur.fetchall()
        print("rows :", rows[0])

        new_table_list = [USER, PROFILE, MATCH, GAME]
        for table in rows[0]:
            if table == "user":
                new_table_list.remove(USER)
            elif table == "profile":
                new_table_list.remove(PROFILE)
            elif table == "matches":
                new_table_list.remove(MATCH)
            elif table == "game":
                new_table_list.remove(GAME)



        print("new_table_list : ", new_table_list)
        for element in new_table_list:
            print(element)
            self.create_table(element)
            # self.create_table(USER)
            # self.create_table(PROFILE)
            # self.create_table(MATCH)
            # self.create_table(GAME)

    def __del__(self):
        self.conn.close()

    # country : korea(0)
    def create_table(self, mode):
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
                  " win int unsigned," \
                  " total_count int unsigned," \
                  " photo int," \
                  " time datetime," \
                  "FOREIGN KEY (user_token) REFERENCES user(token)" \
                  ")"  # 실행할 sql문 cur.execute(sql) # 커서로 sql문 실행
        elif mode == MATCH:
            sql = "CREATE TABLE IF NOT EXISTS matches (" \
                  " user_token char(36) PRIMARY KEY," \
                  " state int unsigned," \
                  " matched_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP," \
                  " CONSTRAINT matches_unique UNIQUE (user_token)"\
                  ")"  # 실행할 sql문 cur.execute(sql) # 커서로 sql문 실행
        elif mode == GAME:
            sql = "CREATE TABLE IF NOT EXISTS game (" \
                  " game_token char(36)," \
                  " player1 char(36)," \
                  " player1_choice int," \
                  " player2 char(36)," \
                  " player2_choice int," \
                  " win char(20),"\
                  " time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP" \
                  ")"  # 실행할 sql문 cur.execute(sql) # 커서로 sql문 실행
        print(sql)
        self.cur.execute(sql)
        self.conn.commit()

    # insert
    def join(self, id, pw, name, country, device):
        try:
            sql = "INSERT INTO user (id, password, name, country, device, locked, token) values (%s, %s, %s, %s, %s, " \
                  "%s, %s) "
            val = (id, pw, name, country, device, False, str(uuid.uuid4()))
            self.cur.execute(sql, val)
            rows = self.cur.fetchall()
            self.conn.commit()
            return True, str()
        except pymysql.err.IntegrityError as error:
            # print(error.args[1])
            return False, error.args[1]

    # select(search)
    def login(self, id, pw, device):
        sql = "select token from user where id=%s and password=%s and device=%s"
        self.cur.execute(sql, (id, pw, device))
        # DB결과를 모두 가져올 때 사용
        rows = self.cur.fetchall()
        return rows[0][0]

    def del_user(self, user_token):
        sql = "delete from user where token=%s"
        val = user_token
        self.cur.execute(sql, (val))
        self.conn.commit()

    def drop_table(self, mode):
        try:
            # drop table
            sql = str()
            if mode == USER:
                sql = "DROP TABLE IF EXISTS user"
            elif mode == PROFILE:
                sql = "DROP TABLE IF EXISTS profile"
            elif mode == GAME:
                sql = "DROP TABLE IF EXISTS game"
            elif mode == MATCH:
                sql = "DROP TABLE IF EXISTS matches"
            self.cur.execute(sql)
            self.conn.commit()
            # conn.close()
        except pymysql.err.OperationalError as error:
            print(error.args[1])

    def get_match(self, user_token):
        sql = "select user_token from matches where state=0 and user_token!=%s"
        self.cur.execute(sql, user_token)
        rows = self.cur.fetchall()
        self.conn.commit()
        print("rows:", rows)
        return rows

    def set_wait(self, user_token):
        # sql = "update match set "
        sql = "SELECT user_token from matches where user_token=%s"
        self.cur.execute(sql, user_token)
        rows = self.cur.fetchall()
        self.conn.commit()
        if not rows: #no exist
            sql = "INSERT INTO matches (user_token, state) values (%s, %s) "
            val = (user_token, 0)
            self.cur.execute(sql, val)
            rows = self.cur.fetchall()
            self.conn.commit()
            return rows
        else: #exist
            return None

    # def update_matching(self, user_token, rival_uuid):
        #insert game table.


db_manager = DBManager()
# new_table_list = [PROFILE, USER, MATCH, GAME]
# for table in new_table_list:
#     print(table)
#     db_manager.drop_table(table)
# conn.close()
# create_table(USER)
# join("aaa", "1434", "kkk", 1, "MAC123")
db_manager.set_wait("b878c7be-393a-4259-8011-0772154613d9")

# print(db_manager.login("aaa", "1434", "MAC123"))
# db_manager.get_match("b878c7be-393a-4259-8011-0772154613d89")
# conn.close()
