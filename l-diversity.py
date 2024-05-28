import pandas as pd
from dataset_generator import dataGeneration

names = (
    'first name', 'last name', 'gender', 'age', 'zip code', 'role', 'education', 'salary'
)

numerical = ('age', 'zip code')

categorical = (
    'gender', 'role', 'education'
)
ei = (
    'first name', 'last name'
)
# read the dataset
df = dataGeneration()

# function to split the dataset into two partitions using the median for numerical columns
def split(df, partition, column):
    """
    :param        df: The dataframe to split
    :param partition: The partition to split
    :param    column: The column along which to split
    :        returns: A tuple containing a split of the original partition
    """
    dfp = df[column][partition]
    if column in categorical or column in ei:
        values = dfp.unique()
        lv = set(values[:len(values)//2])
        rv = set(values[len(values)//2:])
        return dfp.index[dfp.isin(lv)], dfp.index[dfp.isin(rv)]
    else:        
        median = dfp.median()
        dfl = dfp.index[dfp < median]
        dfr = dfp.index[dfp >= median]
        return (dfl, dfr)

# partition the dataset using the split function
def partitioning(df, feature_columns, sensitive_column, is_valid):
    finished_partitions = []
    partitions = [df.index]
    while partitions:
        partition = partitions.pop(0)
        for column in feature_columns:
            lp, rp = split(df, partition, column)
            if not is_valid(df, lp, sensitive_column) or not is_valid(df, rp, sensitive_column):
                continue
            partitions.extend((lp, rp))
            break
        else:
            finished_partitions.append(partition)
    return finished_partitions

# function to check if the dataset is k-anonymized
def is_k_anonymous(df, partition, sensitive_column, k=3):
    """
    :param               df: The dataframe on which to check the partition.
    :param        partition: The partition of the dataframe to check.
    :param sensitive_column: The name of the sensitive column
    :param                k: The desired k
    :returns               : True if the partition is valid according to our k-anonymity criteria, False otherwise.
    """
    if len(partition) < k:
        return False
    return True

# function that applies to the dataset l-diversity
def diversity(df, partition, column):
    return len(df[column][partition].unique())

# function to check if the dataset is l-diverse
def is_l_diverse(df, partition, sensitive_column, l=2):
    """
    :param               df: The dataframe for which to check l-diversity
    :param        partition: The partition of the dataframe on which to check l-diversity
    :param sensitive_column: The name of the sensitive column
    :param                l: The minimum required diversity of sensitive attribute values in the partition 
    """
    return diversity(df, partition, sensitive_column) >= l

# we apply our partitioning method to two columns of our dataset, using "income" as the sensitive attribute
feature_columns = ['first name', 'last name', 'gender', 'age', 'zip code', 'role', 'education']
sensitive_column = 'salary'
finished_partitions = partitioning(df, feature_columns, sensitive_column, is_k_anonymous)


# generating the anonymized dataset

# function to aggregate the dataset's columns
# we need to discuss how to aggregate categorical columns
def agg_categorical_column(series):
    return [','.join(set(series))]

def agg_numerical_column(series):
    return [series.mean()]

def agg_ei_column(series):
    return [series.apply(lambda x: '****')]

def agg_sensitive_column(series):
    return [series.apply(lambda x: round(x/10000)*10000)]

def build_anonymized_dataset(df, partitions, feature_columns, sensitive_column):
    rows = []
    a={}
    for partition in partitions:
        partition_data = df.loc[partition]
        for column in ei:
            a[column] = agg_ei_column(partition_data[column])
        print (a)
        aggregated_data = {}

        
        
# function to build the anonymized dataset
# def build_anonymized_dataset(df, partitions, feature_columns, sensitive_column):
#     aggregations = {}
#     sensitive_column = agg_sensitive_column
#     for column in feature_columns:
#         if column in categorical:
#             aggregations[column] = agg_categorical_column
#         elif column in numerical:
#             aggregations[column] = agg_numerical_column
#         elif column in ei:
#             aggregations[column] = agg_ei_column
#     rows = []
#     for i, partition in enumerate(partitions):
#         grouped_columns = df.loc[partition].agg(aggregations, squeeze=False)
#         # count occurrences of each sensitive value
#         sensitive_counts = df.loc[partition].groupby(sensitive_column).agg({sensitive_column : 'count'})
#         # Anonymized rows
#         values = grouped_columns.iloc[0].to_dict()
#         for sensitive_value, count in sensitive_counts[sensitive_column].items():
#             if count == 0:
#                 continue
#             values.update({
#                 sensitive_column : sensitive_value,
#                 'count' : count,
#             })
#             rows.append(values.copy())
#     return pd.DataFrame(rows)


dfn = build_anonymized_dataset(df, finished_partitions, feature_columns, sensitive_column)  

# l-diversity
finished_l_diverse_partitions = partitioning(df, feature_columns, sensitive_column, lambda *args: is_k_anonymous(*args) and is_l_diverse(*args))
dfl = build_anonymized_dataset(df, finished_l_diverse_partitions, feature_columns, sensitive_column)