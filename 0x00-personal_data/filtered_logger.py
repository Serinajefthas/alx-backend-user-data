#!/usr/bin/env python3
"""module to return encrypted log msg"""
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns manipulated log msg passed to it using regex"""
    for field in fields:
        msg = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', msg)
    return msg


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """returns filtered values from log records"""
        formatted_msg = super().format(record)
        for field in self.fields
            formatted_msg = self.filter_datum(field, formatted_msg)
        return formatted_msg
