import sqlite3


class ConnectDb:
    def __init__(self, db_file='account.db'):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id VARCHAR(20) PRIMARY KEY,
                user_account VARCHAR(20),
                user_password VARCHAR(20),
                isp VARCHAR(20),
                ip_master VARCHAR(20),
                method VARCHAR(20),
                login_method VARCHAR(20)
            )
        ''')
        self.connection.commit()

    def insert_user(self, user_account, user_password,isp, ip_master, method,login_method):
        self.cursor.execute('''
               INSERT OR REPLACE INTO user (id,user_account, user_password,isp, ip_master, method,login_method)
               VALUES (?,?, ?, ?,?,?,?)
           ''', (1,user_account, user_password, isp, ip_master, method,login_method))
        self.connection.commit()

    def close_connection(self):
        self.connection.close()

    def get_first_user(self):
        self.cursor.execute('SELECT * FROM user where id = 1')
        result = self.cursor.fetchone()
        return result is not None, result

    def __del__(self):
        print(f"Object for is being destroyed")
        self.close_connection()