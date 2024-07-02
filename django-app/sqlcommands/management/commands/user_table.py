from sqlcommands.management.helper.query_helper import QueryHelper


class UserTable(QueryHelper):
    def __user_table(self):
        query = """CREATE TABLE IF NOT EXISTS `user` (
               user_id INT AUTO_INCREMENT PRIMARY KEY,
               email VARCHAR(255) UNIQUE NOT NULL,
               fname VARCHAR(255),
               lname VARCHAR(255),
               profile_picture VARCHAR(255) DEFAULT '/static/profile_pictures/default.png',
               is_admin BOOLEAN DEFAULT FALSE,
               password VARCHAR(255),
               activation_status BOOLEAN DEFAULT 0,
               admin_id INT,
               FOREIGN KEY (admin_id) REFERENCES `user`(user_id)
               );"""
        self.execute_query(query)

    def __general_public_table(self):
        query = """
               CREATE TABLE IF NOT EXISTS general_public (
               user_id INT PRIMARY KEY,
               FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
           );"""
        self.execute_query(query)

    def __archeologist_table(self):
        query = """
               CREATE TABLE IF NOT EXISTS archeologist (
               user_id INT PRIMARY KEY,
               archeologist_id INT NOT NULL ,
               FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
           );"""
        self.execute_query(query)

    def execute_user_tables(self):
        self.__user_table()
        self.__archeologist_table()
        self.__general_public_table()
