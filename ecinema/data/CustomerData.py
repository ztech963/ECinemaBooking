from ecinema.data.access import DataAccess
from ecinema.data.db import get_db


class CustomerData(DataAccess):

    def __init__(self):
        self.__db = get_db()

    def get_info(self, key: str):
        return self.get_user_info(key)

    def insert_info(self, data) -> str:
        cursor = self.__db.cursor()
        cursor.execute(
            'INSERT INTO customer (first_name, last_name, '
            'email, subscribe_to_promo, username, password, status) '
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            data
        )
        row_id = cursor.lastrowid
        self.__db.commit()
        return row_id

    def update_info(self, data) -> str:
        self.__db.execute(
            'UPDATE customer SET first_name = ?, last_name = ?, '
            'email = ?, subscribe_to_promo = ?, username = ?, '
            'password = ?, status = ?, address_id = ? WHERE username = ?',
            data
        )
        self.__db.commit()

    def get_user_info(self, user_id: str):
        return self.__db.execute(
            'SELECT * FROM customer WHERE username = ?', (user_id,)
        ).fetchone()

    def get_info_by_email(self, email: str):
        return self.__db.execute(
            'SELECT * FROM customer WHERE email = ?', (email,)
        ).fetchone()

    def set_first_name(self, cid: str, first: str):
        self.__db.execute(
            'UPDATE customer SET first_name = ? WHERE customer_id = ?',
            (first, cid)
        )
        self.__db.commit()

    def set_last_name(self, cid: str, last: str):
        self.__db.execute(
            'UPDATE customer SET last_name = ? WHERE customer_id = ?',
            (last, cid)
        )
        self.__db.commit()

    def set_email(self, cid: str, email: str):
        self.__db.execute(
            'UPDATE customer SET email = ? WHERE customer_id = ?',
            (email, cid)
        )
        self.__db.commit()
