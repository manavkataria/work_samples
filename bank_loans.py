#!/usr/bin/env python
import pandas as pd

DIR_PATH = 'small/'
BANKS_CSV_PATH = DIR_PATH + 'banks.csv'
COVENANTS_CSV_PATH = DIR_PATH + 'covenants.csv'
FACILITIES_CSV_PATH = DIR_PATH + 'facilities.csv'
LOANS_CSV_PATH = DIR_PATH + 'loans.csv'

ASSIGNMENT_CSV_PATH = DIR_PATH + 'assignment_mk.csv'
YIELDS_CSV_PATH = DIR_PATH + 'yeilds_mk.csv'


def main():

    # TODO: Convert to ABC + Implementation
    banks_df = pd.read_csv(BANKS_CSV_PATH)
    covenants_df = pd.read_csv(COVENANTS_CSV_PATH)
    facilities_df = pd.read_csv(FACILITIES_CSV_PATH)
    loans_df = pd.read_csv(LOANS_CSV_PATH)


if __name__ == '__main__':
    main()
