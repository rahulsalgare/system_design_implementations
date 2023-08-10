import psycopg2
import threading


class Connection:
    def __init__(self, connection):
        self.connection = psycopg2.connect(user=connection.get('username'),
                                      host=connection.get('host'),
                                      dbname=connection.get('dbname'))
        self.lock = threading.Lock()


class ConnectionPool:
    def __init__(self, connection: dict, pool_size: int=5):
        self.pool: list[Connection] = []
        self.pool_size: int = pool_size
        self.connection: dict = connection

    def get_connection(self):
        for con in self.pool:
            if not con.lock.locked():
                con.lock.acquire()
                return con.connection

        if (len(self.pool) == 0) or (len(self.pool) < self.pool_size):
            conn = Connection(self.connection)
            self.pool.append(conn)
            conn.lock.acquire()
            return conn.connection

    def close_connection(self, connection_to_close):
        for con in self.pool:
            if con.connection == connection_to_close:
                con.lock.release()
