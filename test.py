# %%
from db.sql import SQLiteDB


db = SQLiteDB.connect("remote.db")
# %%
db.retrieve_exercise(1).plot()


# %%
