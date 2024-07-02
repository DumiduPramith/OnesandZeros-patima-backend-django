from django.core.management.base import BaseCommand
from sqlcommands.management.helper.query_helper import QueryHelper
from django.db import transaction
from django.contrib.auth.hashers import make_password


class Command(BaseCommand, QueryHelper):
    help = 'Create Initial User using raw SQL queries'

    def __archeologist_user(self, fname, email, is_admin, password, activation_status, archeologist_id):
        try:
            with transaction.atomic():
                query = """
                                       INSERT INTO `user` (fname,email,is_admin,password, activation_status)
                                       VALUES (%s, %s, %s, %s, %s);
                                       """
                last_row = self.execute_query(query, (fname, email, is_admin, make_password(password), activation_status))

                query2 = """
                           INSERT INTO `archeologist` (user_id, archeologist_id)
                           VALUES (%s, %s);
                           """
                self.execute_query(query2, (last_row, archeologist_id))
        except Exception as e:
            print(e)

    def __general_user(self, fname, email, is_admin, password, activation_status):
        try:
            with transaction.atomic():
                query = """
                       INSERT INTO `user` (fname,email,is_admin,password, activation_status)
                       VALUES (%s, %s, %s, %s, %s);
                       """
                last_row = self.execute_query(query, (fname, email, is_admin, make_password(password), activation_status))
                query2 = """
                        INSERT INTO `general_public` (user_id)
                        VALUES (%s);
                        """
                self.execute_query(query2, (last_row,))
        except Exception as e:
            print(e)
    def __predictions(self,input_image_path, predicted_image_path, uploader_id, tags):
        try:
            with transaction.atomic():
                query = """
                INSERT INTO `image` (input_image_path, predicted_image_path, uploader_id)
                VALUES (%s, %s, %s);        
                """
                last_row = self.execute_query(query, (input_image_path, predicted_image_path, uploader_id))

                query2 = """
                INSERT INTO image_tags (image_id, tag_name)
                VALUES (%s, CONCAT(%s, ',',%s))
                """
                self.execute_query(query2, (last_row, tags[0], tags[1]))

        except Exception as e:
            print(e)

    def __feedbacks(self, text, rating, archeologist_user_id, image_id):
        query = """
        INSERT INTO `feedback` (text, rating, archeologist_user_id, image_id)
        VALUES (%s, %s, %s, %s);
        """
        self.execute_query(query, (text, rating, archeologist_user_id, image_id))

    def __messages(self, name, message, email):
        query = """
        INSERT INTO `admin_messages` (name, message_text, email)
        VALUES (%s, %s, %s);
        """
        self.execute_query(query, (name, message, email))

    def __run(self):
        self.__archeologist_user('admin','admin@gmail.com',1,'password',1,100)
        self.__archeologist_user('dumidu', 'dumidu42@gmail.com', 1, 'password', 1, 100)

        self.__general_user("Keerthi","keerthi@gmail.com",0,"password",1)
        self.__general_user("Nimal","nimal@gmail.com",0,"password",1)

        self.__predictions('/static/raw_images/2/1_.png', '/static/predicted_images/2/1.png', 2,[7.709196615935131, 80.13946607839371])
        self.__predictions('/static/raw_images/2/2_.png', '/static/predicted_images/2/2.png', 2,[7.709196615935131, 80.13946607839371])
        self.__predictions('/static/raw_images/2/3_.png', '/static/predicted_images/2/3.png', 2,[7.709196615935131, 80.13946607839371])

        self.__predictions('/static/raw_images/2/1_.png', '/static/predicted_images/2/1.png', 1,[7.709196615935131, 80.13946607839371])

        self.__feedbacks('Very well|Somewhat realistic|Somewhat satisfied|good', 5, 2, 1)
        self.__feedbacks('Somewhat well|Not very realistic|Not very satisfied|ok', 3, 2, 1)
        self.__feedbacks('Somewhat well|Not very realistic|Not very satisfied|ok', 4, 2, 2)

        self.__messages('Dumidu', 'When uploading the file, I get a "File too large" error.', 'dumidu@gmail.com')

        self.__messages('Alice', 'I cannot log into my account even though I am sure my credentials are correct.',
                    'alice@example.com')
        self.__messages('John', 'The app crashes whenever I try to open the settings menu.', 'john@example.com')

        self.__messages('Emma', 'I am getting a "Payment failed" error when trying to purchase a subscription.',
                        'emma@example.com')

        self.__messages('Michael', 'Can you add a dark mode option to the app? It would be very helpful.',
                        'michael@example.com')
        self.__messages('Sophia', 'My data is not syncing across devices, and I keep losing my progress.',
                        'sophia@example.com')
        self.__messages('David', 'I am not receiving any notifications even though they are enabled in the settings.',
                        'david@example.com')
        self.__messages('Liam', 'How can I reset my password? I cannot find the option in the app.', 'liam@example.com')

    def handle(self, *args, **kwargs):
        self.__run()
