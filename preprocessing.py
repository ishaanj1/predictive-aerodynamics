import numpy as np
import pandas as pd

def load_data():
    data_file_names = pd.read_csv('data_file_names.csv', header=None, squeeze=True)
    column_labels = pd.read_csv('column_labels.csv', header=None, squeeze=True)
    column_labels_ignore = pd.read_csv('column_labels_ignore.csv', header=None, squeeze=True)
    data_runs = []

    for data_file_name in data_file_names:
        data_run = pd.read_csv(data_file_name, header=None, names=column_labels)
        p_stag = data_run.loc[:, 'p_stagnation']
        p_static = data_run.loc[:, 'p_static']
        # convert static pressure measurements to pressure coefficients
        data_run = data_run.sub(p_static, axis='index').divide(p_stag - p_static, axis='index')
        # drop irrelevant columns from data_run
        data_run = data_run.drop(labels=column_labels_ignore, axis='columns')
        data_runs.append(data_run)
    return data_runs

def merge_rows(X, y, num_rows_merge):
    X_new = pd.DataFrame()
    y_new = pd.DataFrame()

    for i in range(0, X.shape[0], num_rows_merge):
        X_row = pd.Series(X.iloc[i:i+num_rows_merge, :].values.flatten())
        X_new = X_new.append(X_row, ignore_index=True)
        y_row = pd.Series(y.iloc[i+num_rows_merge-1])
        y_new = y_new.append(y_row, ignore_index=True)
    
    return X_new, y_new

def shuffle_rows(X, y):
    X_y = pd.concat([X, y], axis='columns', ignore_index=True)
    X_y = X_y.sample(frac=1).reset_index(drop=True)
    X = X_y.iloc[:, 0:-1]
    y = X_y.iloc[:, -1:]
    return X, y
