# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import logging
from trendypy.trendy import Trendy
import click
import plotly.express as px
import pickle

def group_items_knn(df):
    pass

@click.command()
@click.option('--clusters', default = 3, help = 'Number of clusters for grouping time series')
@click.option('--interactive', default = False, help = 'Should interactive plots be opened in browser', is_flag = True)
def main(clusters, interactive):
    """ Run model training
    """ 
    logger = logging.getLogger(__name__)

    logger.info('loading cleaned data')
    merged_df = pd.read_csv('data/interim/clean_data.csv', parse_dates = ['DeliveryDate'])
    merged_df['NormSold'] = merged_df.groupby(['RetailerName', 'CategoryName'])['Sold'].apply(lambda x: ((x - x.min())/(x.max() - x.min())).fillna(0))
    merged_df['DoW'] = pd.Categorical(merged_df['DeliveryDate'].dt.day_name(), categories = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], ordered = True)

    logger.info('creating category series by date and retailer')
    my_dict = dict()
    for k, v in merged_df.groupby(['RetailerName', 'CategoryName']): my_dict[k] = v['NormSold']
    # pivot_df = merged_df.pivot_table(index = ['DeliveryDate', 'RetailerName'], columns = 'CategoryName', values = 'Sold', fill_value = 0).reset_index()
    
    logger.info(f'BEGIN running unsupervised clustering with {clusters} clusters')
    trendy = Trendy(n_clusters = clusters)
    trendy.fit([*my_dict.values()])
    logger.info('DONE running unsupervised clustering')

    logger.info('applying clustering labels to dataset')
    label_dict = my_dict
    for index, key in enumerate(my_dict): label_dict[key] = trendy.labels_[index]
    merged_df['ClusterLabel'] = merged_df.set_index(['RetailerName', 'CategoryName']).index.map(label_dict).astype('str')

    logger.info('creating cluster label dictionary')
    cluster_dict = merged_df.set_index('ClusterLabel')['CategoryName'].drop_duplicates().groupby('ClusterLabel').apply(list).to_dict()
    with open("data/processed/cluster_dict.pickle", "wb") as f: pickle.dump(cluster_dict, f)

    logger.info('generating `data/processed/labeled_cluster_distributions.png`')
    fig = px.box(merged_df.sort_values('DoW'), x = 'DoW', y = 'NormSold', color = 'ClusterLabel', template = 'plotly_white', title = 'Cluster Distributions by Day of Week')
    fig.for_each_trace(lambda t, cluster_dict = cluster_dict: t.update(name = 'Cluster: ' + t.name + '<br><br> * ' + '<br> * '.join(cluster_dict[t.name]) + '<br><br>'))
    fig.write_image(f'data/processed/labeled_{clusters}_cluster_distributions.png', width = 1980, height = 1080)
    if interactive: fig.show()

if __name__ == "__main__":
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()

