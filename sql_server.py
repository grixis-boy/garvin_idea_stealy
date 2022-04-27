# %%
from datetime import date
import sqlite3
from pathlib import Path
import pandas as pd

# %%
class LoginError(Exception):
    ...


class UserError(Exception):
    ...


def create_user_table(conn: sqlite3.Connection) -> None:
    command = """
    create table if not exists users (
        id integer primary key,
        first_name text not null,
        last_name text not null,
        birth_date text not null,
        email_address text not null
    );
    """

    cur = conn.cursor()
    cur.execute(command)


def create_password_table(conn: sqlite3.Connection):
    command = """
    create table if not exists passwords (
        id integer primary key,
        password integer
    );
    """
    cur = conn.cursor()
    cur.execute(command)


def create_exercise_table(conn: sqlite3.Connection):
    command = """
    create table if not exists exercises (
        exercise_id integer primary key,
        id integer,
        exercise str,
        reps int,
        weight int
    );
    """
    cur = conn.cursor()
    cur.execute(command)


def register_user(
    conn: sqlite3.Connection,
    user_id: int,
    first_name: str,
    last_name: str,
    birth_date: date,
    email: str,
    password: int,
):

    cur = conn.cursor()

    user_command = """insert into users(id, first_name, last_name, birth_date, email_address) 
    values(?,?,?,?,?)"""

    password_command = """insert into passwords(id, password) 
    values(?,?)"""

    cur.execute(user_command, [user_id, first_name, last_name, birth_date, email])
    cur.execute(password_command, [user_id, password])

    conn.commit()


def register_exercise(
    conn: sqlite3.Connection, user_id: int, exercise: str, reps: int, weight: int
):

    cur = conn.cursor()

    command = """insert into exercises(id, exercise, reps, weight) 
    values(?,?,?,?)"""

    cur.execute(command, [user_id, exercise, reps, weight])

    conn.commit()


def login(user_id: str, password: str, conn: sqlite3.Connection):
    cur = conn.cursor()

    try:
        stored_password = next(
            cur.execute(f"select password from passwords where id=={user_id};")
        )[0]

    except StopIteration:
        raise UserError("User does not exist")

    if password != stored_password:
        raise LoginError("Incorrect Password")

    return True


def main():
    with sqlite3.connect("remote.db") as conn:
        create_user_table(conn)
        create_password_table(conn)
        create_exercise_table(conn)

        # register_user(
        #     conn=conn,
        #     user_id=1,
        #     first_name="garvin",
        #     last_name="moyne",
        #     birth_date=date(year=1995, month=2, day=3),
        #     email="garvin_moyne@gmail.com",
        #     password=1234,
        # )

        # register_user(
        #     conn=conn,
        #     user_id=2,
        #     first_name="matthew",
        #     last_name="irwin",
        #     birth_date=date(year=1994, month=10, day=31),
        #     email="mattydirwin@gmail.com",
        #     password=987,
        # )'

        while True:
            u_id = input("user_id: ")
            pwd = int(input("password: "))

            auth_check = login(user_id=u_id, password=pwd, conn=conn)

            if auth_check:
                exercise = input("exercise: ")
                reps = input("reps: ")
                weight = input("weight: ")
                register_exercise(conn, u_id, exercise, reps, weight)

                ex_table = pd.read_sql_query(
                    f"select exercise, reps, weight from exercises where id=={u_id};",
                    con=conn,
                )

                email = input(
                    "Do you want us to send you a copy of your records: (y/n)"
                ).lower()

                if email == "y":
                    print(
                        next(
                            conn.execute(
                                f"select email_address from users where id=={u_id}"
                            )
                        )[0]
                    )

        # while True:
        #     fname = input("first name: ")
        #     lname = input("last name: ")
        #     dob = input("date_of_birth: ")
        #     email = input("email: ")
        #     register_user(conn, fname, lname, dob, email)


if __name__ == "__main__":
    main()

# %%
