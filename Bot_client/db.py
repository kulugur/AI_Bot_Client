import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id= ?", (user_id,)).fetchall()
            return bool(len(result))
    def set_nickname(self, user_id, nickname ):
        with self.connection:
            return self.cursor.execute("UPDATE users SET nickname=? WHERE user_id=?", (nickname, user_id,))

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE users SET signup=? WHERE user_id=?", (signup, user_id,))
    def set_subscription(self, user_id,subscription):
        with self.connection:
             return self.cursor.execute("UPDATE users SET subscription=? WHERE user_id=?", (subscription, user_id,))
    def set_payment(self, user_id,payment):
        with self.connection:
             return self.cursor.execute("UPDATE users SET payment=? WHERE user_id=?", (payment, user_id,))
    def set_wallet(self, user_id,wallet):
        with self.connection:
             return self.cursor.execute("UPDATE users SET wallet=? WHERE user_id=?", (wallet, user_id,))

    def set_start(self, user_id, start):
        with self.connection:
            return self.cursor.execute("UPDATE users SET start=? WHERE user_id=?", (start, user_id,))

    def set_profit_2(self, user_id, profit_2):
        with self.connection:
            return self.cursor.execute("UPDATE users SET profit_2=? WHERE user_id=?", (profit_2, user_id,))

    def set_rsi(self, user_id, rsi):
        with self.connection:
            return self.cursor.execute("UPDATE users SET rsi=? WHERE user_id=?", (rsi, user_id,))

    def set_averaging(self, user_id, averaging):
        with self.connection:
            return self.cursor.execute("UPDATE users SET averaging=? WHERE user_id=?", (averaging, user_id,))

    def set_binance_traid(self, user_id, binance_traid):
        with self.connection:
            return self.cursor.execute("UPDATE users SET binance_traid=? WHERE user_id=?", (binance_traid, user_id,))
    def set_position_balance(self, user_id, position_balance):
        with self.connection:
            return self.cursor.execute("UPDATE users SET position_balance=? WHERE user_id=?", (position_balance, user_id,))


    def set_secret_key(self, user_id, secret_key):
        with self.connection:
            return self.cursor.execute("UPDATE users SET secret_key=? WHERE user_id=?", (secret_key, user_id,))
    def set_api_key(self, user_id, api_key):
        with self.connection:
            return self.cursor.execute("UPDATE users SET api_key=? WHERE user_id=?", (api_key, user_id,))

    def set_binance_balance(self, user_id, balance):
        with self.connection:
            return self.cursor.execute("UPDATE users SET binance_balance=? WHERE user_id=?", (balance, user_id,))

    def set_language(self, user_id, language):
        with self.connection:
            return self.cursor.execute("UPDATE users SET language=? WHERE user_id=?", (language, user_id,))

    def set_position(self, user_id, position_1m, position):
        with self.connection:
            return self.cursor.execute(f"UPDATE users SET {position_1m}=? WHERE user_id=?", (position, user_id,))

    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT signup FROM users WHERE user_id=?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup
    def set_deposit_demo(self, user_id, deposit_demo):
        with self.connection:
            return self.cursor.execute("UPDATE users SET deposit_demo=? WHERE user_id=?", (deposit_demo, user_id,))

    def get_deposit_demo(self, user_id):
        with self.connection:
             return self.cursor.execute("SELECT deposit_demo FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
    def get_all(self):
        return self.cursor.execute("SELECT * FROM users " ).fetchall()
    def get_nickname(self, user_id):
        with self.connection:
             return self.cursor.execute("SELECT nickname FROM users WHERE user_id=?", (user_id,)).fetchone()[0]

    def get_id(self, pay_id):
        with self.connection:
             return self.cursor.execute("SELECT user_id FROM users WHERE wallet=?", (pay_id,)).fetchone()[0]

    def get_time_sub(self, user_id):
        with self.connection:
             return self.cursor.execute("SELECT time_sub FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
    def get_subscription(self, user_id):
        with self.connection:
             return self.cursor.execute("SELECT subscription FROM users WHERE user_id=?", (user_id,)).fetchone()[0]

    def get_start(self, user_id):
        with self.connection:
             return self.cursor.execute("SELECT start FROM users WHERE user_id=?", (user_id,)).fetchone()[0]

    def get_profit_2(self, user_id):
        with self.connection:
             return self.cursor.execute("SELECT profit_2 FROM users WHERE user_id=?", (user_id,)).fetchone()[0]

    def get_rsi(self, user_id):
        with self.connection:
             return self.cursor.execute("SELECT rsi FROM users WHERE user_id=?", (user_id,)).fetchone()[0]

    def get_binance_traid(self, user_id):
        with self.connection:
             return self.cursor.execute("SELECT binance_traid FROM users WHERE user_id=?", (user_id,)).fetchone()[0]

    def get_averaging(self, user_id):
        with self.connection:
             return self.cursor.execute("SELECT averaging FROM users WHERE user_id=?", (user_id,)).fetchone()[0]

    def get_payment(self, user_id):
        with self.connection:
             return self.cursor.execute("SELECT payment FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
    def get_oll_subscription(self, subscription):
        with self.connection:
             return self.cursor.execute("SELECT * FROM users WHERE subscription=?", (subscription,)).fetchall()

    def get_wallet(self, user_id):
        with self.connection:
             return self.cursor.execute("SELECT wallet FROM users WHERE user_id=?", (user_id,)).fetchone()[0]

    def get_wallet_all(self):
        with self.connection:
            result = self.cursor.execute("SELECT wallet FROM users  ").fetchall()
            pay_id = []
            for row in result:
                pay_id.append(str(row[0]))
            return pay_id

    def get_language(self, user_id):
        with self.connection:
             return self.cursor.execute("SELECT language FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
    def get_secret_key(self, user_id):
        with self.connection:
             return self.cursor.execute("SELECT secret_key FROM users WHERE user_id=?", (user_id,)).fetchone()[0]

    def get_api_key(self, user_id):
        with self.connection:
             return self.cursor.execute("SELECT api_key FROM users WHERE user_id=?", (user_id,)).fetchone()[0]


    def get_position(self, user_id, position_1m,):
        with self.connection:
             return self.cursor.execute(f"SELECT {position_1m} FROM users WHERE user_id=?", (user_id,)).fetchone()[0]

    def get_position_balance(self, user_id,):
        with self.connection:
             return self.cursor.execute("SELECT position_balance FROM users WHERE user_id=?", (user_id,)).fetchone()[0]

