#!/usr/bin/env python

def isValidReference(token):
    """
        Validate a Token Reference Syntax

        Arguments:
            token: string

        Returns:
            None

        Raises:
            None

        Side Effects:
            None
    """
    if len(token) == 2 and token[0].isalpha() and token[1].isnumeric():
        return True
    else:
        return False


def extract_token_reference(spreadsheet_df, cell):
    """
        Resursively dereference cell reference pointers with corresponding values.

        Arguments:
            spreadsheet_df: source spreadsheet dataframe
            cell: cell to be dereferenced

        Returns:
            None

        Raises:
            None

        Side Effects:
            None
    """

    substituted_tokens = []
    for token in cell.split():
        if isValidReference(token):
            # Extract token references
            col_ref = token[0]
            row_ref = int(token[1])  # Reference rows start from 1
            ref_cell = spreadsheet_df[col_ref][row_ref]
            # NOTE: Recurssively evaluating the substituted cell
            token = extract_token_reference(spreadsheet_df, ref_cell)
        else:
            pass # do nothing
        substituted_tokens.append(token)
    # Return cell with tokens references substituted
    return ' '.join(substituted_tokens)
