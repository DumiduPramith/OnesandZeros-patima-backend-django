from django.db import connection


class QueryHelper:
    def execute_query(self, query, params=None):
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            self.stdout.write(self.style.SUCCESS(f'Successfully executed: {query}'))
            return cursor.lastrowid
