import os
import numpy as np
import pandas as pd
import sqlite3 as lite
from sqlalchemy import create_engine


def get_trx(date, path, what:str = 'thisMonth'):
    '''
    Return core TRX dataset from sqlite database
    @param:
        date   -Required : Maximum date you want to return data to.
        path   -Required : Connection to sqlite database.
        what   -Optional : thisMonth - return data for the current month/ 30days - return past 30days data from date.
    '''
    curr_tbl = 'core_{}'.format(str(date)[:7].replace('-','_'))
    prev_tbl = 'core_{}'.format(str(date - pd.DateOffset(months=1))[:7].replace('-','_'))
    
    if what == 'thisMonth':
        trx_df = pd.read_sql_table(curr_tbl, path)
        
    elif what == '30days':
        trx_df = pd.read_sql_table(curr_tbl, path)
        prev_df = pd.read_sql_query('select * from {} where EventDate > \'{}\''.format(prev_tbl, str((date - pd.DateOffset(days=30)).date())), path)
        trx_df = trx_df.append(prev_df, ignore_index=True)
    return trx_df


def get_special(date, conn, cat:str = None):
    """
    Load special list from database table special_list for the provided month.
    Special list include Franchise, TPC and Hospital agents.

    @param
    date: -required: Data of that entire month will be returned
    conn: -required: Database connector (sqlalchemy engine)
    cat:  -optional: Specify category to be returned [Franchise, TPC and Hospital] else will return all

    """
    query_1 = 'select * from special_list where cast(strftime(\'%m\', Month) as integer) = {} and cast(strftime(\'%Y\', Month) as integer) = {}'.format(date.month, date.year)
    query_2 = query_1 + ' and [Type] = \"{}\"'.format(cat)
    special_df = pd.DataFrame()

    if cat == None:
        special_df = pd.read_sql_query(query_1, conn, parse_dates=['Month'])
    elif cat in ['Franchise', 'Hospital', 'TPC']:
        special_df = pd.read_sql_query(query_2, conn, parse_dates=['Month'])
    return special_df



def get_franchise(date, path):
    '''
    Return franchise base from that month from sqlite database
    @param:
        date   -Required : Report Month.
        path   -Required : Connection to sqlite database.
    '''
    fra_df = pd.read_sql_query('select * from Franchise_2020', path, parse_dates = ['Month'])
    fra_df = fra_df[(fra_df.Month.dt.month == date.month) & (fra_df.Month.dt.year == date.year)]
    fra_df.FloatAcc = fra_df.FloatAcc.apply(lambda x:x.strip())
    return fra_df[['Month', 'Agent', 'FloatAcc']]


def get_target(date, path):
    '''
    Return current month target from sqlite database
    @param:
        date   -Required : Report Month.
        path   -Required : Connection to sqlite database.
    '''
    target_df = pd.read_sql_query('select * from Targets', path, parse_dates = ['MONTH'])
    target_df = target_df[(target_df.MONTH.dt.month == date.month) & (target_df.MONTH.dt.year == date.year)]
    target_df = target_df.astype({'TARGET':'float', 'SORTCODE':'str'})
    target_df = target_df.pivot(index='SORTCODE', columns='TARGET_CAT', values='TARGET').reset_index()
    return target_df


def get_FAO(date, path):
    '''
    Return current month FAO recruitments from sqlite database
    @param:
        date   -Required : Report Month.
        path   -Required : Connection to sqlite database.
    '''
    fao = pd.read_sql_table('FAO_Recruitment', path, parse_dates=['SUBMITTED_DATE'])
    fao = fao[((fao.SUBMITTED_DATE.dt.month == date.month) & (fao.SUBMITTED_DATE.dt.year == date.year) & (fao.MFO_TYPE == 'AGENT'))]
    fao = fao.groupby(['SORTCODE']).agg({'ACCOUNT_NO':'count', 'MFO_MOBILE':pd.Series.nunique}).rename(columns={'ACCOUNT_NO':'OpenedACC', 'MFO_MOBILE':'MFO'}).reset_index()
    fao = fao.astype({'SORTCODE':'str'})
    return fao


def get_regPOS(date, path):
    pos = pd.read_sql_query('select report_date, float_account, sortcode from pos_registration where (cast(strftime(\'%Y\', report_date) as integer) = {}) and (cast(strftime(\'%m\', report_date) as integer) = {})'.format(date.year, date.month), path)
    pos = pos.astype({'sortcode':'str'})
    pos.columns = pos.columns.str.upper()
    return pos


def get_agentApp(date, path):
    agents = pd.read_sql_query('select * from agent_application where (cast(strftime(\'%Y\', MONTH) as integer) = {}) and (cast(strftime(\'%m\', MONTH) as integer) = {})'.format(date.year, date.month), path)
    agents = agents.astype({'SORTCODE':'str'})
    agents = agents.groupby(['SORTCODE']).agg({'AGENT': 'count'}).reset_index()
    return agents

def get_branchinfo(path):
    branches = pd.read_sql_table('branchinfo', path)
    branches.columns = branches.columns.str.upper()
    branches = branches.astype({'SORTCODE': 'str'})
    return branches
