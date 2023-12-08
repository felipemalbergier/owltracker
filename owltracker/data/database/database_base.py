class DatabaseBase:
    def __init__(self) -> None:
        raise NotImplementedError

    def insert_query(self, query):
        raise NotImplementedError

    def excecute_script(self, *args, **kwargs):
        raise NotImplementedError

    def add_activity(self, **kwargs):
        raise NotImplementedError

    def excecute_query(self, query, values, commit=False):
        raise NotImplementedError