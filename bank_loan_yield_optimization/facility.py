#!/usr/bin/env python


class Facility(object):
    """
        Facility class with all its associated covenants and metadata in one place

        Idempotent Interfaces:
            Facility(): Constructor to create a new facility
            is_valid_assignment(): Validates a loan assignment to this facility
            compute_loan_yield(): Computes expected yield given a `LoanRequest`

        Non-Idempotent Interfaces:
            issue_loan(): Assigns a loan to this facility
    """

    def __init__(self, facility_id, bank_id, initial_amount, interest_rate, max_default_likelihood, banned_states):
        """
            Constructor for `Facility` object

            Arguments:
                facility_id (integer)
                bank_id (integer)
                initial_amount (float)
                interest_rate (float)
                max_default_likelihood (float)
                banned_states (list of string)

            Returns:
                `Facility` object

            Raises:
                TypeError: if banned_states is not a hashable iterable
        """
        # TODO(Future): Make attributes private

        # Static attributes
        self.facility_id = facility_id
        self.bank_id = bank_id
        self.initial_amount = initial_amount
        self.interest_rate = interest_rate
        self.max_default_likelihood = max_default_likelihood
        self.banned_states = set(banned_states)  # optimizes lookup

        # Dynamic attributes
        self.balance_amount = initial_amount
        self.current_yield = 0.

    def __repr__(self):
        """
            Class object representation as a dictionary of attributes. Helpful during debugging
            and inspection.

            Arguments:
                None

            Returns:
                string: Representation of the object
        """
        return repr(vars(self))

    def is_valid_assignment(self, loan_request):
        """
            Validates loan request against all constraints and conventants goverened by this
            facility

            Arguments:
                loan_request (LoanRequest): Input loan request to validate assignment

            Returns:
                is_valid (bool)
        """

        # Validate against constraints & covenants
        if loan_request.origin_state in self.banned_states:
            return False
        if loan_request.default_likelihood > self.max_default_likelihood:
            return False
        if loan_request.amount > self.balance_amount:
            return False

        return True

    def compute_loan_yield(self, loan_request):
        """
            Validates loan request against all constraints and conventants goverened by this
            facility

            Arguments:
                loan_request (LoanRequest): Input loan request to compute yield

            Returns:
                expected_yield (float)
        """
        return loan_request.amount * ((1 - loan_request.default_likelihood) * loan_request.interest_rate - loan_request.default_likelihood - self.interest_rate)

    def issue_loan(self, loan_request):
        """
            Issues a loan from this facility

            NOTE: This is not an idempotent fuction as it issues side effects

            Arguments:
                loan_request (LoanRequest): Input loan request to compute yield

            Returns:
                expected_yield (float)

            Side Effects:
                1. `self.balance_amount` is updated to reflect remaining lendable amount in facility
                2. `self.current_yield` is updated to reflect current effective yield of the facility
        """
        # TODO(Future): Bake validation into issue_loan
        self.balance_amount = self.balance_amount - loan_request.amount
        expected_yield = self.compute_loan_yield(loan_request)
        self.current_yield += expected_yield

        return expected_yield
