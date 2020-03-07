"""
    author: Zituo Yan
    description: create connection of database server and create new database.
    date: 21/02/2020
"""
import sqlite3
import configparser

config = configparser.ConfigParser()
config.read("./db_cnf.txt")
path = config.get("SQLite", "path")


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=MetaSingleton):
    """
        create sqlite connection
    """
    connection = None
    cursor = None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(path)
            self.cursor = self.connection.cursor()
        return self.cursor
