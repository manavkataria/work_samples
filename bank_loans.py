#!/usr/bin/env python
import pandas as pd

DIR_PATH = 'small/'
BANKS_CSV_PATH = DIR_PATH + 'banks.csv'
COVENANTS_CSV_PATH = DIR_PATH + 'covenants.csv'
FACILITIES_CSV_PATH = DIR_PATH + 'facilities.csv'
LOANS_CSV_PATH = DIR_PATH + 'loans.csv'

ASSIGNMENT_CSV_PATH = DIR_PATH + 'assignment_mk.csv'
YIELDS_CSV_PATH = DIR_PATH + 'yeilds_mk.csv'


class Facility(object):
    """
        Facility class with all its associated covenants in one place

        Interfaces:
            Facility(...)
            is_valid_assignment(...)
    """

    def __init__(self, facility_id, bank_id, initial_amount, interest_rate, max_default_likelihood, banned_states):
        """
            Arguments:
                facility_id (integer):
                bank_id (integer):
                initial_amount (float):
                interest_rate (float):
                max_default_likelihood (float):
                banned_states (list of string):

            Returns:
                Returns a facility object given metadata

            Raises:
                FIXME:
                InvalidTypes: if banned_states is not a list
        """
        # TODO: Make attributes private
        self.facility_id = facility_id
        self.bank_id = bank_id
        self.initial_amount = initial_amount
        self.balance_amount = initial_amount
        self.interest_rate = interest_rate
        self.max_default_likelihood = max_default_likelihood
        self.banned_states = set(banned_states)

    def __repr__(self):
        return str({
            'facility_id': self.facility_id,
            'bank_id': self.bank_id,
            'initial_amount': self.initial_amount,
            'balance_amount': self.balance_amount,
            'interest_rate': self.interest_rate,
            'max_default_likelihood': self.max_default_likelihood,
            'banned_states': self.banned_states,
        })

    def is_valid_assignment(self, loan_request):
        """
            Arguments:
                loan: Loan object

            Returns:
                bool
        """
        # TODO: IMPLEMENT


class LoanRequest(object):
    """
        LoanRequest record with its associated metadata.

        NOTE: For now this is a simple container class. In the future, this might potentially evolve to capture more complicated relationships across financial entities (classes) and functions.
    """

    def __init__(self, loan_id, amount, default_likelihood, interest_rate, origin_state):
        # TODO: Make attributes private
        # TODO: Documentation

        self.loan_id = loan_id
        self.amount = amount
        self.default_likelihood = default_likelihood
        self.interest_rate = interest_rate
        self.origin_state = origin_state

    def __repr__(self):
        return str({
            'loan_id': self.loan_id,
            'amount': self.amount,
            'default_likelihood': self.default_likelihood,
            'interest_rate': self.interest_rate,
            'origin_state': self.origin_state,
        })


# TODO: Class Loan Server
def main():
    # TODO: Documentation

    # TODO: Convert to ABC + Implementation
    # Load data
    banks_df = pd.read_csv(BANKS_CSV_PATH)
    covenants_df = pd.read_csv(COVENANTS_CSV_PATH)
    facilities_df = pd.read_csv(FACILITIES_CSV_PATH)
    loans_df = pd.read_csv(LOANS_CSV_PATH)

    facilities_list = []
    # Load Facilities with its associated Covenats into a Class
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

    # Sort facility by `interest_rate` to optimize yield
    facilities_list.sort(key=lambda facility: facility.interest_rate)

    # Process Loans Stream
    for loan in loans_df.itertuples():
        loan_found = False

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

        # Iterate over facilities for loan assignments
        for facility in facilities_list:
            loan_found = facility.is_valid_assignment(loan_request)

            if loan_found:
                # Log to assignmenet file
                # Compute yield
                break


if __name__ == '__main__':
    main()
