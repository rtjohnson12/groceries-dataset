
import click
import logging
import pandas as pd
from pathlib import Path
import pdb
import pickle
from apyori import apriori


@click.command()
@click.argument('clean_df_filepath', type=click.Path(), default = 'data/interim/clean_data.csv')
@click.argument('transactions_filepath', type=click.Path(), default = 'data/interim/transactions.pickle')
def main(clean_df_filepath, transactions_filepath):
    """ Creates features and processes data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.debug('making model features from processed data')

    transactions = pd.read_pickle(transactions_filepath)
    run_apriori(transactions)




def run_apriori(transactions):
    # pdb.set_trace()

    # Retailer A
    pdb.set_trace()
    results = list(apriori(transactions[0], min_length = 2))
    results[0]

    for item in results:
        pdb.set_trace()
        pair = item[0]
        items = [x for x in pair]
        print("Rule: " + items[0] + " -> " + items[1])
        print("Support: " + str(item[1]))
        print("Confidence: " + str(item[2][0][2]))
        print("Lift: " + str(item[2][0][3]))

    temp = [['beer', 'nuts'], ['beer', 'cheese']]
    results = list(apriori(temp))

    pass


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_fmt)
    project_dir = Path(__file__).resolve().parents[2]

    main()
