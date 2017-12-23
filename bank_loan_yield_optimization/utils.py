#!/usr/bin/env python
import csv
import os.path


def stream_writer(csv_filepath, header, row_values):
    """
        Stream Logger:
            Designed to _append_ to a shared resource log file. Thus opens and closes a connection
            for each append. Assuming no race-conditions. Ideally, this interface should reside
            on a distributed log server and be accessed as an API call to that server.

        NOTE: This is not an idempotent fuction as it issues side effects

        Arguments:
            csv_filepath (string)
            header (list of strings)
            row_values (list of values)

        Returns:
            None

        Raises:
            OSError: if csv_filepath is not accessible

        Side Effects:
            Writing to a file
    """

    file_exists = os.path.exists(csv_filepath)

    with open(csv_filepath, 'a') as csvfile:
        writer = csv.writer(csvfile)

        # file doesn't exist yet, write a header
        if not file_exists:
            writer.writerow(header)

        # append values
        writer.writerow(row_values)
