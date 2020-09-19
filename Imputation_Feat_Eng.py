import numpy as np
import pandas as pd


def impute_categorize(df, cols):
    def missing_val_info(df):
        '''Accepts a dataframe and prints a Series containing column names and
        the sum of their NaN values.'''

        print('Number of rows with NaN:', len(df[df.isna().any(axis=1)]), '\n')
        cols_na = df.loc[:, df.isna().any()] # df with only columns that have missing values

        if (len(df[df.isna().any(axis=1)]) > 0):
            print('Columns with NaN:\n', cols_na.isna().sum())
    
    missing_val_info(df)


    def drop_cols_majority_nan(df):
        '''Accepts a dataframe and returns a copy of the dataframe minus columns
        that had more than 90% missing values.'''

        drop_thresh = df.shape[0] * 0.9
        new_df = df.dropna(axis=1, how='all', thresh=drop_thresh).copy()  
        return new_df

    drop_cols_majority_nan(df)
    

    def impute(df, cols):
        '''Accepts a df and list of column names to fill NaN with the string N/A.'''

        df[cols] = df[cols].fillna('N/A')

    # If observation has TotalBsmtSF > 0, NaN in any Bsmt column != No Basement
    def impute_bsmt(df, cols):
        '''Accepts a df and list of column names to fill NaN with the string N/A,
           excluding cols that have TotalBsmtSF > 0.'''

        # Store rows where NaN != No Basement
        to_drop = df[cols][(df[cols].isna().any(axis=1)) & (df[cols].TotalBsmtSF > 0)]
        # After dropping rows, fill NaNs
        dframe = df[cols].drop(to_drop.index).fillna('N/A')
        df[cols] = pd.concat([dframe, to_drop])

    impute(df, cols)
    
    def missing_cols(df):
        '''Accepts a dataframe and returns a list of its columns containing NaN.'''

        return df.columns[df.isna().any()].tolist()

    missing_cols(df)

    def impute_categorical_mode(df, cols):
        '''Accepts a df and list of column names to fill NaN in categorical columns
        with the mode of each column.'''

        df[cols] = df[cols].fillna(train.mode().iloc[0])
    
    impute_categorical_mode(df, cols)

    def num_to_cat_variable(df, cols):
        '''Accepts a df and list of columns to convert into dtype category.'''
        df[cols] = df[cols].astype('category')

    date_cols = list(train.columns[train.columns.str.contains('Year')
                                   | train.columns.str.contains('Yr')
                                   | train.columns.str.contains('Mo')])
    
    num_to_cat_variable(df, cols)

    return df