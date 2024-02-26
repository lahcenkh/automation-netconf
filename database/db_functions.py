import sqlite3

DATABASE_PATH = "database/database.db"

def get_db_info(query):
    try:
        connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
            # Create a cursor
        cursor = connection.cursor()
        # Execute a SELECT statement
        cursor.execute(query)
        # Fetch the data
        results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        result_dicts = [dict(zip(columns, row)) for row in results]
        # Close the connection
        connection.close()
        return result_dicts
        
    except Exception as e:
        print(f"Error Happened:\n{e}")
        connection.close()
        return "Error"
    

def edit_post_db(query):
    try:
        connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        # Create a cursor object
        cursor = connection.cursor()
        # Insert data into the table
        cursor.execute(query)
        # Commit the changes
        connection.commit()
        # Close the connection
        connection.close()
        return "updated"
    except Exception as e:
        print(f"Error Happened:\n {e}")
        connection.close()
        return "Error!"

def delete_post_db(query):
    try:
        connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        # Create a cursor object
        cursor = connection.cursor()
        # Insert data into the table
        cursor.execute(query)
        # Commit the changes
        connection.commit()
        # Close the connection
        connection.close()
        return "deleted"
    except Exception as e:
        print(f"Error Happened:\n {e}")
        connection.close()
        return "Error!"
    
def add_post_db(query):
    try:
        connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        # Create a cursor object
        cursor = connection.cursor()
        # Insert data into the table
        cursor.execute(query)
        # Commit the changes
        connection.commit()
        # Close the connection
        connection.close()
        return "added"
    except Exception as e:
        print(f"Error Happened:\n {e}")
        connection.close()
        return "Error!"