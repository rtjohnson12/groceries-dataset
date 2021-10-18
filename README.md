
# Exploring Groceries Data

Data comes from https://github.com/shelfengine/interview.

## Setup

```
# Create virtual environment
python -m venv .venv

# Windows
# .venv\Scripts\activate.bat

# Unix or MacOS
# source .venv/bin/activate

# Install dependencies
python -m pip install -r requirements.txt
```

## Project Organization

    ├── README.md
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to process data
        │   └── make_dataset.py
        │
        ├── features       <- Scripts to turn raw data into features for modeling
        │   └── build_features.py
        │
        ├── models         <- Scripts to train models and then use trained models to make
        │   │                 predictions
        │   ├── predict_model.py
        │   └── train_model.py
        │
        └── visualization  <- Scripts to create exploratory and results oriented visualizations
            └── visualize.py


--------

## Running the Code

### Data Preparation

There are two data sources available in the project, 

To create interim data sources, run

```python
python src/data/make_dataset.py [optional sales filepath] [optional lookup filepath]
```

By adding `@click.argument` decorators from the `click` module, we can pass arguments to `src.data.make_dataset.main` via the command line. On Windows, I can run

```markdown
(.venv) PS C:\Users\rtjoh\Documents\Projects\groceries-dataset> python src/data/make_dataset.py .\data\raw\8570071016.csv .\data\raw\3390929248.csv
2021-10-16 22:44:37,077 - __main__ - DEBUG - fetching category lookup
2021-10-16 22:44:37,079 - __main__ - DEBUG - ingesting sales history
2021-10-16 22:44:37,083 - __main__ - DEBUG - merging sales and lookup
2021-10-16 22:44:37,085 - __main__ - DEBUG - computing and writing transactions data
2021-10-16 22:44:37,211 - __main__ - DEBUG - writing cleaned data frame
```

The first argument is the file path to the sales data, and the second argument is the file path to the lookup data. In practice, I imagine that these data sources are stored in a database as opposed to `.csv` files so the arguments could be modified to specify a date range parameter. Running this command creates two files:

* `clean_data.csv` - Processed sales data joined with lookup values.
* `transactions.pickle` - Processed transaction data formatted for use by the `apyori` module (https://pypi.org/project/apyori/).

Regarding the transactions data, the standard format accepted by the `apyori` module is as follows:

```python
from apyori import apriori

transactions = [
    ['beer', 'nuts'],
    ['beer', 'cheese'],
]
results = list(apriori(transactions))
```

In this example, the list elements correspond to individual "transactions". Unfortunately, there is no customer segmentation in the sales data provided. Without it, it is difficult to tie together individual purchases.

```
>>> merged_df
    DeliveryDate  WeekNumber  CategoryId                            RetailerId  Sold     CategoryName RetailerName
0     2021-03-01           9           0  BEE9891F-628C-467C-8292-008B938BBC34   0.0             Bowl   Retailer A
1     2021-03-02           9           0  BEE9891F-628C-467C-8292-008B938BBC34   0.0             Bowl   Retailer A
2     2021-03-03           9           0  BEE9891F-628C-467C-8292-008B938BBC34   2.0             Bowl   Retailer A
3     2021-03-04           9           0  BEE9891F-628C-467C-8292-008B938BBC34   0.0             Bowl   Retailer A
4     2021-03-05           9           0  BEE9891F-628C-467C-8292-008B938BBC34   4.0             Bowl   Retailer A
..           ...         ...         ...                                   ...   ...              ...          ...
803   2021-03-17          11          23  46D64632-2C73-4DBF-A3B3-EDFF547300F0   0.0  Vegetable Trays   Retailer C
804   2021-03-18          11          23  46D64632-2C73-4DBF-A3B3-EDFF547300F0   1.0  Vegetable Trays   Retailer C
805   2021-03-19          11          23  46D64632-2C73-4DBF-A3B3-EDFF547300F0   0.0  Vegetable Trays   Retailer C
806   2021-03-20          11          23  46D64632-2C73-4DBF-A3B3-EDFF547300F0   1.0  Vegetable Trays   Retailer C
807   2021-03-21          11          23  46D64632-2C73-4DBF-A3B3-EDFF547300F0   1.0  Vegetable Trays   Retailer C
```

For the purposes of this analysis, we will assume that there is only a single purchase each day per `RetailerId`.


