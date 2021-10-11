
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from apyori import apriori

df = pd.read_csv("data/Groceries_dataset.csv", parse_dates=['Date'])
df.head()

# check for null values
df.isnull().any()
# df.set_index('Member_number', inplace = True)

# Total Products
all_products = df.itemDescription.unique()
len(all_products)

# Displaying Top Products & Customer IDs
df.itemDescription.value_counts()
df.Member_number.value_counts()

# Top 10 frequently sold products
def distribution_plot(x, y, name = None, xaxis = None, yaxis = None):
    fig = go.Figure([go.Bar(x = x, y = y)])
    fig.update_layout(title_text = name, yaxis_title = yaxis, xaxis_title = xaxis)
    fig.show()
        
x = df.itemDescription.value_counts().sort_values(ascending = False)[:10]
distribution_plot(x.index, x.values)

# One-representation of products purchased
one_hot = pd.get_dummies(df.itemDescription)
df.drop('itemDescription', inplace = True, axis = 1)
df = df.join(one_hot)

# Transactional representation
records = df.groupby(["Member_number","Date"])[all_products[:]].apply(sum)
records = records.reset_index()[all_products]

# Replacing non-zero values with product names
def get_Pnames(x):
    for product in all_products:
        if x[product] > 0:
            x[product] = product
    return x

records = records.apply(get_Pnames, axis=1)
records.head()

# Removing zeros
transactions = [sub[~(sub == 0)].tolist() for sub in records.values if sub[sub != 0].tolist()]
transactions[0]

# Association Rules
rules = apriori(transactions, min_support = 0.00030, min_confidence = 0.05, min_lift = 3, min_length = 2, target = "rules")
association_results = list(rules)

for item in association_results:
    pair = item[0] 
    items = [x for x in pair]
    print("Rule: " + items[0] + " -> " + items[1])

    print("Support: " + str(item[1]))

    print("Confidence: " + str(item[2][0][2]))
    print("Lift: " + str(item[2][0][3]))
    print("=====================================")

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



raw_data.head(1).T
