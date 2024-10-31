import sqlite3
import pymongo

class DatabaseManager:
    def __init__(self, db_type="sqlite", config=None):
        self.db_type = db_type
        self.config = config
        self.connection = None
        self.setup_connection()

    def setup_connection(self):
        """Sets up the database connection based on the type (SQL/NoSQL)."""
        if self.db_type == "sqlite":
            self.connection = sqlite3.connect(self.config["sqlite"]["db_path"])
        elif self.db_type == "mongodb":
            client = pymongo.MongoClient(self.config["mongodb"]["uri"])
            self.connection = client[self.config["mongodb"]["db_name"]]
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")

    def execute_sql(self, query, params=None):
        """Executes an SQL query."""
        if self.db_type != "sqlite":
            raise ValueError("SQL queries are only supported for SQLite databases.")
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        self.connection.commit()
        return cursor.fetchall()

    def insert_mongodb(self, collection, data):
        """Inserts data into a MongoDB collection."""
        if self.db_type != "mongodb":
            raise ValueError("MongoDB operations are only supported for MongoDB databases.")
        return self.connection[collection].insert_one(data)

if __name__ == "__main__":
    config = {
        "sqlite": {"db_path": "data/mydatabase.db"},
        "mongodb": {"uri": "mongodb://localhost:27017", "db_name": "vuln_scanner"}
    }
    db_manager = DatabaseManager(db_type="sqlite", config=config)
    db_manager.execute_sql("CREATE TABLE IF NOT EXISTS vulnerabilities (id INTEGER PRIMARY KEY, name TEXT, severity TEXT)")
