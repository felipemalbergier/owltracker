class DatabaseBase:
    def __init__(self) -> None:
        raise NotImplementedError

    def select_query(self, query):
        raise NotImplementedError

    def insert_query(self, query):
        raise NotImplementedError

    def excecute_script(self, script):
        raise NotImplementedError

    def add_activity(self, **kwargs):
        raise NotImplementedError

    def excecute_query(self, query):
        return self.select_query(query)

    def excecute_query_format(self, query, values):
        return self.insert_query_format(query, values)
