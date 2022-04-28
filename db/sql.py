from dataclasses import dataclass, field
import sqlite3
from typing import Protocol
from datetime import date
import pandas as pd


class DataBase(Protocol):
    def create_user_table(self):
        ...

    def create_password_table(self):
        ...

    def create_exercise_table(self):
        ...

    def register_user(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        birth_date: date,
        email: str,
        password: int,
    ):
        ...

    def register_exercise(self, user_id: int, exercise: str, reps: int, weight: int):
        ...

    def retrieve_exercise(self, user_id: int):
        ...


@dataclass
class SQLiteDB:
    cursor: sqlite3.Cursor

    @staticmethod
    def connect(db_name: str):
        return SQLiteDB(sqlite3.connect(db_name).cursor())

    def _commit(self):
        self.cursor.connection.commit()

    def create_exercise_table(self):
        self.cursor.execute(
            """
            create table if not exists exercises (
                exercise_id integer primary key,
                id integer,
                exercise str,
                reps int,
                weight int
            );
            """
        )

        self._commit()

    def create_password_table(self):
        self.cursor.execute(
            """
            create table if not exists passwords (
                id integer primary key,
                password integer
            );
            """
        )

        self._commit()

    def create_user_table(self):
        self.cursor.execute(
            """
            create table if not exists users (
                id integer primary key,
                first_name text not null,
                last_name text not null,
                birth_date text not null,
                email_address text not null
            );
            """
        )
        self._commit()

    def register_user(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        birth_date: date,
        email: str,
        password: int,
    ):

        user_command = """insert into users(id, first_name, last_name, birth_date, email_address)
        values(?,?,?,?,?)"""

        password_command = """insert into passwords(id, password)
        values(?,?)"""

        self.cursor.execute(
            user_command, [user_id, first_name, last_name, birth_date, email]
        )
        self.cursor.execute(password_command, [user_id, password])

        self._commit()

    def register_exercise(self, user_id: int, exercise: str, reps: int, weight: int):

        self.cursor.execute(
            "insert into exercises(id, exercise, reps, weight) values(?,?,?,?)",
            [user_id, exercise, reps, weight],
        )
        self._commit()

    def retrieve_exercise(self, user_id: int):
        return pd.read_sql_query(
            f"select exercise, reps, weight from exercises where id=={user_id};",
            con=self.cursor.connection,
        )

    def check_if_empty(self, table: str):
        return self.cursor.execute(f"select count(*) from {table}").fetchone() == (0,)
