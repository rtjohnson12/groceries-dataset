# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
from apyori import apriori
from pathlib import Path
import pickle

# from dotenv import find_dotenv, load_dotenv

@click.command()
@click.argument('sales_filepath', type=click.Path(), default = 'data/raw/8570071016.csv')
@click.argument('lookup_filepath', type=click.Path(), default = 'data/raw/3390929248.csv')
def main(sales_filepath, lookup_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../interim).
    """
    logger = logging.getLogger(__name__)

    logger.debug('fetching category lookup')
    lookup = get_lookup(file_name = lookup_filepath)
    
    logger.debug('ingesting sales history')
    sales = get_sales(file_name = sales_filepath)

    logger.debug('merging sales and lookup')
    merged_df = pd.merge(sales, lookup, how = 'left', on = ['CategoryId', 'RetailerId'])

    logger.debug('computing and writing transactions data')
    all_products, transactions = summarize_transactions(merged_df)
    with open("data/interim/transactions.pickle", "wb") as f: pickle.dump(transactions, f)

    logger.debug('writing cleaned data frame')
    merged_df.to_csv('data/interim/clean_data.csv')
    
def get_sales(file_name):
    df = pd.read_csv(file_name, parse_dates = ['DeliveryDate'])
    df['RetailerId'] = df['RetailerId'].str.upper()

    # might be missing values in `Sold`, impute by group
    # intestestingly, all of the missing values occur on March 21st..
    df['Sold'] = df.groupby(['CategoryId', 'RetailerId'])['Sold'].ffill()

    return df

def get_lookup(file_name):
    df = pd.read_csv(file_name)
    df['RetailerId'] = df['RetailerId'].str.upper()

    return df

def summarize_transactions(df):
    """ Convert sales data to transactions list. No customer segmentation available, so separate by `RetailerName` and unique `DeliveryDate`
    Returns:
        list(strings): List of list
        [['beer', 'nuts'],
         ['beer', 'cheese']]
    """
    # find all sold products
    all_products = df.groupby('RetailerName').CategoryName.unique()

    # round transactions to nearest integer value
    temp = df
    temp['Sold'] = round(temp['Sold']).astype(int)
    temp = temp.reindex(temp.index.repeat(temp['Sold'])).reset_index(drop = True)
    transactions = temp.groupby(['RetailerName', 'DeliveryDate'])['CategoryName'].apply(list).groupby(level = 0).apply(list)

    return all_products, transactions

def run_apriori(transactions, retailer_index = 0):

    results = list(apriori(transactions[retailer_index], min_length = 2))

    for item in results:
        pair = item[0]
        items = [x for x in pair]
        print("Rule: " + items[0] + " -> " + items[1])
        print("Support: " + str(item[1]))
        print("Confidence: " + str(item[2][0][2]))
        print("Lift: " + str(item[2][0][3]))

    temp = [['beer', 'nuts'], ['beer', 'cheese']]
    results = list(apriori(temp))

    return results

def support(var, df):
    """
    Calculate support for item, i.e. how popular an item is by, as measured by the proportion of transactions in which an item appears
    """
    return len(df[df.itemDescription.isin(var)])/len(df)

def confidence(X, Y, df):
    """
    Calculate confidence for item {X -> Y}, i.e. how popular an item is by, as measured by the proportion of transactions in which X appears where Y also appears
    """
    return len(df[df.itemDescription.isin([X, Y])])/len(df[df.itemDescription.isin(Y)])

def lift(X, Y, df):
    """ How likely item Y is purchased when item X is purchased while controlling for how popular item Y is."""
    return confidence(X, Y, df)/support(Y, df)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_fmt)
    project_dir = Path(__file__).resolve().parents[2]

    main()
