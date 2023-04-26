from owltracker.data.database.database_base import DatabaseBase
from owltracker.data.database.sqlite.sqlite_database import SQLiteDatabase

class Database(DatabaseBase):
    def __init__(self) -> None:
        self.__class__ = SQLiteDatabase
        self.__init__()


if __name__ == "__main__":
    db = Database()
    from datetime import datetime
    db.excecute_query_format("UPDATE activity set end = (?) WHERE id = (SELECT MAX(id) FROM activity);", [datetime.now()])
    print(db.select_query("Select * from activity;"))
