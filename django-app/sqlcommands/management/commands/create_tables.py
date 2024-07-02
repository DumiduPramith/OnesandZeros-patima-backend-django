from django.core.management.base import BaseCommand
from sqlcommands.management.commands.user_table import UserTable


class Command(BaseCommand, UserTable):
    help = 'Create tables using raw SQL queries'

    def __image_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS image (
                image_id INT AUTO_INCREMENT PRIMARY KEY,
                input_image_path VARCHAR(255),
                predicted_image_path VARCHAR(255),
                uploader_id INT NOT NULL,
                FOREIGN KEY (uploader_id) REFERENCES user(user_id) ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.execute_query(sql)

    def __feedback_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS feedback (
                feedback_id INT AUTO_INCREMENT PRIMARY KEY,
                text TEXT,
                rating INT,
                archeologist_user_id INT NOT NULL,
                image_id INT NOT NULL,
                FOREIGN KEY (image_id) REFERENCES image(image_id) ON DELETE CASCADE,
                FOREIGN KEY (archeologist_user_id) REFERENCES archeologist(user_id) ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.execute_query(sql)

    def __image_tags_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS image_tags (
            tag_id INT AUTO_INCREMENT,
                image_id INT NOT NULL,
                tag_name VARCHAR(255),
                PRIMARY KEY (tag_id,image_id),
                FOREIGN KEY (image_id) REFERENCES image(image_id) ON DELETE CASCADE
            )
        '''
        self.execute_query(sql)

    def __admin_messages_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS admin_messages (
                message_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50),
                message_text TEXT,
                email VARCHAR(255),
                check_status BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.execute_query(sql)

    def __create_tables(self):
        self.__image_table()
        self.__feedback_table()
        self.__image_tags_table()
        self.__admin_messages_table()

    def handle(self, *args, **kwargs):
        self.execute_user_tables()
        self.__create_tables()
