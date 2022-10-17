import os
import numpy as np
import pandas as pd
import re


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

# *************************NARRATE SERVICES********************************

def narrate(temp_df:pd.DataFrame):
    temp_df['Service'] = np.where(((temp_df.Narration.str.contains('^TMS INST')) & (temp_df.AmountDebit > 0)), 'DEPOSIT',
                         np.where(((temp_df.CustomerAccount.str.contains('^01J7')) & (temp_df.AmountDebit > 0) & (temp_df.Narration.str.contains('^TMS CASH DEPOSIT'))), 'A2A_DEPOSIT',
                         np.where(((temp_df.Narration.str.contains('^TMS CASH DEPOSIT')) & (temp_df.AmountDebit > 0)), 'DEPOSIT',
                         np.where(((temp_df.Narration.str.contains('^TMS CASH WITHDRAW')) & (temp_df.AmountCredit > 0)), 'CASH WITHDRAW',
                                     'Unidentified Yet'))))
    return temp_df
# *************************NARRATE SERVICES********************************


def compute_Tarrif(dfx: pd.DataFrame):
    dfx['OldRevenue'] = np.where((dfx.Service.str.upper() == 'INSTITUTIONAL PAYMENT'), 1000,  
                    np.where((dfx.Service.str.upper() == 'OTHER CRDB ACCOUNTS'), 1000,
#                   CUSTOMER WITHDRAW TARRIFS         
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.Amount < 1000), 0,
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount >= 1000) & (dfx.Amount <= 30000)), 500,
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 30000) & (dfx.Amount <= 50000)), 750,      
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 50000) & (dfx.Amount <= 75000)), 1000,     
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 75000) & (dfx.Amount <= 100000)), 1500,
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 100000) & (dfx.Amount <= 250000)), 2000,
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 250000) & (dfx.Amount <= 500000)), 2500,      
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 500000) & (dfx.Amount <= 750000)), 3000,     
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 750000) & (dfx.Amount <= 1000000000)), 4000,        
#                   CUSTOMER DEPOSIT TARRIFS
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.Amount < 1000), 0,
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount >= 1000) & (dfx.Amount <= 30000)), 250,
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 30000) & (dfx.Amount <= 50000)), 375,      
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 50000) & (dfx.Amount <= 75000)), 500,     
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 75000) & (dfx.Amount <= 100000)), 750,
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 100000) & (dfx.Amount <= 250000)), 1000,
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 250000) & (dfx.Amount <= 500000)), 1250,      
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 500000) & (dfx.Amount <= 750000)), 1500,     
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 750000) & (dfx.Amount <= 1000000000)), 2000,
#                   AGENT DEPOSIT TARRIFS
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & (dfx.Amount < 1000), 0,
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & ((dfx.Amount >= 1000) & (dfx.Amount <= 30000)), 250,
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & ((dfx.Amount > 30000) & (dfx.Amount <= 50000)), 375,      
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & ((dfx.Amount > 50000) & (dfx.Amount <= 75000)), 500,     
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & ((dfx.Amount > 75000) & (dfx.Amount <= 100000)), 750,
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & ((dfx.Amount > 100000) & (dfx.Amount <= 250000)), 1000,
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & ((dfx.Amount > 250000) & (dfx.Amount <= 500000)), 1250,      
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & ((dfx.Amount > 500000) & (dfx.Amount <= 750000)), 1500,     
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & ((dfx.Amount > 750000) & (dfx.Amount <= 1000000000)), 2000,
                    0 )))))))))))))))))))))))))))))
                                         
    return dfx
    
#*************************************************************** END COMPUTE REVENUE ********************************************************************

def compute_commission(dfx: pd.DataFrame):
    dfx['OldCommission'] = np.where((dfx.Service.str.upper() == 'INSTITUTIONAL PAYMENT'), 1000,  
                    np.where((dfx.Service.str.upper() == 'OTHER CRDB ACCOUNTS'), 1000,
#                   AGENT WITHDRAW COMMISSION         
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.Amount < 1000), 0,
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount >= 1000) & (dfx.Amount <= 30000)), 250,
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 30000) & (dfx.Amount <= 50000)), 375,      
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 50000) & (dfx.Amount <= 75000)), 500,     
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 75000) & (dfx.Amount <= 100000)), 750,
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 100000) & (dfx.Amount <= 250000)), 1000,
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 250000) & (dfx.Amount <= 500000)), 1250,      
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 500000) & (dfx.Amount <= 750000)), 1500,     
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 750000) & (dfx.Amount <= 1000000000)), 2000,        
#                   AGENT DEPOSIT COMMISSION     
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.Amount < 1000), 0,
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount >= 1000) & (dfx.Amount <= 30000)), 250,
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 30000) & (dfx.Amount <= 50000)), 375,      
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 50000) & (dfx.Amount <= 75000)), 500,     
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 75000) & (dfx.Amount <= 100000)), 750,
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 100000) & (dfx.Amount <= 250000)), 1000,
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 250000) & (dfx.Amount <= 500000)), 1250,      
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 500000) & (dfx.Amount <= 750000)), 1500,     
                    np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 750000) & (dfx.Amount <= 1000000000)), 2000,
#                   AGENT DEPOSIT COMMISSION
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & (dfx.Amount < 1000), 0,
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & ((dfx.Amount >= 1000) & (dfx.Amount <= 30000)), 250,
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & ((dfx.Amount > 30000) & (dfx.Amount <= 50000)), 375,      
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & ((dfx.Amount > 50000) & (dfx.Amount <= 75000)), 500,     
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & ((dfx.Amount > 75000) & (dfx.Amount <= 100000)), 750,
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & ((dfx.Amount > 100000) & (dfx.Amount <= 250000)), 1000,
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & ((dfx.Amount > 250000) & (dfx.Amount <= 500000)), 1250,      
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & ((dfx.Amount > 500000) & (dfx.Amount <= 750000)), 1500,     
                    np.where((dfx.Service.str.upper() == 'A2A_DEPOSIT') & ((dfx.Amount > 750000) & (dfx.Amount <= 1000000000)), 2000,
                    0 )))))))))))))))))))))))))))))
                                         
    return dfx
    
#*************************************************************** END COMPUTE  COMMISSION********************************************************************

def compute_new_tarrif(dfx: pd.DataFrame):
    dfx['NewRevenue'] = np.where((dfx.Service.str.upper() == 'OTHER CRDB ACCOUNTS'), 1000,
#                   CUSTOMER WITHDRAW TARRIFS         
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.Amount < 500), 0,
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount >= 500) & (dfx.Amount <= 1000)), 50,
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 1000) & (dfx.Amount <= 2500)), 150,
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 2500) & (dfx.Amount <= 5000)), 220,      
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 5000) & (dfx.Amount <= 10000)), 300,     
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 10000) & (dfx.Amount <= 20000)), 560,
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 20000) & (dfx.Amount <= 30000)), 750,
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 30000) & (dfx.Amount <= 50000)), 1300,      
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 50000) & (dfx.Amount <= 100000)), 1900,     
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 100000) & (dfx.Amount <= 200000)), 2750,
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 200000) & (dfx.Amount <= 300000)), 3800,
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 300000) & (dfx.Amount <= 400000)), 4500,
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 400000) & (dfx.Amount <= 500000)), 5000,
                    np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount > 500000) & (dfx.Amount <= 10000000000)), 7000, 
                    0 )))))))))))))))
                                         
    return dfx
    
#*************************************************************** END COMPUTE NEW REVENUE ********************************************************************
def compute_new_commission(dfx: pd.DataFrame):
#     NORMAL AGENT COMMISSION
    dfx['NewCommission'] = np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'NORMAL') & (dfx.Amount < 500), 0,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount >= 500) & (dfx.Amount <= 1000)), 20,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 1000) & (dfx.Amount <= 2500)), 60,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 2500) & (dfx.Amount <= 5000)), 90,      
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 5000) & (dfx.Amount <= 10000)), 120,     
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 10000) & (dfx.Amount <= 20000)), 200,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 20000) & (dfx.Amount <= 30000)), 260,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 30000) & (dfx.Amount <= 50000)), 380,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 50000) & (dfx.Amount <= 100000)), 550,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 100000) & (dfx.Amount <= 200000)), 950,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 200000) & (dfx.Amount <= 300000)), 1500,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 300000) & (dfx.Amount <= 400000)), 1800,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 400000) & (dfx.Amount <= 500000)), 2000,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 500000) & (dfx.Amount <= 10000000000)),3000,
#                   AGENT DEPOSIT COMMISSION  
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'NORMAL') & (dfx.AgentCI == dfx.CustomerCI), 0,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'NORMAL') & (dfx.Amount < 500), 0,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount >= 500) & (dfx.Amount <= 1000)), 5,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 1000) & (dfx.Amount <= 2500)), 35,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 2500) & (dfx.Amount <= 5000)), 50,      
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 5000) & (dfx.Amount <= 10000)), 70,     
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 10000) & (dfx.Amount <= 20000)), 130,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 20000) & (dfx.Amount <= 30000)), 180,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 30000) & (dfx.Amount <= 50000)), 250,      
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 50000) & (dfx.Amount <= 100000)), 290,     
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 100000) & (dfx.Amount <= 200000)), 480,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 200000) & (dfx.Amount <= 300000)), 900,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 300000) & (dfx.Amount <= 400000)), 1080,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 400000) & (dfx.Amount <= 500000)), 1200,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'NORMAL') & ((dfx.Amount > 500000) & (dfx.Amount <= 10000000000)), 1650,
#     FRANCHISE COMMISSION
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & (dfx.Amount < 500), 0,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount >= 500) & (dfx.Amount <= 1000)), 22,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 1000) & (dfx.Amount <= 2500)), 66,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 2500) & (dfx.Amount <= 5000)), 99,      
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 5000) & (dfx.Amount <= 10000)), 130,     
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 10000) & (dfx.Amount <= 20000)), 220,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 20000) & (dfx.Amount <= 30000)), 285,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 30000) & (dfx.Amount <= 50000)), 415,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 50000) & (dfx.Amount <= 100000)), 605,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 100000) & (dfx.Amount <= 200000)), 1045,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 200000) & (dfx.Amount <= 300000)), 1650,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 300000) & (dfx.Amount <= 400000)), 1980,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 400000) & (dfx.Amount <= 500000)), 2200,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 500000) & (dfx.Amount <= 1000000)),3300,
            np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 1000000) & (dfx.Amount <= 10000000000)),4000,
#                   AGENT DEPOSIT COMMISSION  
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & (dfx.AgentCI == dfx.CustomerCI), 0,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & (dfx.Amount < 500), 0,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount >= 500) & (dfx.Amount <= 1000)), 5,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 1000) & (dfx.Amount <= 2500)), 37,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 2500) & (dfx.Amount <= 5000)), 53,      
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 5000) & (dfx.Amount <= 10000)), 74,     
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 10000) & (dfx.Amount <= 20000)), 135,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 20000) & (dfx.Amount <= 30000)), 185,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 30000) & (dfx.Amount <= 50000)), 260,      
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 50000) & (dfx.Amount <= 100000)), 300,     
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 100000) & (dfx.Amount <= 200000)), 500,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 200000) & (dfx.Amount <= 300000)), 945,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 300000) & (dfx.Amount <= 400000)), 1120,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 400000) & (dfx.Amount <= 500000)), 1260,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 500000) & (dfx.Amount <= 1000000)), 1700,
            np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.isFranchise.str.upper() == 'FRANCHISE') & ((dfx.Amount > 1000000) & (dfx.Amount <= 1000000000000)), 1850,
            0 ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
    return dfx

# def compute_new_commission(dfx: pd.DataFrame):
#     dfx['NewCommission'] = np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.Amount < 500), 0,
#                     np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount >= 500) & (dfx.Amount <= 1000)), 20,
#                     np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 1000) & (dfx.Amount <= 2500)), 60,
#                     np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 2500) & (dfx.Amount <= 5000)), 90,      
#                     np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 5000) & (dfx.Amount <= 10000)), 120,     
#                     np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 10000) & (dfx.Amount <= 20000)), 200,
#                     np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 20000) & (dfx.Amount <= 30000)), 260,
#                     np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 30000) & (dfx.Amount <= 50000)), 380,
#                     np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 50000) & (dfx.Amount <= 100000)), 550,
#                     np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 100000) & (dfx.Amount <= 200000)), 950,
#                     np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 200000) & (dfx.Amount <= 300000)), 1500,
#                     np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 300000) & (dfx.Amount <= 400000)), 1800,
#                     np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 400000) & (dfx.Amount <= 500000)), 2000,
#                     np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 500000) & (dfx.Amount <= 10000000000)),3000,
# #                   AGENT DEPOSIT COMMISSION     
#                     np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.Amount < 500), 0,
#                     np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount >= 500) & (dfx.Amount <= 1000)), 5,
#                     np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 1000) & (dfx.Amount <= 2500)), 35,
#                     np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 2500) & (dfx.Amount <= 5000)), 50,      
#                     np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 5000) & (dfx.Amount <= 10000)), 70,     
#                     np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 10000) & (dfx.Amount <= 20000)), 130,
#                     np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 20000) & (dfx.Amount <= 30000)), 180,
#                     np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 30000) & (dfx.Amount <= 50000)), 250,      
#                     np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 50000) & (dfx.Amount <= 100000)), 290,     
#                     np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 100000) & (dfx.Amount <= 200000)), 480,
#                     np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 200000) & (dfx.Amount <= 300000)), 900,
#                     np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 300000) & (dfx.Amount <= 400000)), 1080,
#                     np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 400000) & (dfx.Amount <= 500000)), 1200,
#                     np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 500000) & (dfx.Amount <= 10000000000)), 1650,
#                     0 ))))))))))))))))))))))))))))
                                         
#     return dfx
    
#*************************************************************** END COMPUTE NEW COMMISSION********************************************************************

# def compute_new_commission(dfx: pd.DataFrame):
#     if dfx['AgentType'] == 'Normal':
#         dfx['NewCommission'] = np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & (dfx.Amount < 500), 0,
#                                np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') & ((dfx.Amount >= 500) & (dfx.Amount <= 1000)), 20,
#                                np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 1000) & (dfx.Amount <= 2500)), 60,
#                                np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 2500) & (dfx.Amount <= 5000)), 90,
#                                np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 5000) & (dfx.Amount <= 10000)), 120,
#                                np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 10000) & (dfx.Amount <= 20000)), 200,
#                                np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 20000) & (dfx.Amount <= 30000)), 260,
#                                np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 30000) & (dfx.Amount <= 50000)), 380,
#                                np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 50000) & (dfx.Amount <= 100000)), 550,
#                                np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 100000) & (dfx.Amount <= 200000)), 950,
#                                np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 200000) & (dfx.Amount <= 300000)), 1500,
#                                np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 300000) & (dfx.Amount <= 400000)), 1800,
#                                np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 400000) & (dfx.Amount <= 500000)), 2000,
#                                np.where((dfx.Service.str.upper() == 'CASH WITHDRAW') &  ((dfx.Amount > 500000) & (dfx.Amount <= 10000000000)),3000,
#         #                   AGENT DEPOSIT COMMISSION     
#                                np.where((dfx.Service.str.upper() == 'DEPOSIT') & (dfx.Amount < 500), 0,
#                                np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount >= 500) & (dfx.Amount <= 1000)), 5,
#                                np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 1000) & (dfx.Amount <= 2500)), 35,
#                                np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 2500) & (dfx.Amount <= 5000)), 50,      
#                                np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 5000) & (dfx.Amount <= 10000)), 70,     
#                                np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 10000) & (dfx.Amount <= 20000)), 130,
#                                np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 20000) & (dfx.Amount <= 30000)), 180,
#                                np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 30000) & (dfx.Amount <= 50000)), 250,      
#                                np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 50000) & (dfx.Amount <= 100000)), 290,     
#                                np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 100000) & (dfx.Amount <= 200000)), 480,
#                                np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 200000) & (dfx.Amount <= 300000)), 900,
#                                np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 300000) & (dfx.Amount <= 400000)), 1080,
#                                np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 400000) & (dfx.Amount <= 500000)), 1200,
#                                np.where((dfx.Service.str.upper() == 'DEPOSIT') & ((dfx.Amount > 500000) & (dfx.Amount <= 10000000000)), 1650,
#                                0 ))))))))))))))))))))))))))))
                                         
#     return dfx