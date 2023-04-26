from sqlite_database import SQLiteDatabase


def get_create_db_query(drop_tables=False):

    query = """
    CREATE TABLE IF NOT EXISTS activity (
        id INTEGER PRIMARY KEY,
        process_name TEXT,
        window_title TEXT,
        start DATETIME NOT NULL,
        end DATETIME
        
        ) ;
    
    """
    if drop_tables:
        query = "DROP TABLE IF EXISTS activity;" + query

    return query


if __name__ == "__main__":
    query = get_create_db_query(True)
    sql = SQLiteDatabase()
    sql.excecute_script(query)
    # sql.insert_query("INSERT INTO activity (process_name, window_title) VALUES ('hi', 'hiii')")
    # print(sql.select_query("select * from activity"))
    print("FINITO")