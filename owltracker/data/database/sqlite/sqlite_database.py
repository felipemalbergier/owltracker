import sqlite3

from owltracker.data.database.database_base import DatabaseBase
from owltracker.data.database.sqlite.create_sqlite_database import get_query_create_activity_table, get_query_create_task_source_table, get_query_create_task_table
from owltracker.utils import WAIT_TIME_MSECONDS


class SQLiteDatabase(DatabaseBase):
    DB_NAME = "sqlite_owltracker.db"

    def __init__(self) -> None:
        self.connection = sqlite3.connect(self.DB_NAME)
        self.cursor = self.connection.cursor()
        self.last_process_name = None
        self.last_window_title = None

    def excecute_query(self, query, values=None, commit=False):
        try:
            response = self.cursor.execute(query, tuple(values) or tuple())
        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                self.create_all_tables()

        if commit:
            self.connection.commit()
        return response.fetchall()

    def excecute_script(self, script):
        response = self.cursor.executescript(script)

    def __del__(self):
        self.connection.close()

    def update_end_activity(self, end):
        query = f"""UPDATE activity set end = (?) WHERE id = (SELECT MAX(id) FROM activity);"""
        self.excecute_query(query, [end], commit=True)

    def add_new_activity(self, activity):
        query = f"INSERT INTO activity ({','.join(activity.keys())}) VALUES ({','.join(['?'] * len(activity))});"
        self.excecute_query(query, activity.values(), commit=True)

    def create_all_tables(self):
        self.excecute_query(get_query_create_activity_table())
        self.excecute_query(get_query_create_task_table())
        self.excecute_query(get_query_create_task_source_table())


if __name__ == '__main__':
    sql = SQLiteDatabase()
    sql.add_activity(**{"process_name": "test_name",
                     "window_title": "window_title"})
    print(sql.excecute_query("select * from activity;"))
