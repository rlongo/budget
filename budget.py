#!/usr/bin/env python3

import numpy as np
import pandas as pd
from generator import Generator
import argparse

from read_inputs import read_tables
import matplotlib.pyplot as plt

grand_total_label = 'Total'
date_format_str = "{}-{:02d}"

def plot_cash_streams(streams, ax):
    streams.plot(kind='line', ax=ax)

def get_cash_streams(data):
    processed = data.groupby(['date-year', 'date-month', 'type'], as_index=False).sum()
    processed['date'] = processed.apply(lambda row: date_format_str.format(row['date-year'], row['date-month']), axis=1)
    return processed.pivot_table(index='date', columns='type', values='spend',
            margins=True, margins_name=grand_total_label, aggfunc=np.sum).drop(grand_total_label, axis=1)

def get_category_spend(data, category):
    return data.query('category=="{}"'.format(category)).groupby(['subcategory'], as_index=False)['spend'].sum()

def get_category_spend_monthly(data, category, add_total=False):
    df = data.query('category=="{}"'.format(category)).groupby(['date-year', 'date-month', 'subcategory'], as_index=False)['spend'].sum()
    df['date'] = df.apply(lambda row: date_format_str.format(row['date-year'], row['date-month']), axis=1)
    df['date'] = df.apply(lambda row: date_format_str.format(row['date-year'], row['date-month']), axis=1)
    df1 = df.pivot(index='subcategory', columns='date', values='spend')
    if add_total:
        df1['Total'] = df1.sum(axis=1)
    return df1

def plot_category_spend(data, ax, category):
    df = get_category_spend(data, category)
    df.plot(kind='bar', x='subcategory', y='spend', ax=ax)
    rects = ax.patches
    for rect, label in zip(rects, df['spend']):
        label = '${:,.2f}'.format(label)
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label, ha='center', va='bottom')

def plot_category_spend_monthly(data, ax, category):
    df = get_category_spend_monthly(data, category)
    df.plot(kind='bar', stacked=True, ax=ax)

    total_spend = df.sum(axis=1)
    rects = ax.patches
    for rect, label in zip(rects, total_spend):
        label = '${:,.2f}'.format(label)
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label, ha='center', va='bottom')

def main():
    parser = argparse.ArgumentParser(description='A budget tracking and monitoring tool')
    parser.add_argument('-i', dest='input_dir', metavar='input_dir', type=str,
            default='inputs', help='input directory containing budgeting csv files')
    args = parser.parse_args()
    input_dir = args.input_dir[0]

    print("Processing inputs in %s" % args.input_dir)
    data = read_tables(args.input_dir)
    
    # Show all Pandas floats as $ from here on out. If we don't want
    # this, have to do it per column (which is a little annoying)
    pd.options.display.float_format = '${:,.2f}'.format

    cash_streams = get_cash_streams(data)
    savings = get_category_spend(data, 'savings')
    debts = get_category_spend(data, 'debt')
    capex = get_category_spend_monthly(data, 'capex', True)
    monthly_expenses = get_category_spend_monthly(data, 'living', True)
    monthly_spend = get_category_spend_monthly(data, 'purchases', True)

    fig1, ax1 = plt.subplots()
    plot_cash_streams(cash_streams.drop(grand_total_label, axis=0), ax1)
    ax1.set_title('Cash Streams')
    fig1.savefig('cash-streams.png')

    # Add a delta column
    cash_streams['delta'] = cash_streams['income'] - cash_streams['expense']

    section_label = 'Annual'
    
    g = Generator()
    g.add_section_image(section_label, 'Annual Cash Flow', 'cash-streams.png')
    g.add_section_dataframe(section_label, None, cash_streams)
    g.add_section_dataframe(section_label, 'Accumulated Savings', savings)
    g.add_section_dataframe(section_label, 'Total Payments Towards Debts', debts) 
    g.add_section_dataframe(section_label, 'Total Capex', capex) 
    g.add_section_dataframe(section_label, 'Monthly Expenses', monthly_expenses) 
    g.add_section_dataframe(section_label, 'Monthly Spend', monthly_spend) 

    g.generate('output.html')

if __name__=="__main__":
    main()
