import sqlite3


DB_NAME = 'CryptoChat.db'


class DatabaseHandler:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name: str, columns: dict):
        # Create a table if not exists
        columns_str = ', '.join([f'{col} {col_type}' for col, col_type in columns.items()])
        query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                {columns_str}
            )
        '''
        self.cursor.execute(query)
        self.conn.commit()
        # Check if the table was created
        result = self.query_data('sqlite_master', ['name'], f"type='table' AND name='{table_name}'")
        if result is not None and result[0] == table_name:
            print(f"Table {table_name} created ..")
            return True
        else:
            print(f"Failed to create table {table_name}.")
            return False

    def insert_data(self, table_name: str, data: dict):
        # Insert data into a table
        placeholders = ', '.join(['?' for _ in data])
        query = f'''
            INSERT INTO {table_name} ({', '.join(data.keys())})
            VALUES ({placeholders})
        '''
        self.cursor.execute(query, tuple(data.values()))
        self.conn.commit()
        if self.cursor.rowcount != 0:
            # print(f"Inserted {self.cursor.rowcount} rows into {table_name} 📥")
            return True
        else:
            # print(f"No rows inserted into {table_name} !")
            return False

    def insert_user(self, username: str, public_key: str, host: str, public_ip: str, city: str, region: str, loc: str, timestamp: str):
        # Insert an user
        if self.query_data('Users', ['username', 'public_key', 'loc'], f"username='{username}' AND public_key='{public_key}' AND loc='{loc}'") is None:
            self.insert_data('Users', {
                'username': username,
                'public_key': public_key,
                'host': host,
                'public_ip': public_ip,
                'city': city,
                'region': region,
                'loc': loc,
                'timestamp': timestamp
            })
            # print(f"User ({username}) added to database !")
            return True
        else:
            # print(f"User ({username}) already exists !")
            return False

    def insert_conversation(self, sender: str, receiver: str, message: str, timestamp: str):
        # Insert a conversation
        self.insert_data('Conversations', {
            'sender': sender,
            'receiver': receiver,
            'message': message,
            'timestamp': timestamp
        })

    def remove_data(self, table_name: str, condition: str = None):
        # Remove data from a table based on a condition or not
        query = f'''
            DELETE FROM {table_name}
        '''
        if condition:
            query += f' WHERE {condition}'
        self.cursor.execute(query)
        self.conn.commit()
        if self.cursor.rowcount != 0:
            # print(f"Deleted {self.cursor.rowcount} rows from {table_name} 🧹")
            return True
        else:
            # print(f"No rows deleted from {table_name} !")
            return False

    def remove_user(self, username: str):
        # Remove an user
        self.remove_data('Users', f"username='{username}'")

    def update_data(self, table_name: str, data: str, condition: str = None):
        # Update data in the table based on a condition or not
        query = f'''
            UPDATE {table_name}
            SET {data}
        '''
        if condition:
            query += f' WHERE {condition}'
        self.cursor.execute(query)
        self.conn.commit()
        if self.cursor.rowcount != 0:
            # print(f"Updated {self.cursor.rowcount} rows from {table_name} 🔄")
            return True
        else:
            # print(f"No rows updated from {table_name} !")
            return False

    def query_data(self, table_name: str, columns: list, condition: str = None):
        # Query data from a table
        columns_str = ', '.join(columns)
        query = f'''
            SELECT {columns_str}
            FROM {table_name}
        '''
        if condition:
            query += f' WHERE {condition}'
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        all_results = self.cursor.fetchall()
        if result is None:
            # print(f"\n\nNo rows found in {table_name} !")
            return None
        elif len(columns) == 1 and columns[0] != '*':
            return result
        else:
            return all_results


if __name__ == '__main__':

    DB = DatabaseHandler(DB_NAME)
    DB.create_table('Users', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'username': 'TEXT',
        'public_key': 'TEXT',
        'host': 'TEXT',
        'public_ip': 'TEXT',
        'city': 'TEXT',
        'region': 'TEXT',
        'loc': 'TEXT',
        'timestamp': 'DATETIME'
    })
    DB.create_table('Conversations', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'sender': 'TEXT',
        'receiver': 'TEXT',
        'message': 'TEXT',
        'timestamp': 'DATETIME'
    })
