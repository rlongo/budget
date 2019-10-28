#!/usr/bin/env python3

import os
import sys

import pandas as pd

def read_tables(data_dir):
    """
    Reads out table data in csv format.
    :param data_dir: A directory containing all CSV files to read in
    """
    li = []

    for root, dirs, files in os.walk(data_dir):
        for f in files:
            if f.endswith(".csv"):
                p = os.path.join(root, f)
                df = pd.read_csv(p, index_col=None, header=0)
                li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    return frame

def main():
    if len(sys.argv) <= 1:
        data_dir = os.getcwd()
    else:
        data_dir = sys.argv[1]
    frame = read_tables(data_dir)
    print(frame.info())

if __name__=="__main__":
    main()
