from sqlite_database import SQLiteDatabase
FAt

def get_query_create_activity_table(drop_tables=False):

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

# need to create a task table
def get_query_create_task_table(drop_tables=False):
    query = """
    CREATE TABLE IF NOT EXISTS task (
        id INTEGER PRIMARY KEY,
        name TEXT,
        source INTEGER,
        ) ;
    
    """
    if drop_tables:
        query = "DROP TABLE IF EXISTS task;" + query

    return query

# create source table
def get_query_create_task_source_table(drop_tables=False):
    query = """
    CREATE TABLE IF NOT EXISTS task_source (
        id INTEGER PRIMARY KEY,
        name TEXT,
        ) ;
    
    """
    if drop_tables:
        query = "DROP TABLE IF EXISTS task_source;" + query

    return query

if __name__ == "__main__":
    query = get_query_create_activity_table()
    sql = SQLiteDatabase()
    sql.excecute_script(query)
    # sql.excecute_query("INSERT INTO activity (process_name, window_title) VALUES ('hi', 'hiii')", commit=True)
    # print(sql.select_query("select * from activity"))
    print("FINITO")