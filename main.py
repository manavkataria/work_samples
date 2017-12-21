#!/usr/bin/env python
"""
    Main entrypoint for LoanFacilitiesServer with data-driven configuration.

    Executes the following steps:
        1. Creates Loan Facilities Sever
        2. Runs Loan Stream Processor (main loop)
        3. Generates Facilities Yield Report

    NOTE: This is the only file that contains configuration settings (global variables).
    Ideally, this configuration should be an independent file -or- imported from a database.
"""

from loan_facilities_server import LoanFacilitiesServer

DIR_PATH = 'large/'
BANKS_CSV_PATH = DIR_PATH + 'banks.csv'
COVENANTS_CSV_PATH = DIR_PATH + 'covenants.csv'
FACILITIES_CSV_PATH = DIR_PATH + 'facilities.csv'
LOANS_CSV_PATH = DIR_PATH + 'loans.csv'

ASSIGNMENT_CSV_PATH = DIR_PATH + 'assignment.csv'
YIELDS_CSV_PATH = DIR_PATH + 'yields.csv'


def main():
    # Load and Parse Facilities, Covenants and Loans
    loan_server = LoanFacilitiesServer(FACILITIES_CSV_PATH, COVENANTS_CSV_PATH, LOANS_CSV_PATH)

    # Process Loans Stream
    loan_server.process_loans_stream(ASSIGNMENT_CSV_PATH)

    # Print Facility Yield Report
    loan_server.generate_facility_yield_report(YIELDS_CSV_PATH)


if __name__ == '__main__':
    main()
