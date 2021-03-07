import pymysql
import sys
import uuid

# import mariadb

# Get Cursor

USER = 100
PROFILE = 95
GAME = 90# GAME > RESULT
# ROUND = 85
WAIT = 85
MATCH = 80
CHOICE = 75
RESULT = 70


KOREA = 10
# id : 4-20자의 영문 소문자, 숫자, (_),(-)만 가능 : 이거 나중에 email값으로 바꿔도 될 듯
# pw : 8~16자 영문 대 소문자, 숫자, 특수문자
# device_num : 20자?

WAITING = 0
PLAYING = 1

USER_CHOICE = 0
AUTO_CHOICE = 1


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
                  " total_round int unsigned," \
                  " photo int," \
                  " time datetime," \
                  "FOREIGN KEY (user_token) REFERENCES user(token)" \
                  ")"  # 실행할 sql문 cur.execute(sql) # 커서로 sql문 실행
        elif mode == WAIT:
            sql = "CREATE TABLE IF NOT EXISTS waiting (" \
                  " user_token char(36) PRIMARY KEY," \
                  " time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP" \
                  ")"  # 실행할 sql문 cur.execute(sql) # 커서로 sql문 실행
        elif mode == MATCH:
            sql = "CREATE TABLE IF NOT EXISTS matches (" \
                  " user_token char(36) PRIMARY KEY," \
                  " rival_token char(36) UNIQUE," \
                  " game_token char(36)," \
                  " matched_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP," \
                  " CONSTRAINT matches_unique UNIQUE (user_token)"\
                  ")"  # 실행할 sql문 cur.execute(sql) # 커서로 sql문 실행
        elif mode == CHOICE:
            sql = "CREATE TABLE IF NOT EXISTS choice (" \
                  " user_token char(36) PRIMARY KEY," \
                  " choice int unsigned," \
                  " detail int unsigned," \
                  " matched_time TIMESTAMP," \
                  " choice_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP" \
                  ")"  # 실행할 sql문 cur.execute(sql) # 커서로 sql문 실행
        elif mode == RESULT:
            sql = "CREATE TABLE IF NOT EXISTS result (" \
                  " game_token char(36)," \
                  " player char(36)," \
                  " player_choice int," \
                  " win TINYINT,"\
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
            print("[join] rows : ", rows)
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
        print("[login] rows : ", rows)
        return rows

    def del_user(self, id, pw, country):
        try:
            sql = "delete from user where id=%s and password=%s and country=%s"
            val = (id, pw, country)
            result = self.cur.execute(sql, val)
            self.conn.commit()
            # print("result : ", result, type(result))
            if result == 0:
                return False
            else:
                return True
        except:
            print(sys.exc_info())

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
        sql = "select user_token, state from matches where user_token!=%s"
        self.cur.execute(sql, user_token)
        rows = self.cur.fetchall()
        self.conn.commit()
        print("rows:", rows)
        return rows

    def get_user_state(self, user_token):
        sql = "select user_token from waiting where user_token=%s"
        self.cur.execute(sql, user_token)
        rows = self.cur.fetchall()
        self.conn.commit()
        print("rows:", rows)
        if rows:
            return WAITING, None
        else:
            sql = "select game_token, rival_token from matches where user_token=%s"
            self.cur.execute(sql, user_token)
            matches_result = self.cur.fetchall()
            self.conn.commit()
            print("rows:", rows)
            if matches_result:
                return PLAYING, matches_result
            else:
                # waiting도 playing도 아닌 상황. 그 이전의 상황일 경우
                return None, None

    def insert_waiting(self, user_token):
        sql = "INSERT INTO waiting user_token values (%s) "
        # val = (, WAITING)
        self.cur.execute(sql, user_token)
        rows = self.cur.fetchall()
        self.conn.commit()
        return rows

    def get_waiting_list(self):
        sql = "SELECT user_token from waiting order by time ASC"
        self.cur.execute(sql, user_token)
        rows = self.cur.fetchall()
        return rows

    def set_match(self, user_token, rival_token, game_token):
        # return game_token.
        sql = "INSERT INTO matches (user_token, rival_token, game_token) values (%s, %s, %s) "
        val = (user_token, rival_token, game_token)
        self.cur.execute(sql, val)
        rows = self.cur.fetchall()
        self.conn.commit()
        return rows

    def get_match_list(self, user_token):
        sql = "SELECT game_token, rival_token from matches WHERE user_token=%s"
        self.cur.execute(sql, user_token)
        rows = self.cur.fetchall()
        return rows

    def set_wait(self, user_token):
        # sql = "update match set "
        sql = "SELECT user_token from matches where user_token=%s"
        self.cur.execute(sql, user_token)
        rows = self.cur.fetchall()
        print("select matches table : ", rows)
        self.conn.commit()
        if not rows: #no exist
            sql = "INSERT INTO matches (user_token, state) values (%s, %s) "
            val = (user_token, WAITING)
            self.cur.execute(sql, val)
            rows = self.cur.fetchall()
            self.conn.commit()
            return rows
        else: #exist
            return None

    def rm_from_wait(self, user_token):
        sql = "DELETE FROM waiting WHERE user_token = (%s)"
        self.cur.execute(sql, user_token)
        rows = self.cur.fetchall()
        self.conn.commit()
        return rows

    def matching_success(self, player1, player2):
        # insert game table.
        game_token = str(uuid.uuid4())
        sql = "INSERT INTO game (user_token, state) values (%s, %s) "
        val = (user_token, WAITING)
        self.cur.execute(sql, val)
        rows = self.cur.fetchall()
        self.conn.commit()
        print("[matching_success] rows :", rows)
        return rows, game_token

    def get_game(self, user_token):
        sql = "SELECT game_token from game where player1=%s or player2=%s"
        self.cur.execute(sql, (user_token, user_token))
        rows = self.cur.fetchall()
        self.conn.commit()
        print("[get game] rows : ", rows)
        return rows

    def set_choice(self, user_token, game_token, choice, choice_time):
        sql = "SELECT game_token from game where player1=%s or player2=%s"
        self.cur.execute(sql, (user_token, user_token))
        get_matched_time = self.cur.fetchall()
        self.conn.commit()

        sql = "INSERT INTO choice (user_token, choice, detail, matched_time, choice_time) values (%s, %s) "
        val = (user_token, choice, USER_CHOICE, get_matched_time, choice_time)
        self.cur.execute(sql, val)
        rows = self.cur.fetchall()
        self.conn.commit()
        print("[set_choice] rows :", rows)
        return rows

    def am_i_win(self, game_token, user_token):
        sql = "SELECT win from result where game_token=%s and win!=NULL and player=%s"
        val = (game_token, user_token, user_token)
        self.cur.execute(sql, val)
        rows = self.cur.fetchall()
        self.conn.commit()
        print("[get_result] rows : ", rows)
        if rows: # if result exist.
            if rows[0][0] == user_token:
                return True, user_token
            else:
                return False, user_token
        else:
            return False, None

    def get_choices(self, game_token):
        sql = "SELECT user_token, choice from choice where game_token=%s"
        self.cur.execute(sql, game_token)
        user_token = self.cur.fetchall()
        self.conn.commit()
        return user_token

    def get_win_record(self, user_token):
        sql = "SELECT win, total_round from profile where user_token=%s"
        self.cur.execute(sql, user_token)
        win_record = self.cur.fetchall()
        self.conn.commit()
        return win_record

    def update_profile_win(self, user_token, win):
        # UPDATE table_1 SET column_1 = 'x' WHERE column_2 = 'aa';
        sql = "UPDATE profile SET win = (%s) WHERE user_token = (%s)"
        val = (win, user_token)
        self.cur.execute(sql, val)
        rows = self.cur.fetchall()
        self.conn.commit()
        print("[update_profile_win] rows :", rows)
        return rows

    def update_result(self, game_token, user_token, win):
        sql = "UPDATE result SET win = (%s) WHERE game_token = (%s) and user_token = (%s)"
        val = (win, game_token, user_token)
        self.cur.execute(sql, val)
        rows = self.cur.fetchall()
        self.conn.commit()

        sql = "UPDATE result SET win = (%s) WHERE game_token = (%s) and user_token != (%s)"
        val = (not win, game_token, user_token)
        self.cur.execute(sql, val)
        rows = self.cur.fetchall()
        self.conn.commit()
        # print("[update_profile_win] rows :", rows)
        # return rows

    # def logout(self, user_token):



# db_manager = DBManager()
# # new_table_list = [PROFILE, USER, MATCH, GAME]
# # for table in new_table_list:
# #     print(table)
# #     db_manager.drop_table(table)
# # conn.close()
# # create_table(USER)
# # db_manager.join("aaa", "1434", "kkk", KOREA, "MAC123")
# user_token = db_manager.login("aaa", "1434", "MAC123")
# print("user_token : ", user_token)
# print(db_manager.set_wait("64138ab1-91b0-4ed7-b395-5a780f843c21"))
# # db_manager.del_user(user_token)
# 
# # print(db_manager.login("aaa", "1434", "MAC123"))
# r_uuid = db_manager.get_user_state("64138ab1-91b0-4ed7-b395-5a780f843c21")
# if r_uuid:
#     print(r_uuid[0])
#     print("rival_r_uuid[0][0], r_uuid[0][1]")
# # conn.close()
# 
# # db_manager.get_game(user_token)
