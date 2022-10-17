import os
import numpy as np
import pandas as pd


def read_core(path:str = None, channel:bool = True, skip_keyword: str = 'TRANSACTIONID'):
    '''
    Documentation here
    '''
    core_df = pd.DataFrame()
    df_header = ['TransactionID', 'AgentName', 'BRC', 'Blank_1', 'TRXDate', 'AgentAccount', 'Narration', 
                 'AmountDebit', 'AmountCredit', 'CustomerAccount', 'CustomerName', 'BranchName', 'Blank_2']
    if channel: df_header.insert(11, 'Channel')
    try:
        if os.path.exists(path):
            skip_row = skip_rows(path, skip_keyword)
            if skip_row >= 0: # Means we know where to strart reading the data file
                core_df = pd.read_csv(path, sep='¥', skiprows=skip_row, engine='python', names=df_header).drop(columns=['Blank_1', 'Blank_2'])
                core_df = core_df.apply(lambda x: x.astype(str).str.upper())
                core_df = core_df.apply(lambda x: x.astype(str).str.strip())
                core_df.fillna('Undefined', inplace=True)
                
                core_df[['AmountDebit','AmountCredit']] = core_df[['AmountDebit','AmountCredit']].apply(lambda x:x.str.replace(',', '').astype('float'))
                core_df.TRXDate =  core_df.apply(lambda rw: format_date(rw['TRXDate']), axis=1)
                core_df.TRXDate = pd.to_datetime(core_df.TRXDate, dayfirst=False)
                core_df.insert(0, 'EventDate', core_df.TRXDate.dt.date) 
                core_df.EventDate = pd.to_datetime(core_df.EventDate, yearfirst=True, dayfirst=False)
       
        else: raise NameError('ERROR: Path do not exist \"{}\"'.format(path))
    except NameError as e: print(e)
    finally: return core_df


# -------------------------------------------------------------------------------------------------------

def read_comm(path:str):
    '''
    Documentation here
    '''
    comm_df = pd.DataFrame()
    try:
        if os.path.exists(path):
            header = ['TRXDate', 'AccountName', 'Code', 'BranchName', 'AgentAccount', 'CustomerAccount', 
                      'CustomerName', 'Narration', 'AmountDebit', 'AmountCredit', 'AgentCOMM', 'BranchCOMM']
            comm_df = pd.read_csv(path, names = header, sep = '\t', dtype=str, skiprows=1)
            
            # Processing
            comm_df.fillna('Undefined', inplace=True)
            comm_df = comm_df.apply(lambda x: x.str.upper())
            comm_df = comm_df.apply(lambda x: x.str.strip())
            
            # Formating
            comm_df.AmountDebit = comm_df.AmountDebit.str.replace(',', '')
            comm_df.AmountCredit = comm_df.AmountCredit.str.replace(',', '')
            comm_df.AgentCOMM = comm_df.AgentCOMM.str.replace(',', '')
            comm_df.BranchCOMM = comm_df.BranchCOMM.str.replace(',', '')
            
            comm_df = comm_df.astype({'AmountDebit': 'float64', 'AmountCredit': 'float64', 'AgentCOMM': 'float64', 'TRXDate': 'M'})
            comm_df.insert(0, 'EventDate', comm_df.TRXDate.dt.date)
            comm_df.EventDate = pd.to_datetime(comm_df.EventDate, yearfirst=True, dayfirst=False)
            

        else: raise NameError('Error: Path do not exist \"{}\"'.format(path))

    except NameError as e: print(e)
    finally:
        return comm_df

# -------------------------------------------------------------------------------------------------------


def skip_rows(file: str, lookup: str):
    '''
    Returnt number of rows to skip where reading Core TRX files
    @params:
        file     -Required : File locaton
        lookup   -Reguired : Word that appears on the first row
    '''
    occurance = []
    with open(file, 'r') as fl:
        for line_number, line in enumerate(fl,1):
            if lookup in line:
                occurance.append(line_number)
    return None if (len(occurance) == 0) else occurance[0]


def format_date(dt):
    return '{}-{}-{} {}'.format(dt[6:10], dt[3:5], dt[:2], dt[11:19])
