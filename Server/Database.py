import sqlite3


DB_NAME = 'CyberChat.db'


class DatabaseHandler:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        # Create a table if not exists
        columns_str = ', '.join([f'{col} {col_type}' for col, col_type in columns.items()])
        query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                {columns_str}
            )
        '''
        self.cursor.execute(query)
        self.conn.commit()
        if self.cursor.rowcount != 0:
            return
        print(f"Table {table_name} created ..")

    def insert_data(self, table_name, data):
        # Insert data into a table
        placeholders = ', '.join(['?' for _ in data])
        query = f'''
            INSERT INTO {table_name} ({', '.join(data.keys())})
            VALUES ({placeholders})
        '''
        self.cursor.execute(query, tuple(data.values()))
        self.conn.commit()
        if self.cursor.rowcount != 0:
            print(f"Inserted {self.cursor.rowcount} rows into {table_name} 📥")
        else:
            print(f"No rows inserted into {table_name} 🚫")
    
    def insert_user(self, username, public_key, host, public_ip, mac, city, region, loc, timestamp):
        # Create an user
        self.insert_data('Users', {
            'username': username,
            'public_key': public_key,
            'host': host,
            'public_ip': public_ip,
            'MAC': mac,
            'city': city,
            'region': region,
            'loc': loc,
            'timestamp': timestamp
        })

    def remove_data(self, table_name, condition=None):
        # Remove data from a table based on a condition or not
        query = f'''
            DELETE FROM {table_name}
        '''
        if condition:
            query += f' WHERE {condition}'
        self.cursor.execute(query)
        self.conn.commit()
        if self.cursor.rowcount != 0:
            print(f"Deleted {self.cursor.rowcount} rows from {table_name} 🧹")
        else:
            print(f"No rows deleted from {table_name} 🚫")

    def remove_user(self, username):
        # Remove an user
        self.remove_data('Users', f"username='{username}'")

    def update_data(self, table_name, data, condition=None):
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
            print(f"Updated {self.cursor.rowcount} rows from {table_name} 🔄")
        else:
            print(f"No rows updated from {table_name} 🚫")

    def query_data(self, table_name, columns, condition=None):
        # Query data from a table
        columns_str = ', '.join(columns)
        query = f'''
            SELECT {columns_str}
            FROM {table_name}
        '''
        if condition:
            query += f' WHERE {condition}'
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            print(f"No rows found in {table_name} 🚫")
            return None
        if len(columns) == 1 and columns[0] != '*':
            return self.cursor.fetchone()[0]
        else:
            return self.cursor.fetchall()


DB = DatabaseHandler(DB_NAME)
DB.create_table('Users', {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'username': 'TEXT',
    'public_key': 'TEXT',
    'host': 'TEXT',
    'public_ip': 'TEXT',
    'MAC': 'TEXT',
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
    'hash256': 'TEXT',
    'signature': 'TEXT',
    'timestamp': 'DATETIME'
})
