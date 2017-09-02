import psycopg2
import psycopg2.extras


CONNECTION_STR = "dbname = 'bans' user = 'bans' host='localhost' password = 'pass'"


def select_query(sql_str, variables=None, connection_str=CONNECTION_STR):
    try:
        with psycopg2.connect(connection_str) as connection:
            with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql_str, variables)
                return cursor.fetchall()
    except psycopg2.DatabaseError as exception:
        print(exception)
