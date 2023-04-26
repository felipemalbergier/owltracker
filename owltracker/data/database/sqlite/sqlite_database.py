from datetime import datetime
from datetime import timezone
from datetime import timedelta
import sqlite3

from owltracker.data.database.database_base import DatabaseBase
from owltracker.utils import WAIT_TIME_MSECONDS


class SQLiteDatabase(DatabaseBase):
    DB_NAME = "sqlite_owltracker.db"

    def __init__(self) -> None:
        self.connection = sqlite3.connect(self.DB_NAME)
        self.cursor = self.connection.cursor()
        self.last_process_name = None
        self.last_window_title = None

    def select_query(self, query):
        response = self.cursor.execute(query)
        return response.fetchall()

    def insert_query(self, query):
        response = self.cursor.execute(query)
        self.connection.commit()

    def insert_query_format(self, query, values):
        response = self.cursor.execute(query, tuple(values))
        self.connection.commit()

    def excecute_script(self, script):
        response = self.cursor.executescript(script)

    def __del__(self):
        self.connection.close()

    def add_activity(self, **kwargs):
        # If last process name is the same - I update end datetime
        if (self.last_process_name == kwargs.get('process_name', '') and self.last_window_title == kwargs.get('window_title', '')):
            kwargs['end'] = datetime.now(timezone.utc) + timedelta(milliseconds=WAIT_TIME_MSECONDS)
            query = f"""UPDATE activity set end = (?) WHERE id = (SELECT MAX(id) FROM activity);"""
            self.excecute_query_format(query, [kwargs['end']])
        else:  # (else) if last process name is null or different I add start datetime and end datetime
            kwargs['start'] = datetime.now(timezone.utc)
            kwargs['end'] = datetime.now(timezone.utc) + timedelta(milliseconds=WAIT_TIME_MSECONDS)
            query = f"INSERT INTO activity ({','.join(kwargs.keys())}) VALUES ({','.join(['?'] * len(kwargs))});"
            self.insert_query_format(query, kwargs.values())

        self.last_process_name = kwargs['process_name']
        self.last_window_title = kwargs['window_title']


if __name__ == '__main__':
    sql = SQLiteDatabase()
    sql.add_activity(**{"process_name": "test_name",
                     "window_title": "window_title"})
    print(sql.select_query("select * from activity;"))
