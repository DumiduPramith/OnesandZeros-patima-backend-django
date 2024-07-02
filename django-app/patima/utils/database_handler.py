from django.db import connection

class DatabaseHandler:
    @staticmethod
    def run_select_query(query, params=None):
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

    @staticmethod
    def run_insert_query(query, params=None):
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.lastrowid  # returns the ID of the last inserted row

    @staticmethod
    def run_update_query(query, params=None):
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount  # returns the number of rows affected

    @staticmethod
    def run_delete_query(query, params=None):
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount  # returns the number of rows deleted
