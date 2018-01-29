#!/usr/bin/env python
"""
    Main entrypoint for PostfixParser with data-driven configuration.

    Executes the following steps:
        1. Load Input: Parse Input Spreadsheet
        2. Process: Evaluates Postfix Expressions
        3. Report: Generates Evaluation Report

    NOTE: This is the only file that contains configuration settings (global variables).
    Ideally, this configuration should be an independent file -or- imported from a database.
"""

from postfix_parser import PostfixParser

DIR_PATH = './'
INPUT_CSV_PATH = DIR_PATH + 'input.csv'
OUTPUT_CSV_PATH = DIR_PATH + 'output.csv'


def main():
    # TODO(Future): Implement overwriting default configuration with using command line arguments
    # see `argparse`: https://docs.python.org/2/library/argparse.html

    # Input: Load and Parse spreadsheet
    parser = PostfixParser(INPUT_CSV_PATH)

    # Evaluate: Postfix Expressions
    parser.evaluate()

    # Report: Produce Output Spreadsheet
    parser.generate_report(OUTPUT_CSV_PATH)


if __name__ == '__main__':
    main()
