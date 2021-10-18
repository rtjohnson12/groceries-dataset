# -*- coding: utf-8 -*-
import logging
import pandas as pd
from pathlib import Path
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import kaleido

def main():
    """ Run visualization
    """
    logger = logging.getLogger(__name__)
    
    logger.info('loading cleaned data')
    merged_df = pd.read_csv('data/interim/clean_data.csv', parse_dates = ['DeliveryDate'])
    # merged_df = merged_df.groupby(['RetailerName', 'CategoryName', 'DoW']).agg({'Sold': 'mean'}).reset_index()

    logger.info('generating `data/processed/sales_by_retailer.png`')
    fig = px.box(merged_df, x = 'DoW', y = 'Sold', color = 'RetailerName', template = 'plotly_white', title = 'Distribution of Sales by Retailer')
    fig.write_image('data/processed/sales_by_retailer.png')
    # fig.show()

    logger.info('generating `data/processed/sales_through_time.png`')
    fig = px.line(merged_df, x = 'DeliveryDate', y = 'Sold', color = 'CategoryName', facet_row = 'RetailerName', template = 'plotly_white', title = 'Category Sales Through Time')
    fig.update_yaxes(matches = None)
    fig.write_image('data/processed/sales_through_time.png')
    # fig.show()

    logger.info('generating `data/processed/normalized_sales_through_time.png`')
    norm_merged_df = merged_df
    norm_merged_df['Sold'] = norm_merged_df.groupby('CategoryName')['Sold'].apply(lambda x: (x - x.min())/(x.max() - x.min()))
    fig = px.line(norm_merged_df, x = 'DeliveryDate', y = 'Sold', color = 'CategoryName', facet_row = 'RetailerName', template = 'plotly_white', title = 'Category Sales Through Time')
    fig.update_yaxes(matches = None)
    fig.write_image('data/processed/sales_through_time.png')
    # fig.show()

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
