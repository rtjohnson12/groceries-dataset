# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import logging

def group_items_knn(df):
    pass

def main():
    """ Run model training
    """ 
    logger = logging.getLogger(__name__)

    logger.info('loading cleaned data')
    merged_df = pd.read_csv('data/interim/clean_data.csv', parse_dates = ['DeliveryDate'])
    
    import pdb; pdb.set_trace()

    pass

if __name__ == "__main__":
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()

