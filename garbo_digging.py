# %%
from datetime import date
import sqlite3
from pathlib import Path
import pandas as pd

with sqlite3.connect("remote.db") as conn:
    ex_table = pd.read_sql_query(
        f"select exercise, reps, weight from exercises where id==1;",
        con=conn,
    )
# %%
