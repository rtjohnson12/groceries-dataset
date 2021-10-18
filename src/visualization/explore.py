# -*- coding: utf-8 -*-
import logging
import pandas as pd
from pathlib import Path
import pdb
import matplotlib.pyplot as plt
import plotly.express as px
import kaleido
# from dotenv import find_dotenv, load_dotenv

def main():
    """ Run visualization scripts
    """
    logger = logging.getLogger(__name__)
    
    logger.info('loading cleaned data')
    merged_df = pd.read_csv('data/interim/clean_data.csv', parse_dates = ['DeliveryDate'])
    merged_df['DoW'] = pd.Categorical(merged_df['DeliveryDate'].dt.day_name(), categories = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], ordered = True)
    
    logger.info('generating `data/processed/sales_by_retailer.png`')
    # plot_data = merged_df.groupby(['RetailerName', 'CategoryName', 'DoW']).agg({'Sold': 'mean'}).reset_index()
    fig = px.box(merged_df, x = 'DoW', y = 'Sold', color = 'RetailerName', template = 'plotly_white', title = 'Distribution of Sales by Retailer')
    fig.write_image('data/processed/sales_by_retailer.png')
    # fig.show()

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
