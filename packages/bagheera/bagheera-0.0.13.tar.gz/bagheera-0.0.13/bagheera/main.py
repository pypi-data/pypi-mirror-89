"""
Main module used as entry point for the console executable "bagheera".

TODO: This is not true, fix.
"""
import os
from bagheera.parser.parser import parser
import pyparsing

def parse(file):
    """
    Entry point for the parser.

    :param file:
    :return:
    """
    try:
        return parser(file).parseFile(file, parseAll=True)
    except pyparsing.ParseException as e:
        print(e.line)
        print(" " * (e.column - 1) + "^")
        print(e)
        raise e