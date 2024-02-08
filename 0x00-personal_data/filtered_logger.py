#!/usr/bin/env python3
"""module to return encrypted log msg"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns manipulated log msg passed to it using regex"""
    return re.sub(fr'(?<=^|{separator})({"|".join(fields)})(?={separator}|$)',
                  redaction, message)
