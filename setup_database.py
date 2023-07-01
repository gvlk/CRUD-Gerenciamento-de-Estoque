def setup_database() -> None:
    from mysql.connector import connect

    connection = connect(
        host="127.0.0.1",
        user="spi",
        password="spi",
        port="3306",
        database="crud_spi"
    )
    cursor = connection.cursor()
    cursor.execute("DROP DATABASE IF EXISTS crud_spi;")
    cursor.execute("CREATE DATABASE crud_spi;")
    cursor.execute("USE crud_spi;")

    with open('setup_database.sql', 'r') as sql_file:
        sql_statements = sql_file.read().split(';')

        for statement in sql_statements:
            if statement.strip():
                cursor.execute(statement)

    connection.commit()
    cursor.close()
    connection.close()
