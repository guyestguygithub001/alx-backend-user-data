#!/usr/bin/env python3

"""
This module provides functionality for filtering and redacting sensitive
personal information (PII) from log messages. It uses regular expressions
and a custom formatter to redact fields like names, email addresses, phone
numbers, social security numbers, and passwords. Additionally, it includes
utility functions for creating a logger and connecting to a MySQL database.
"""

import re
import os
import logging
import mysql.connector
from typing import List

patterns = {
    'extract': lambda x, y: r'(?P<field>{})=\[^{}\]\*'.format('|'.join(x), y),
    'replace': lambda x: r'\\g<field>={}'.format(x),
}

PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Redacts the specified fields in the given message using regular expressions.

    Args:
        fields (List[str]): A list of field names to redact.
        redaction (str): The string to replace the field values with.
        message (str): The message string to be redacted.
        separator (str): The separator character used in the message.

    Returns:
        str: The redacted message string.
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)

def get_logger() -> logging.Logger:
    """
    Creates and configures a logger for user data logging.

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Creates a connection to a MySQL database using environment variables.

    Returns:
        mysql.connector.connection.MySQLConnection: The database connection object.
    """
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")

    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection

def main():
    """
    Logs the information about user records in a table with sensitive data redacted.
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)

    info_logger = get_logger()
    connection = get_db()

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)

class RedactingFormatter(logging.Formatter):
    """
    A custom formatter class that redacts specified fields in log messages.

    Attributes:
        REDACTION (str): The string used to replace the redacted field values.
        FORMAT (str): The format string for the log message output.
        FORMAT_FIELDS (tuple): The fields used in the log message format.
        SEPARATOR (str): The separator character used in the log message.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes the RedactingFormatter with the specified fields to redact.

        Args:
            fields (List[str]): A list of field names to redact.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record by redacting the specified fields in the message.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message with redacted fields.
        """
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt

if __name__ == "__main__":
    main()
