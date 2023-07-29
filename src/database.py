from datetime import datetime
import logging
import pytz
import mysql.connector
from mysql.connector import Error
from margaret.settings import MYSQL_CONFIG


logger = logging.getLogger(__name__)


class DbQueries:

    @staticmethod
    def create_schema(name):
        return f'CREATE SCHEMA {name}'

    @staticmethod
    def use_schema(name):
        return f'USE {name}'

    @staticmethod
    def create_user_table():
        query = '''
        CREATE TABLE User (
            id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            member_id VARCHAR(600) UNIQUE NOT NULL,
            name VARCHAR(600) NOT NULL,
            challenges_finished INT DEFAULT 0,
            score INT DEFAULT 0,
            last_update DATETIME DEFAULT NULL
        )
        '''
        return query

    @staticmethod
    def insert_user(member_id, name):
        return f"INSERT INTO User (member_id, name) VALUES ('{member_id}', '{name}')"

    @staticmethod
    def select_user(where=None):
        if not where:
            return 'SELECT * FROM User'

        column, value = where.get('column'), where.get('value')
        operator = where.get('operator')
        condition = f'{column} {operator} {value}'

        return f'SELECT * FROM User WHERE {condition}'

    @staticmethod
    def update_user_score(member_id, score):
        query = f'UPDATE User SET score = score + {score} WHERE member_id = {member_id}'
        return query

    @staticmethod
    def update_user_challenges(member_id):
        query = f'UPDATE User SET challenges_finished = challenges_finished + 1 WHERE member_id = {member_id}'
        return query

    @staticmethod
    def update_user_last_update(member_id):
        now = datetime.now().astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S')
        query = f'UPDATE User SET last_update = {now} WHERE member_id = {member_id}'
        return query


def db_connection(
    host_name=MYSQL_CONFIG['MYSQL_HOST'],
    user_name=MYSQL_CONFIG['MYSQL_USER'],
    user_password=MYSQL_CONFIG['MYSQL_PASSWORD'],
    port=MYSQL_CONFIG['MYSQL_PORT']):
    """
    Connects with database.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            port=port
        )
    except Error as err:
        logger.error('Error: %s', str(err))

    return connection


def create_db_connection(
    host_name=MYSQL_CONFIG['MYSQL_HOST'],
    user_name=MYSQL_CONFIG['MYSQL_USER'],
    user_password=MYSQL_CONFIG['MYSQL_PASSWORD'],
    db_name=MYSQL_CONFIG['MYSQL_DATABASE'],
    port=MYSQL_CONFIG['MYSQL_PORT']):
    """
    Connects with database.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            port=port
        )
    except Error as err:
        logger.error('Error: %s', str(err))

    return connection


def create_database(connection, query):
    """
    Create a new schema;
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except Error as err:
        logger.error('Error: %s', str(err))


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as err:
        logger.error('Error: %s', str(err))


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        logger.error('Error: %s', str(err))


def init_db():
    """
    Initial migration script;
    Creates the schema and tables.
    *Run this function only in the first execution of the system*
    """
    con = db_connection()

    # Creates main schema and tables
    script = (
        DbQueries.create_schema(MYSQL_CONFIG['MYSQL_DATABASE']),
        DbQueries.use_schema(MYSQL_CONFIG['MYSQL_DATABASE']),
        DbQueries.create_user_table(),
    )
    for statement in script:
        execute_query(con, statement)
    logger.info('Database and tables created!')
    logging.info('Migration finished.')
