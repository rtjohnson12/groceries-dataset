# -*- coding: utf-8 -*-
import logging
import requests
import pandas as pd
import json
from pathlib import Path
from apyori import apriori
# from dotenv import find_dotenv, load_dotenv

def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    print("Hello main")

def remove_outliers():
    pass

def impute_missing():
    pass

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    main()

def support(var, df):
    """
    Calculate support for item, i.e. how popular an item is by, as measured by the proportion of transactions in which an item appears
    Examples
        support(['candy', 'whole milk'], df)
    """
    return len(df[df.itemDescription.isin(var)])/len(df)

def confidence(X, Y, df):
    """
    Calculate confidence for item {X -> Y}, i.e. how popular an item is by, as measured by the proportion of transactions in which X appears where Y also appears
    Examples
        confidence(['candy'], ['whole milk'], df)
    """
    return len(df[df.itemDescription.isin([X, Y])])/len(df[df.itemDescription.isin(Y)])


def lift(X, Y, df):
    """ How likely item Y is purchased when item X is purchased while controlling for how popular item Y is."""

    return confidence(X, Y, df)/support(Y, df)
