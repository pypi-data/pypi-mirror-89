# -*- coding: utf-8 -*-
"""
Created by Babel Pte. Ltd.
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import itertools
from tqdm import tqdm
from scipy import stats as ss
import random
from datetime import timedelta
import tkinter as tk
import sys
from tkinter import filedialog


def cramers(x,y):
    """
    Function to calculate Cramers Correlation
    
    Input: column_1, column_2
    Output: correlation r (float)
    """
    confusion_matrix = pd.crosstab(x,y)
    chi2 = ss.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2/n
    r,k = confusion_matrix.shape
    phi2corr = max(0, phi2-((k-1)*(r-1))/(n-1))
    rcorr = r-((r-1)**2)/(n-1)
    kcorr = k-((k-1)**2)/(n-1)
    corr = np.sqrt(phi2corr/min((kcorr-1),(rcorr-1)))        
    return corr


def correlation(x, y, method='cramers'): #option for type of correlation added 
    """
    Function to calculate correlation in given method
    
    Input: column_1, column_2, method = ['pearson','spearman','kendall','cramers']
    Output: correlation r (float)
    """
    try:
        if (method == 'pearson'): 
            corr, _ = ss.pearsonr(x,y)
        elif (method == 'spearman'): 
            corr, _ = ss.spearmanr(x,y)
        elif (method == 'kendall'): 
            corr, _ = ss.kendalltau(x,y)
        elif (method == 'cramers'): 
            corr = cramers(x,y)
    except:
        corr = cramers(x,y)    
    return corr


def make_corr_dict(df, method='pearson'):
    """
    Function to make dictionaries of all column combinations and correlations
    
    Input: dataframe, method = ['pearson','spearman','kendall','cramers']
    Output: (correlation dictionary : singles, correlation dictionary : mirrored), Prints (Unused columns number and names)
    """
    for_corr = df[list(col for col in df.columns if ((df[col].nunique()!=df.shape[0]) & (df[col].notna().any()) ))]
    for_corr.fillna(0, inplace = True)
    col_combinations = list(itertools.combinations(for_corr.columns,2))
    method = "pearson"
    corr_dict = dict()
    for x, y in tqdm(col_combinations):
        print("\nProcessing" + str(x) + " " + str(y))
        corr_dict[(x,y)] = correlation(for_corr[x].astype('category').cat.codes,for_corr[y].astype('category').cat.codes, method)
    mirrors = dict(((b,a),(c)) for ((a,b),(c)) in corr_dict.items())
    corr_dict_mirror = corr_dict.copy()
    corr_dict_mirror.update(mirrors)
    print("Used Columns : ", str(len(for_corr.columns)))
    print("Unused Columns : ", str(len(df.columns)-len(for_corr.columns)))
    for_corr_cols = [str(k) for k in for_corr.columns]
    df_cols = [str(k2) for k2 in df.columns]
    print("Unused Col Names: ", str(np.setdiff1d(df_cols,for_corr_cols)))
    print("Completed creating correlation table")
    return(corr_dict, corr_dict_mirror)


def corr_table(corr_dict_mirror):
    """
    Function to visualize all correlations
    
    Input: Mirrored dictionary of correlations
    Output: Prints (heatmap)
    """
    print("Started creating final table & visualization")
    corr_table = pd.DataFrame(corr_dict_mirror, index=[0]).T.reset_index(level=[0,1]).pivot(index='level_0', columns='level_1')
    corr_table.columns = corr_table.columns.droplevel(0)
    corr_table.to_csv("Correlations amongst columns.csv", header=True, index=True)
    plt.figure(figsize=(10,10))
    svm = sns.heatmap(corr_table)
    figure = svm.get_figure()    
    figure.savefig('correlation table.png', dpi=400)
    print("Completed creating final table & visualization")
    

def significance(corr_dict, min_value, max_value):
    """
    Function to print all significant correlations between columns
    
    Input: Dictionary of Correlations: Singles, minimum value of correlational significance, maximum value of correlational significance
    Output: List of all significant column combinations
    """
    
    large_corr = pd.DataFrame(range(0,len(corr_dict)),corr_dict).reset_index(level=[0,1])
    large_corr = large_corr[(large_corr[0]>max_value)| (large_corr[0]<min_value)]
    print(large_corr.to_string(), "\n\n")


def browse_for_file(ct=0):
    """
    Function to enable users to select a file from anywhere on their laptop
    
    Input: Count of times the wrong file has been selected(ct)
    Output: Path & Name of the file selected
    """
    root = tk.Tk()
    root.withdraw() 
    file_name = filedialog.askopenfilename()
    if file_name.split('.')[-1] not in ['csv', 'xlsx', 'xls']:
        print("Please try to select only CSV or XLSX files. This package only processes these")
        print("You have " + str(4-ct) + " tries left to select the file.\n")
        ct+=1
        if ct==4:
            print("You seem to have selected the wrong file format a few times. \nPlease re-run and select only CSV or XLSX files")
            sys.exit()
        browse_for_file(ct)
    return file_name


def RFM_scorer(df, id_col, date_col, amount_col, show_graph = False):   
    """
    Function to perform Segmentation for Event Attendees
    
    Input: dataframe, id column name (str), date column name (str), 
            total amount column name (str), boolean to display distribution graphs
    Output: RFM dataframe
            distplots (optional)
    """
    print("\tBegin segmentation pre-processing")
    RFM = df.loc[:,[id_col,date_col,amount_col]]
    RFM['frequency']=0
    RFM[date_col] = pd.to_datetime(RFM[date_col])
    snapshot = RFM[date_col].max()+timedelta(days=1)
    print("\t\tBegin RFM segmentation")
    RFM = RFM.groupby([id_col]).agg({date_col:lambda x:(snapshot-x.max()).days, 'frequency':'count',amount_col:sum}).fillna(0)
    RFM.columns=['recency','frequency','monetary']
    r_labels = range(5, 0, -1); f_labels = range(1, 6); m_labels = range(1,6)
    r_groups = pd.qcut(RFM['recency'], q=5, labels=r_labels)
    f_groups = pd.qcut(RFM['frequency'], q=5, labels=f_labels)
    m_groups = pd.qcut(RFM['monetary'], q=5, labels=m_labels)
    print("\t\tRFM segmentation completed")
    RFM = RFM.assign(R = r_groups.values.astype(int), F = f_groups.values.astype(int), M = m_groups.astype(int))
    RFM['RFM'] = RFM[['R', 'F', 'M']].values.tolist()
    RFM['score'] = RFM.R + RFM.F +RFM.M
    if (show_graph):
        plt.figure(figsize=(12,10))
        plt.subplot(3, 1, 1); sns.distplot(RFM['recency'])
        plt.subplot(3, 1, 2); sns.distplot(RFM['frequency'])
        plt.subplot(3, 1, 3); sns.distplot(RFM['monetary'])
        plt.show()
    print("\tCompleted segmentation processing")
    return RFM


def rfm():
    """
    Function to perform Segmentation for Event Attendees
    
    Input: null
    Output: null
    """
    print("Begin segmentation for events")
    file_name = browse_for_file()
    print("Currently processing file - " + file_name)
    if file_name.split('.')[-1]=='csv':
        items = pd.read_csv(file_name)
    else:
        items = pd.read_excel(file_name, index_col=0)
    random.seed(43)
    items.head()
    test = RFM_scorer(items, 'user_account_id', 'TimeStamp', 'UnitPrice', show_graph = False)
    test.to_csv("RFM segmentation.csv", header=True, index=True)
    print("Completed segmentation for events")


def correlations():
    """
    Function to determine Correlations for all Event data
    
    Input: null
    Output: Correlations dataframe
    """
    file_name = browse_for_file()
    print("Currently processing file - " + file_name)
    if file_name.split('.')[-1]=='csv':
        test = pd.read_csv(file_name)
    else:
        test = pd.read_excel(file_name, index_col=0)
    corr_dict, corr_dict_mirror = make_corr_dict(test)
    corr_table(corr_dict_mirror)
