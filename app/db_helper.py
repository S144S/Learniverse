import json
import sqlite3
from datetime import datetime

from flask_login import UserMixin


class UserManagement(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


class Users:
    def __init__(self, db: str) -> None:
        """
        The constructor of Users table class.

        :param db: Represents the name(or path) of the SQLite database
        :type db_file: str
        """
        self.__db = db

    def setup(self) -> None:
        """
        Creates the users table in database.
        """
        self.conn = sqlite3.connect(self.__db)
        cursor = self.conn.cursor()
        # Create users table
        sql = """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        fname TEXT NOT NULL,
        lname TEXT NOT NULL,
        grade INTEGER NOT NULL DEFAULT 7,
        register_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        last_login DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT 1,
        is_admin BOOLEAN DEFAULT 0
        )"""
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()

    def add_user(
            self,
            username: str,
            password: str,
            fname: str,
            lname: str,
            grade: int = 7,
            register_date=None,
            last_login=None,
            is_active: bool = True,
            is_admin: bool = False
    ) -> bool:
        """
        Inserts a new user into the database.

        :param username: The username of the user
        :type username: str
        :param password: User's password
        :type password: str
        :param fname: The first name of the user
        :type fname: str
        :param lname: The last name of the user
        :type lname: str
        :param grade: The grade of the user. defaults to 7
        :type grade: int (optional)
        :param register_date: The date and time when the user
        is registered (optional)
        :param last_login: The date and time of the
        user's last login (optional)
        :param is_active: Indicates whether the user
        is currently active or not. defaults to True
        :type is_active: bool (optional)
        :param is_admin: Indicates whether the user being added
        is an admin or not. defaults to False
        :type is_admin: bool (optional)
        :return: a boolean that includes
        the status of adding a new user to the database
        """
        if not register_date:
            register_date = datetime.now()
        if not last_login:
            last_login = datetime.now()

        sql = """INSERT OR IGNORE INTO users (
        username, password, fname, lname, grade, register_date,
        last_login, is_active, is_admin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        param = (
            username,
            password,
            fname,
            lname,
            grade,
            register_date,
            last_login,
            is_active,
            is_admin
        )
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            self.conn.commit()
            self.conn.close()
            print("User added successfully")
            return True
        except Exception as e:
            print(e)
            return False

    def update_user_info(
            self,
            id: int,
            username: str,
            fname: str,
            lname: str,
            grade: int,
    ) -> bool:
        """
        Update user parameters in the database based on user ID.

        :param id: The ID of the user to update
        :type id: int
        :param username: New username for the user
        :type username: str
        :param fname: New first name for the user
        :type fname: str
        :param lname: New last name for the user
        :type lname: str
        :param grade: New grade for the user
        :type grade: int
        :return: a boolean that includes
        the status of updating the new user's info.
        """
        sql = """UPDATE users SET
        username = ?, fname = ?,lname = ?, grade = ?
        WHERE id = ?
        """
        params = (username, fname, lname, grade, id)
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def update_user_password(self, id, password) -> bool:
        """
        Update user parameters in the database based on user ID.

        :param id: The ID of the user to update
        :type id: int
        :param password: New password for the user
        :type password: str
        :return: a boolean that includes
        the status of updating the user's password.
        """
        sql = "UPDATE users SET password = ? WHERE id = ?"
        params = (password, id)
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def update_user_last_login(self, id) -> bool:
        """
        Update a user last login date in the database based on user ID.

        :param id: The ID of the user to update
        :type id: int
        :return: a boolean that includes
        the status of updating the user's last login.
        """
        last_login = datetime.now()
        sql = "UPDATE users SET last_login = ? WHERE id = ?"
        params = (last_login, id)
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def get_user_id(self, username: str) -> int:
        """
        Get a user's id from db.

        :param username: The username of the user
        :type username: str
        :return: an integer that includes user's id.
        """
        sql = "SELECT id FROM users WHERE username = ?"
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (username,))
            row = cursor.fetchone()
            id = 0
            if row:
                id = row[0]
            self.conn.close()
            return id
        except Exception as e:
            print(e)
            return 0

    def get_user(self, id: int) -> dict:
        """
        Retrieves a user from a SQLite database based on their ID.

        :param id: Represents the unique identifier of a user
        :type id: int
        :return: user object.
        """
        sql = "SELECT * FROM users WHERE id = ?"
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            user = {}
            if row:
                column_names = [desc[0] for desc in cursor.description]
                user = dict(zip(column_names, row))
            self.conn.close()
            return user
        except Exception as e:
            print(e)
            return {}


class Planets:
    def __init__(self, db: str) -> None:
        self.__db = db

    def setup(self) -> None:
        """
        Creates the planets table in database.
        """
        self.conn = sqlite3.connect(self.__db)
        cursor = self.conn.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS planets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            video TEXT,
            avatar TEXT,
            image TEXT,
            desc TEXT
        )'''
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()

    def add_planet(self, name: str, video: str = '', avatar: str = '', image: str = '', desc: str = '') -> bool:
        """
        Adds a new planet to the database.

        :param name: Name of the planet
        :param video: URL or path to video
        :param avatar: Avatar image path
        :param image: Main image path
        :param desc: Description of the planet
        :return: True if added successfully, else False
        """
        sql = '''INSERT INTO planets (name, video, avatar, image, desc) VALUES (?, ?, ?, ?, ?)'''
        params = (name, video, avatar, image, desc)
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def get_all_planets(self) -> list[dict]:
        """
        Fetches all planets from the database.

        :return: List of planet dictionaries
        """
        sql = "SELECT * FROM planets"
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            self.conn.close()
            return [dict(zip(column_names, row)) for row in rows]
        except Exception as e:
            print(e)
            return []

    def get_all_planets_basic_info(self) -> list[dict]:
        """
        Fetches all planets basic info from the database.

        :return: List of planet dictionaries
        """
        sql = "SELECT name, avatar FROM planets"
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            self.conn.close()
            return [dict(zip(column_names, row)) for row in rows]
        except Exception as e:
            print(e)
            return []

    def get_planet_by_id(self, id: int) -> dict:
        """
        Retrieves a planet's information based on its id.

        :param id: id of the planet
        :return: Dictionary with planet details or empty dict if not found
        """
        sql = "SELECT * FROM planets WHERE id = ?"
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            self.conn.close()
            if row:
                column_names = [desc[0] for desc in cursor.description]
                return dict(zip(column_names, row))
            return {}
        except Exception as e:
            print(e)
            return {}

    def get_planet_by_name(self, name: str) -> dict:
        """
        Retrieves a planet's information based on its name.

        :param name: Name of the planet
        :return: Dictionary with planet details or empty dict if not found
        """
        sql = "SELECT * FROM planets WHERE name = ?"
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (name,))
            row = cursor.fetchone()
            self.conn.close()
            if row:
                column_names = [desc[0] for desc in cursor.description]
                return dict(zip(column_names, row))
            return {}
        except Exception as e:
            print(e)
            return {}


class UserState:
    def __init__(self, db: str) -> None:
        self.__db = db

    def setup(self) -> None:
        """
        Creates the user_state table in the database.
        """
        self.conn = sqlite3.connect(self.__db)
        cursor = self.conn.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS user_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            planet_id INTEGER NOT NULL,
            is_solve_puzzle BOOLEAN DEFAULT 0,
            is_solve_exam BOOLEAN DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(planet_id) REFERENCES planets(id)
        )'''
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()

    def add_user_state(self, user_id: int, planet_id: int = 1) -> bool:
        """
        Adds a new user state entry.

        :param user_id: User's ID
        :param planet_id: Planet's ID
        :return: True if successful
        """
        sql = '''INSERT INTO user_state (user_id, planet_id) VALUES (?, ?)'''
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (user_id, planet_id))
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def update_user_planet(self, user_id: int, planet_id: int) -> bool:
        """
        Updates the planet_id for a given user.

        :param user_id: User's ID
        :param planet_id: New planet ID
        :return: True if successful
        """
        sql = "UPDATE user_state SET planet_id = ? WHERE user_id = ?"
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (planet_id, user_id))
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def get_user_planet_id(self, user_id: int) -> int:
        """
        Retrieves the current planet ID of the user.

        :param user_id: User's ID
        :return: Planet ID or 0 if not found
        """
        sql = "SELECT planet_id FROM user_state WHERE user_id = ?"
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (user_id,))
            row = cursor.fetchone()
            self.conn.close()
            return row[0] if row else 0
        except Exception as e:
            print(e)
            return 0

    def get_user_solve_status(self, user_id: int) -> int:
        """
        Retrieves the current solve status of the user.

        :param user_id: User's ID
        :return: Solve status or 0 if not found
        """
        sql = "SELECT is_solve_puzzle, is_solve_exam FROM user_state WHERE user_id = ?"
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (user_id,))
            row = cursor.fetchone()
            self.conn.close()
            return row if row else (0, 0)
        except Exception as e:
            print(e)
            return (0, 0)

    def update_user_puzzle_solve_status(self, user_id: int, stat: bool) -> bool:
        """
        Updates the puzzle solve status for a given user.

        :param user_id: User's ID
        :param stat: New puzzle solve status
        :return: True if successful
        """
        sql = "UPDATE user_state SET is_solve_puzzle = ? WHERE user_id = ?"
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (stat, user_id))
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def update_user_exam_solve_status(self, user_id: int, stat: bool) -> bool:
        """
        Updates the exam solve status for a given user.

        :param user_id: User's ID
        :param stat: New exam solve status
        :return: True if successful
        """
        sql = "UPDATE user_state SET is_solve_exam = ? WHERE user_id = ?"
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (stat, user_id))
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            print(e)
            return False


class GiftContent:
    def __init__(self, db: str) -> None:
        self.__db = db

    def setup(self) -> None:
        """
        Creates the gift_content table in the database.
        """
        self.conn = sqlite3.connect(self.__db)
        cursor = self.conn.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS gift_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            planet_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY(planet_id) REFERENCES planets(id)
        )'''
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()

    def add_content(self, planet_id: int, content: str) -> bool:
        """
        Adds a new content entry for a specific planet.

        :param planet_id: ID of the planet
        :param content: Text content to be added
        :return: True if successful
        """
        sql = '''INSERT INTO gift_content (planet_id, content) VALUES (?, ?)'''
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (planet_id, content))
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def get_contents_by_planet(self, planet_id: int) -> list[str]:
        """
        Retrieves all content entries for a given planet.

        :param planet_id: ID of the planet
        :return: List of content strings
        """
        sql = "SELECT content FROM gift_content WHERE planet_id = ?"
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (planet_id,))
            rows = cursor.fetchall()
            self.conn.close()
            return [row[0] for row in rows] if rows else []
        except Exception as e:
            print(e)
            return []


class Exam:
    def __init__(self, db: str) -> None:
        self.__db = db

    def setup(self) -> None:
        """
        Creates the exam table in the database.
        """
        self.conn = sqlite3.connect(self.__db)
        cursor = self.conn.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS exam (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            planet_id INTEGER NOT NULL,
            q1 TEXT, q1_options TEXT, q1_right_answer INTEGER,
            q2 TEXT, q2_options TEXT, q2_right_answer INTEGER,
            q3 TEXT, q3_options TEXT, q3_right_answer INTEGER,
            q4 TEXT, q4_options TEXT, q4_right_answer INTEGER,
            q5 TEXT, q5_options TEXT, q5_right_answer INTEGER,
            q6 TEXT, q6_options TEXT, q6_right_answer INTEGER,
            q7 TEXT, q7_options TEXT, q7_right_answer INTEGER,
            q8 TEXT, q8_options TEXT, q8_right_answer INTEGER,
            q9 TEXT, q9_options TEXT, q9_right_answer INTEGER,
            q10 TEXT, q10_options TEXT, q10_right_answer INTEGER,
            FOREIGN KEY(planet_id) REFERENCES planets(id)
        )'''
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()

    def add_exam(self, planet_id: int, questions: list[dict], correct_answers: dict) -> bool:
        """
        Adds a full 10-question exam for a given planet.

        :param planet_id: ID of the planet
        :param questions: List of 10 dicts with keys: question, options
        :param correct_answers: Dict of question index to correct option index (1-based)
        :return: True if successful
        """
        if len(questions) != 10:
            raise ValueError("Exactly 10 questions are required.")

        sql = '''INSERT INTO exam (
            planet_id,
            q1, q1_options, q1_right_answer,
            q2, q2_options, q2_right_answer,
            q3, q3_options, q3_right_answer,
            q4, q4_options, q4_right_answer,
            q5, q5_options, q5_right_answer,
            q6, q6_options, q6_right_answer,
            q7, q7_options, q7_right_answer,
            q8, q8_options, q8_right_answer,
            q9, q9_options, q9_right_answer,
            q10, q10_options, q10_right_answer
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

        params = [planet_id]
        for i in range(10):
            q = questions[i]
            options_json = json.dumps(q['options'], ensure_ascii=False)
            params.extend([q['question'], options_json, correct_answers[f"q{i+1}"]])

        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def get_exam_questions(self, planet_id: int) -> list[dict]:
        sql = "SELECT * FROM exam WHERE planet_id = ?"
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (planet_id,))
            row = cursor.fetchone()
            self.conn.close()

            if not row:
                return []

            questions = []
            for i in range(1, 11):
                base = 2 + (i - 1) * 3
                question = row[base]
                try:
                    options = json.loads(row[base + 1]) if row[base + 1] else []
                except Exception as e:
                    print(f"Error parsing question {i}: {e}")
                    options = []
                questions.append({"question": question, "options": options})

            return questions
        except Exception as e:
            print("Error getting questions ->", e)
            return []

    def get_correct_answers(self, planet_id: int) -> dict:
        sql = "SELECT * FROM exam WHERE planet_id = ?"
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (planet_id,))
            row = cursor.fetchone()
            self.conn.close()

            if not row:
                return {}

            return {f"q{i}": row[2 + (i - 1) * 3 + 2] for i in range(1, 11)}
        except Exception as e:
            print("Error getting correct answers ->", e)
            return {}


class UserRocket:
    def __init__(self, db: str) -> None:
        self.__db = db

    def setup(self) -> None:
        """
        Creates the user_rocket table in the database.
        """
        self.conn = sqlite3.connect(self.__db)
        cursor = self.conn.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS user_rocket (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            money INTEGER DEFAULT 50,
            cold_trip BOOLEAN DEFAULT 0,
            atomic_fuel BOOLEAN DEFAULT 0,
            flying_motor BOOLEAN DEFAULT 0,
            titanium_body BOOLEAN DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )'''
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()

    def add_user_rocket(self, user_id: int) -> bool:
        """
        Adds a new rocket entry for a user.
        """
        sql = '''INSERT OR IGNORE INTO user_rocket (user_id) VALUES (?)'''
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (user_id,))
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def get_user_money(self, user_id: int) -> int:
        """
        Retrieves the current money of a user.
        """
        sql = "SELECT money FROM user_rocket WHERE user_id = ?"
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (user_id,))
            row = cursor.fetchone()
            self.conn.close()
            return row[0] if row else 0
        except Exception as e:
            print(e)
            return 0

    def update_user_money(self, user_id: int, new_money: int) -> bool:
        """
        Updates the money of a user.
        """
        sql = "UPDATE user_rocket SET money = ? WHERE user_id = ?"
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (new_money, user_id))
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def get_user_rocket_features(self, user_id: int) -> dict:
        """
        Returns a dictionary of all rocket features for the given user.
        """
        sql = '''SELECT cold_trip, atomic_fuel, flying_motor, titanium_body
                 FROM user_rocket WHERE user_id = ?'''
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (user_id,))
            row = cursor.fetchone()
            self.conn.close()
            if row:
                keys = ["cold_trip", "atomic_fuel", "flying_motor", "titanium_body"]
                return dict(zip(keys, row))
            return {}
        except Exception as e:
            print(e)
            return {}

    def update_rocket_feature(self, user_id: int, feature: str, value: bool) -> bool:
        """
        Updates a specific rocket feature for the user.

        :param user_id: ID of the user
        :param feature: Name of the feature to update (must be one of the valid columns)
        :param value: Boolean value (True/False)
        :return: True if successful
        """
        valid_features = ["cold_trip", "atomic_fuel", "flying_motor", "titanium_body"]
        if feature not in valid_features:
            print(f"Invalid feature: {feature}")
            return False

        sql = f"UPDATE user_rocket SET {feature} = ? WHERE user_id = ?"
        try:
            self.conn = sqlite3.connect(self.__db)
            cursor = self.conn.cursor()
            cursor.execute(sql, (int(value), user_id))
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            print(e)
            return False


class DBHelper:
    def __init__(self, db_file: str = "database.db") -> None:
        """
        The constructor of DataBase helper class.

        :param db_file: The `db_file` represents the name(or path)
        of the SQLite database
        :type db_file: str (optional)
        """
        self.db_file = db_file

        self.users = Users(self.db_file)
        self.planet = Planets(self.db_file)
        self.user_state = UserState(self.db_file)
        self.gift_content = GiftContent(self.db_file)
        self.exam = Exam(self.db_file)
        self.rocket = UserRocket(self.db_file)
        
    def create_tables(self):
        self.users.setup()
        self.planet.setup()
        self.user_state.setup()
        self.gift_content.setup()
        self.exam.setup()
        self.rocket.setup()
        print("Database and tables created successfully!")


if __name__ == "__main__":
    db_helper = DBHelper()
    db_helper.create_tables()