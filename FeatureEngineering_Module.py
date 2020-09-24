import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

import numpy as np


class FeatureEngineering():
    '''
    Goes through the entire feature engineering process
    Argument: 
        df: dataframe
    Returns: dataframe that went through feature engineering/selection
    '''
    def __init__(self, columns=None):
        self.columns = columns

    def transform(self, df):
        # Drop 4 outliers of GrLivArea in train set
        if len(df) == 1460:
            df.drop(df[df["GrLivArea"] > 4000].index, inplace = True)

        # Feature Transformation
        df["SecondFlr"] = df["2ndFlrSF"].apply(lambda x: 1 if x > 0 else 0)
        df["PorchSF"] = df["OpenPorchSF"]+df["EnclosedPorch"]+df["3SsnPorch"]+df["ScreenPorch"]
        df["ExtraRoom"] = df["TotRmsAbvGrd"] - df["BedroomAbvGr"]
        df["SinceRemod"] = df["YrSold"].astype(int) - df["YearRemodAdd"].astype(int)
        df["FullBaths"] = df["BsmtFullBath"] + df["FullBath"]
        df["HalfBaths"] = df["BsmtHalfBath"] + df["HalfBath"]
        df["LotShape"] = df["LotShape"].apply(lambda x: "IR" if ((x == "IR1") | (x == "IR2") | (x == "IR3")) else x)
        lotconf_ord = {"FR2":"FR", "FR3":"FR"}
        df["LotConfig"] = df["LotConfig"].replace(lotconf_ord)

        garagetype_ord = {"BuiltIn":"Attchd", "Basment": "Attchd", "CarPort": "Detchd", "2Types": "Attchd"}
        df["GarageType"] = df["GarageType"].replace(garagetype_ord)

        landcont_ord = {"Bnk":"NotLvl","HLS":"NotLvl","Low":"NotLvl"}
        df["LandContour"] = df["LandContour"].replace(landcont_ord)
        df["Condition1"] = df["Condition1"].apply(lambda x: "Abnorm" if x != "Norm" else x)

        df["RoofStyle"] = df["RoofStyle"].apply(lambda x: "Other" if x not in ["Gable", "Hip"] else x)

        df["HeatingQC"] = df["HeatingQC"].apply(lambda x: "BA" if ((x == "Fa") | (x == "Po")) else x)

        df["Functional"] = df["Functional"].apply(lambda x: "Nottyp" if x != "Typ" else x)

        df["SaleType"] = df["SaleType"].apply(lambda x: "Unconv" if x != "WD" else x)
        df["SaleCondition"] = df["SaleCondition"].apply(lambda x: "Unconv" if x != "Normal" else x)

        df["OverallQual"] = \
            df["OverallQual"].apply(lambda x: 
                "BA" if x < 5 else "Avg" if x == 5 else "AA" if x == 6 else "EX" if x > 8 else "GO")
        df["OverallCond"] = \
            df["OverallCond"].apply(lambda x: 
                "BA" if x < 5 else "Avg" if x == 5 else "AA" if x == 6 else "EX" if x > 8 else "GO")

        # Dropping Irrelevant Features
        def drop_feat(df, cols):
            df.drop(cols, axis = 1, inplace = True)
            return df

        cols = ["BsmtFinSF1", "BsmtFinSF2", "BsmtUnfSF", "TotalBsmtSF", "1stFlrSF", "2ndFlrSF", "LowQualFinSF",
        "OpenPorchSF", "EnclosedPorch", "3SsnPorch", "ScreenPorch", "TotRmsAbvGrd", "GarageYrBlt", "GarageArea",
        "YearRemodAdd", "YrSold", "YearBuilt", "BsmtFullBath", "FullBath", "BsmtHalfBath", "HalfBath", "MSSubClass",
        "Street", "Utilities", "Condition2", "RoofMatl", "BsmtFinType2", "Heating","LandSlope", "MiscVal", "PoolArea"]

        new_df = drop_feat(df, cols)
    
        return new_df
    
    def fit(self, df, y=None, **fit_params):
        return self


    
    
    
    
    
    
    
    