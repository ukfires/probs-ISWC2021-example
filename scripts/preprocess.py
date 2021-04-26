#!/usr/bin/env python3

import sys
import os.path
import pandas as pd
import numpy as np

def prepare_col_list(df, col_str):
    if any(col_str in col for col in df.columns):
        columns = [col for col in df.columns if col_str in col]
        for col in columns:
            if df[col].dtype == np.int64:
                continue
            if df[col].dtype != np.number:
                df[col] = df[col].str.replace(".", "", regex=True)
            else:
                df = df.astype({col: str})
                #df[col] = df[col].to_string
                df[col] = df[col].str.replace(".", "", regex=True)
    return df
    
def correct_missing_data(df):
    qnt_columns = [col for col in df.columns if ("QNT" in col) or ("VAL" in col)]
    for column in qnt_columns:
        if pd.api.types.is_string_dtype(df[column]):
            df.loc[df[column] == ':' , column] = ''
    return df

def values_as_ints(df):
    qnt_columns = [col for col in df.columns if ("QNT" in col) or ("VAL" in col)]
    if "QNTUNIT" in qnt_columns:
        qnt_columns.remove("QNTUNIT") 
    for col in qnt_columns:
        if pd.api.types.is_string_dtype(df[col]):
            df[col] = df[col].str.replace(",", "", regex=True)
            df[col] = pd.to_numeric(df[col], errors='ignore')
    return df

def split_hirarchy(df):
    levels = [6]
    df = df[df['Aggregate Level'].isin(levels)]
    
    return df

def preprocess_files(filename, output_dir):
    if 'csv' in filename:
        df = pd.read_csv(filename, encoding= 'utf_8_sig',
                         dtype={"PRCCODE": str})
    elif 'xlsx' in filename:
        df = pd.read_excel(filename)
        filename = filename.replace('xlsx','csv')
    elif 'xls' in filename:
        df = pd.read_excel(filename)
        filename = filename.replace('xls','csv')
    else:
        print("Unknown filename extension:", filename)
        return

    df = prepare_col_list(df, "Code")
    df = prepare_col_list(df, "Parent")
    df = correct_missing_data(df)
    df = values_as_ints(df)
    if "ct-2018-" in filename:
        df = split_hirarchy(df)

    #####################################################################
    # For illustrative purposes -- ignore some 2018 PRODCOM data        #
    #                                                                   #
    # This is to make a simpler example with a lower-bound observation. #
    #####################################################################
    if "PRODCOM2018DATA" in filename:
        df = df[~df["PRCCODE"].isin(["08121190", "08121210"])]

    df.to_csv(os.path.join(output_dir, os.path.basename(filename)), index=False)


if __name__ == "__main__":
    raw_data_dir = sys.argv[1]
    out_data_dir = sys.argv[2]

    datasource_files = {
        "prodcom": [
            "PRD_2017_20200617_185035.csv",
            "PRD_2016_20200617_185122.csv",
            "PRODCOM2014DATA_extract.csv",
            "PRODCOM2016DATA.csv",
            "PRODCOM2017DATA.csv",
            "PRODCOM2018DATA.csv",
        ],
        "comtrade": [
            "ct-2018-exports.csv",
            "ct-2018-imports.csv",
            "HSCodeandDescription_2017.csv",

        ],
        # "object_mappings": [
        #     "object_mappings.csv",
        # ],
    }

    for source_name, filenames in datasource_files.items():
        print(f"Preparing files for datasource {source_name}...")
        for filename in filenames:
            print(f"    {filename}")
            preprocess_files(os.path.join(raw_data_dir, filename),
                             os.path.join(out_data_dir, source_name))
