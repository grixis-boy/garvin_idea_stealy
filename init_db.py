from db.sql import SQLiteDB
from datetime import date


def create_tables(db):
    db.create_exercise_table()
    db.create_password_table()
    db.create_user_table()


def add_users(db):
    db.register_user(
        user_id=1,
        first_name="garvin",
        last_name="moyne",
        birth_date=date(year=1995, month=2, day=3),
        email="garvin_moyne@gmail.com",
        password=1234,
    )

    db.register_user(
        user_id=2,
        first_name="matthew",
        last_name="irwin",
        birth_date=date(year=1994, month=10, day=31),
        email="mattydirwin@gmail.com",
        password=987,
    )

    db.register_user(
        user_id=3,
        first_name="courtney",
        last_name="miller",
        birth_date=date(year=1991, month=9, day=20),
        email="counrteymiller@gmail.com",
        password=111,
    )


def add_exercises(db):
    db.register_exercise(1, exercise="running", reps=10, weight=None)
    db.register_exercise(1, exercise="squats", reps=20, weight=50)
    db.register_exercise(1, exercise="squats", reps=30, weight=40)


def main():
    db = SQLiteDB.connect("remote.db")

    create_tables(db)

    if db.check_if_empty("users"):
        add_users(db)

    if db.check_if_empty("exercises"):
        add_exercises(db)

    db.cursor.connection.close()


if __name__ == "__main__":
    main()
