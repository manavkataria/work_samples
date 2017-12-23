#!/usr/bin/env python


class LoanRequest(object):
    """
        LoanRequest object with its associated metadata.

        NOTE: For now this is a simple container class. In the future, this might potentially
        evolve to capture more complicated relationships across loan request types,
        financial entities and functions.

        Idempotent Interfaces:
            LoanRequest(): Constructor that encapsulates LoanRequest metadata

        Non-Idempotent Interfaces:
            None
    """

    def __init__(self, loan_id, amount, default_likelihood, interest_rate, origin_state):
        # TODO(Future): Make attributes private
        # TODO(Future): Documentation
        self.loan_id = loan_id
        self.amount = amount
        self.default_likelihood = default_likelihood
        self.interest_rate = interest_rate
        self.origin_state = origin_state

    def __repr__(self):
        return repr(vars(self))
