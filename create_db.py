import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    """Create a database connection"""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    
    return connection

def create_database(connection, db_name):
    """Create a database"""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE {db_name};")
        print(f"Database '{db_name}' created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def create_table(connection):
    """Create a table"""
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Job (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        company VARCHAR(255) NOT NULL,
        link VARCHAR(255) NOT NULL,
        experience VARCHAR(100) NOT NULL,
        salary VARCHAR(100) NOT NULL,
        location VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        post_date VARCHAR(100) NOT NULL,
        image_link VARCHAR(255) ,
        date_of_post DATE NOT NULL
    );
    """
    try:
        cursor.execute(create_table_query)
        print("Table 'Job' created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def main():
    # Database credentials
    host_name = "127.0.0.1"  
    user_name = "root"  
    user_password = ""  
    db_name = "placement_portal"  

    # Create a connection to the MySQL server
    connection = create_connection(host_name, user_name, user_password, db_name)

    # Create the database
    create_database(connection, db_name)

    # Connect to the newly created database
    connection.database = db_name

    # Create the Job table
    create_table(connection)

    # Close the connection
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

if __name__ == "__main__":
    main()
