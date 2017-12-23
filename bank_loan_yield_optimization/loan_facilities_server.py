#!/usr/bin/env python

import pandas as pd
import utils

from facility import Facility
from loan_request import LoanRequest


class LoanFacilitiesServer(object):
    """
        LoanFacilitiesServer class with loan stream processing capability.

        NOTE: This class abstracts the input _format_ specific parsing. Input format is likely
        to change with time. Ideally, there should be dedicated classes for each input source
        isolating format specific parsing functionality.

        Idempotent Interfaces:
            LoanFacilitiesServer(): Constructor that loads & parses facilities, covenants and loans csv
            parse_facilities_and_covenants(): Parses facilities and covenants into a unified list
            parse_loan_request(): Parses loan requests into a convenient `LoanRequest` object

        Non-Idempotent Interfaces:
            process_loans_stream(): Processes loans for optimal yield facility assignment
            log_loan_assignment(): Logs loan assignment
            generate_facility_yield_report(): Generates facility yield report
    """

    def __init__(self, facilities_csv_path, covenants_csv_path, loans_csv_path):
        """
            Construtor for `LoanFacilitiesServer`.

            Performs the following steps:
                1. Loads facilities, covenants and loans csv into dataframes.
                2. Parses facilities and covenants into a unified list of `Facility` objects.
                3. Sorts `facilities_list` by `interest_rate` to optimize yield

            Arguments:
                facilities_csv_path (string)
                covenants_csv_path (string)
                loans_csv_path (string)

            Returns:
                `LoanFacilitiesServer` object

            Raises:
                OSError: if any of the input files are not accessible
        """

        # Load Facilities with its associated Covenats
        self.facilities_df = pd.read_csv(facilities_csv_path)
        self.covenants_df = pd.read_csv(covenants_csv_path)

        # Parse Facilities & Covenants
        self.facilities_list = self.parse_facilities_and_covenants()
        # Sort facility by `interest_rate` to optimize yield
        self.facilities_list.sort(key=lambda facility: facility.interest_rate)

        # Load Loans csvfile
        # NOTE: This will be processed a stream input
        self.loans_df = pd.read_csv(loans_csv_path)

    def parse_facilities_and_covenants(self, facilities_df=None, covenants_df=None):
        """
            Parses facilities and covenants into a unified list of `Facility` objects

            Arguments:
                facilities_df (dataframe) or None
                covenants_df (dataframe) or None

            Returns:
                facilities_list (list of Facility objects)

            Raises:
                AttributeError: if facilities_df or covenants_df are not valid dataframes
                TypeError: if facilities_df or covenants_df have invalid values

            Known Limitations:
                Input format specific parser.
        """
        # TODO(Future): Move this function to an input source specific class

        if facilities_df is None:
            facilities_df = self.facilities_df
        if covenants_df is None:
            covenants_df = self.covenants_df

        facilities_list = []
        for facility_metadata in facilities_df.itertuples():
            facility_covenants_df = covenants_df[covenants_df.facility_id == facility_metadata.id]

            max_default_likelihood = float(facility_covenants_df.max_default_likelihood.dropna())
            facility_id = int(facility_metadata.id)
            bank_id = int(facility_metadata.bank_id)
            amount = float(facility_metadata.amount)
            interest_rate = float(facility_metadata.interest_rate)
            banned_states = facility_covenants_df.banned_state.tolist()

            facilities_list.append(Facility(facility_id,
                                            bank_id,
                                            amount,
                                            interest_rate,
                                            max_default_likelihood,
                                            banned_states))
        return facilities_list

    def parse_loan_request(self, loan):
        """
            Parses a single loan request stream input entry into a convenient `LoanRequest` object.

            Arguments:
                loan (dataframe row)

            Returns:
                loan_request (LoanRequest object)

            Raises:
                AttributeError: if `loan` is not a valid dataframe row
                TypeError: if `loan` has an invalid value

            Known Limitations:
                Input format specific parser.
        """
        # TODO(Future): Move this function to an input source specific class

        loan_id = int(loan.id)
        amount = float(loan.amount)
        default_likelihood = float(loan.default_likelihood)
        interest_rate = float(loan.interest_rate)
        origin_state = str(loan.state)

        loan_request = LoanRequest(loan_id,
                                   amount,
                                   default_likelihood,
                                   interest_rate,
                                   origin_state)
        return loan_request

    def process_loans_stream(self, assignment_csv_path):
        """
            Processes a loan stream to find an optimal yield given a list of facilities
            while satisfying their covenants and constraints.

            For every loan in the stream, perform the following steps:
                1. Parse a single loan request
                2. Find an optimal valid loan assignment given `facilities_list`
                3. Issue Loan via a facility
                4. Log loan assignmnet

            NOTE: This is not an idempotent fuction as it issues side effects

            Arguments:
                assignment_csv_path (string)

            Returns:
                None

            Raises:
                OSError: if assignment_csv_path is not accessible
                AttributeError: if `loan` is not a valid dataframe row
                TypeError: if `loan` has an invalid value

            Side Effects:
                Writing to a file
        """
        # NOTE: On a large-scale high-performance production system this should be implemented
        # as a distributed system workers performing various streaming and batch reporting tasks

        for loan in self.loans_df.itertuples():
            # Parse a _single_ Loan Request
            loan_request = self.parse_loan_request(loan)
            # Iterate over facilities for loan assignments
            for facility in self.facilities_list:
                if facility.is_valid_assignment(loan_request):
                    # Issue Loan and compute corresponding expected yield
                    # NOTE: Return value `expected_yield` of `issue_loan` is unused here but could be used
                    # to feed into a real-time monitoring dashboard. Imagine a graph of:
                    #     (a) Overall Yield vs. Time, or
                    #     (b) Yield Per Facility vs. Time
                    facility.issue_loan(loan_request)

                    # Log Loan Assignment
                    self.log_loan_assignment(assignment_csv_path, loan_request.loan_id, facility.facility_id)

                    # Loan request satisfied
                    break

    @classmethod
    def log_loan_assignment(self, csv_filepath, loan_id, facility_id):
        """
            Consumes a generic stream writer to log a loan assignment

            NOTE: This is not an idempotent fuction as it issues side effects

            Arguments:
                csv_filepath (string)
                loan_id (integer)
                facility_id (integer)

            Returns:
                None

            Raises:
                OSError: if csv_filepath is not accessible

            Side Effects:
                Writing to a file
        """
        header = ['loan_id', 'facility_id']
        row_values = [loan_id, facility_id]
        utils.stream_writer(csv_filepath, header, row_values)

    def generate_facility_yield_report(self, csv_filepath, facilities_list=None):
        """
            Generates an overall yield report of all facilities

            NOTE: This is not an idempotent fuction as it issues side effects

            Arguments:
                csv_filepath (string)
                facilities_list (list of `Facility` objects)

            Returns:
                None

            Raises:
                OSError: if csv_filepath is not accessible
                AttributeError: if `facilities_list` is not a valid list of `Facility` objects
                TypeError: if `facilities_list` has an invalid value

            Side Effects:
                Writing to a file
        """
        if facilities_list is None:
            facilities_list = self.facilities_list

        drop_columns = ['balance_amount', 'bank_id', 'banned_states', 'initial_amount',
                        'interest_rate', 'max_default_likelihood', 'current_yield']
        yield_report = pd.DataFrame(vars(f) for f in facilities_list)
        yield_report['expected_yield'] = yield_report.current_yield.apply(lambda amount: round(amount))
        yield_report = yield_report.drop(drop_columns, axis=1)
        yield_report.to_csv(path_or_buf=csv_filepath, index=False)
