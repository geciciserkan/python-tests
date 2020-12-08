import itertools
import sys
import numpy as np
import pandas as pd
from datetime import datetime


class DataValidation(object):

    def __init__(self, data_file_path,check_cols_for_nan, check_cols_for_date_type,check_cols_for_dupes, possible_values_for_account_type):
        self.f = open(data_file_path)
        self.df = pd.read_csv(self.f, header=0)
        self.check_cols_for_nan =check_cols_for_nan
        self.check_cols_for_date_type =check_cols_for_date_type
        self.check_cols_for_dupes =check_cols_for_dupes
        self.possible_values_for_account_type=possible_values_for_account_type
        self.errors = []
        self.valid = False;

        self.check_int_columns()
        self.check_date_columns()
        self.check_account_types()
        self.check_dupes()

        if self.errors:
            print("Validation failed - {} errors found".format(len(self.errors)))
        else:
            self.valid=True
            print("Validation complete.")

    def check_int_columns(self):
        try:
            for  index, row in self.df.iterrows():
                for column in self.check_cols_for_nan:
                    if not isinstance(row[column], int):
                        raise TypeError("Row found with NaN.")
        except Exception as exec:
            self.errors.append(True)


    def check_date_columns(self):
        try:
            for  index, row in self.df.iterrows():
                for column in self.check_cols_for_date_type:
                        if not pd.to_datetime(self.df[column], format='%m/%d/%Y', errors='coerce').notnull().all():
                            raise TypeError("Row found with wrong date format.")
        except Exception as exec:
            self.errors.append(True)


    def check_account_types(self):
        try:
            actual = sorted(set(self.df.account_type.values))
            expected = sorted(set(self.possible_values_for_account_type))
            assert set(actual).issubset(expected)
        except Exception as exec:
            self.errors.append(True)


    def check_dupes(self):
        try:
            for column in self.check_cols_for_dupes:
                ids = self.df[column]
                duplicated = self.df[ids.isin(ids[ids.duplicated()])].sort_values(column)
                if len(duplicated):
                    raise ValueError("Duplciated rows found")
        except Exception as exec:
            self.errors.append(True )






###################################  CALL VALIDATION ########################################


data_file_path = './data-clean.csv'
check_cols_for_nan = ["age"]
check_cols_for_date_type = ["signup_date","birthday"]
check_cols_for_dupes = ["guid"]
possible_values_for_account_type=["google", "facebook", "other"]

result=DataValidation( data_file_path,check_cols_for_nan, check_cols_for_date_type,check_cols_for_dupes, possible_values_for_account_type)

def score():
    #scoring logic
    return 0.15523;

if result.valid:
   score_point=score()
   print("Score is {}".format(score_point))
else:
   raise ValueError("Score data is not valid. Please check validations logs")
