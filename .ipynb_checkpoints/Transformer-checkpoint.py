import os
import numpy as np
import pandas as pd


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

def narrate(temp_df:pd.DataFrame):
    withdraw_trx = ['TMS CASH WITHDRAW', 'TMS AGENT WITHDRAW', 'MANUAL CASH', 'REF AGW', 'TMS B2B CO']
    deposit_trx = ['TMS UTT AMIS', 'TMS UDSM', 'TMS SAUT AC', 'TMS BUGANDO CUHAS AC', 'TMS BUGANDO HOSPITAL AC', 'TMS ALMUNTAZIR',
                   'TMS DECOHAS', 'TMS AMUCTA', 'TMS KCMUCO', 'TMS CASH DEP', 'TMS TUDARCO', 'TMS CRDB INSURANCE',
                   'TMS B2B CI', 'TMS TCC', 'TMS TLS AC', 'AGY DP', 'CASH DEPOSIT', 'TMS CASH DEPOSIT', 'CARD LESS DEPOSIT', 
                   'TMS CCM', 'TMS INST', 'TMS APPLEVALLEY AC', 'TMS TBL BEER PAYMENT AC', 'TMS SCHOOL FEES AC']
    bills_trx = ['TMS DANGOTE DEP', 'TMS AIRTEL TOP UP', 'TMS AZAM ACC', 'TMS AIRTEL CASHIN', 'TMS DSTV ACC', 'TMS HALOTOUP MOB', 
                   'TMS PRECISION AIR', 'TMS SMILE ACC', 'TMS SPORTS PAYMENTS AC', 'TMS STARTIMES ACC', 'TMS TIGO TOP UP MOB', 
                   'TMS TRA CONTROL NO', 'TMS TTCL AIRTIME MOB', 'TMS TTCL BROADBAND MOB', 'TMS VODACOM TOPUP MOB', 'TMS ZUKU AC']
    Mobile_deposit = ['TMS C2B HALOTEL', 'AIRTEL MONEY DEPOSIT', 'TIGOPESA C2B', 'M PESA DEPOSIT']
    float_depos = ['CASH DEPOS', 'TMS INT CASH IN']
    temp_df['Service'] = np.where((temp_df.Narration.str.contains('TMS GEPG-LUKU')), 'Luku',
                         np.where(((temp_df.Narration.str.contains('TMS GEPG BIL')) & (temp_df.AmountDebit > 0)), 'GEPG',
                         np.where(((temp_df.CustomerAccount.str.contains('01J7')) & (temp_df.AmountDebit > 0) & (temp_df.Narration.str.contains('DEPOSIT'))), 'A2A_Deposit',
                         np.where(((temp_df.Narration.str.contains('|'.join(withdraw_trx))) & (temp_df.AmountCredit > 0)), 'Withdraw',
                         np.where(((temp_df.Narration.str.contains('|'.join(deposit_trx))) & (temp_df.AmountDebit > 0)), 'Cust_Deposit',
                         np.where(((temp_df.Narration.str.contains('|'.join(bills_trx))) & (temp_df.AmountDebit > 0)), 'Bill',
                         np.where((temp_df.Narration.str.contains('TMS TRANSFER')), 'Transfer',  #check this
                         np.where((temp_df.Narration.str.contains('TMS CHARGE BALANCE')), 'Balance', #check this
                         # Float
                         np.where((temp_df.Narration.str.contains('TMS CHARGE MINISTATEMENT')), 'Mini_Statement', #check this
                         #A Agent Deposit
                         np.where((temp_df.Narration.str.contains('|'.join(Mobile_deposit))), 'Agent_Mobile_Deposit',
                         np.where(((temp_df.Narration.str.contains('INTERNAL TRX')) & (temp_df.AmountDebit == 0)), 'Agent_Chek_Deposit',
                         np.where(((temp_df.Narration.str.contains('ADVANCE LOANID')) & (temp_df.AmountDebit == 0)), 'Agent_Loan_Deposit',
                         np.where(((temp_df.Narration.str.contains('OMNFT  FROM')) & (temp_df.AmountDebit == 0)), 'Agent_Internet_Deposit',
                         np.where(((temp_df.Narration.str.contains('|'.join(float_depos))) & (temp_df.AmountDebit == 0)), 'Agent_Cash_Deposit',            
                         # Agent Withdraw                      
                         np.where(((temp_df.Narration.str.contains('ADVANCE LOANID')) & (temp_df.AmountDebit > 0)), 'Agent_Loan_Withdraw',
                         np.where(((temp_df.Narration.str.contains('|'.join(['CASH WD', 'CASH W/DRAW']))) & (temp_df.AmountDebit > 0)), 'Agent_Cash_Withdraw',
                         # VAT
                         np.where(((temp_df.CustomerName.str.contains('CRDB VAT COLLECTION')) & (temp_df.AmountDebit > 0)), 'VAT_Collection',
                                     'Unidentified Yet')))))))))))))))))
    return temp_df



#*************************************************************** COMPUTE REVENUE / COMMISSION /INCOME ********************************************************************


def compute_inc(dfx: pd.DataFrame, tarrif_df: pd.DataFrame):
    '''
    @Params:
        - dfx.is_franchise : Required : 1 if the trx is performed by franchise and 0 if normal agent.
        - dfx.Service     : Required : Deptict nature of transaction (Deposit, withdraw, luku, GePG, Bill)
        - dfx.Value       : Value of the transacted amount.
    '''
    dfx['Tarrif'] = np.where((dfx.Service.str.upper() == 'LUKU'), 'LUKU',  
                    np.where((dfx.Service.str.upper() == 'GEPG'), 'GEPG', 
                    np.where((dfx.Service.str.upper() == 'BILL'), 'BILL', 
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & (dfx.Value < 1000), 'w_00',         
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 1000) & (dfx.Value < 4000)), 'w_01',          
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 4000) & (dfx.Value < 5000)), 'w_02',          
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 5000) & (dfx.Value < 10000)), 'w_03', 
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 10000) & (dfx.Value < 20000)), 'w_04',        
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 20000) & (dfx.Value < 40000)), 'w_05',        
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 40000) & (dfx.Value < 50000)), 'w_06',        
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 50000) & (dfx.Value < 100000)), 'w_07',  
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 100000) & (dfx.Value < 200000)), 'w_08',      
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 200000) & (dfx.Value < 300000)), 'w_09',      
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 300000) & (dfx.Value < 400000)), 'w_10',      
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 400000) & (dfx.Value < 500000)), 'w_11',      
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 500000) & (dfx.Value < 600000)), 'w_12',      
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 600000) & (dfx.Value < 1000000)), 'w_13',    
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 1000000) & (dfx.Value < 2000000)), 'w_14',    
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 2000000) & (dfx.Value < 3000000)), 'w_15',    
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 3000000) & (dfx.Value < 4000000)), 'w_16',    
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 4000000) & (dfx.Value < 5000000)), 'w_17',    
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 5000000) & (dfx.Value < 8000000)), 'w_18',    
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 8000000) & (dfx.Value < 10000000)), 'w_19', 
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 10000000) & (dfx.Value < 15000000)), 'w_20',  
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 15000000) & (dfx.Value < 20000000)), 'w_21',  
                    np.where((dfx.Service.str.upper() == 'WITHDRAW') & ((dfx.Value >= 20000000) & (dfx.Value <= 24999999)), 'w_22', 
                    
                    np.where(((dfx.Service.str.upper() == 'CUST_DEPOSIT') & (dfx.Value < 200)), 'd_00', 
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 200) & (dfx.Value < 6000)), 'd_01',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 6000) & (dfx.Value < 9000)), 'd_02',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 9000) & (dfx.Value < 10000)), 'd_03',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 10000) & (dfx.Value < 20000)), 'd_04',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 20000) & (dfx.Value < 50000)), 'd_05',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 50000) & (dfx.Value < 100000)), 'd_06',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 100000) & (dfx.Value < 200000)), 'd_07',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 200000) & (dfx.Value < 300000)), 'd_08', 
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 300000) & (dfx.Value < 400000)), 'd_09',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 400000) & (dfx.Value < 500000)), 'd_10',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 500000) & (dfx.Value < 800000)), 'd_11',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 800000) & (dfx.Value < 1000000)), 'd_12',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 1000000) & (dfx.Value < 1500000)), 'd_13',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 1500000) & (dfx.Value < 2000000)), 'd_14',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 2000000) & (dfx.Value < 2500000)), 'd_15',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 2500000) & (dfx.Value < 3000000)), 'd_16',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 3000000) & (dfx.Value < 4000000)), 'd_17',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 4000000) & (dfx.Value < 5000000)), 'd_18',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 5000000) & (dfx.Value < 6000000)), 'd_19',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 6000000) & (dfx.Value < 7000000)), 'd_20',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 7000000) & (dfx.Value < 8000000)), 'd_21',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 8000000) & (dfx.Value < 9000000)), 'd_22',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 9000000) & (dfx.Value < 10000000)), 'd_23',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 10000000) & (dfx.Value < 11000000)), 'd_24',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 11000000) & (dfx.Value < 12000000)), 'd_25',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 12000000) & (dfx.Value < 13000000)), 'd_26',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 13000000) & (dfx.Value < 14000000)), 'd_27',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 14000000) & (dfx.Value < 15000000)), 'd_28',
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 15000000) & (dfx.Value < 15000000)), 'd_29', 
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 15000000) & (dfx.Value < 40000000)), 'd_30', 
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & ((dfx.Value >= 40000000) & (dfx.Value < 50000000)), 'd_31', 
                    np.where((dfx.Service.str.upper() == 'CUST_DEPOSIT') & (dfx.Value >= 50000000), 'd_32', 'Other' )))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
                             
    dfx = dfx.merge(tarrif_df, on='Tarrif', how='left')
    dfx['Commission'] = np.where((dfx.Tarrif =='BILL'), 0, 
                        np.where((dfx.Tarrif =='Other'), 0, 
                        np.where((dfx.Tarrif =='GEPG'), (dfx.AgentComm), 
                        np.where((dfx.Tarrif =='LUKU'), (dfx.Value * dfx.AgentComm), 
                        np.where((dfx.is_franchise == 0), (dfx.AgentComm), 
                        np.where((dfx.is_franchise == 1), (dfx.FranchComm), 0))))))

    dfx['Revenue'] = np.where((dfx.Tarrif.str.contains('|'.join(['BILL', 'GEPG', 'LUKU', 'Other', 'CUST_DEPOSIT']))), 0, 
                     np.where(((dfx.Service.str.upper() == 'WITHDRAW') & (dfx.is_franchise == 0)), (dfx.Charge/1.18),
                     np.where(((dfx.Service.str.upper() == 'WITHDRAW') & (dfx.is_franchise == 0)), (dfx.Charge/1.18), 0)))

    dfx['Income'] = np.where((dfx.Tarrif.str.contains('|'.join(['BILL', 'GEPG', 'LUKU', 'Other', 'CUST_DEPOSIT']))), 0, 
                    np.where(((dfx.Service.str.upper() == 'WITHDRAW') & (dfx.is_franchise == 0)), ((dfx.Charge/1.18) - dfx['Commission']),
                    np.where(((dfx.Service.str.upper() == 'WITHDRAW') & (dfx.is_franchise == 0)), ((dfx.Charge/1.18) - dfx['Commission']), 0)))              
    return dfx
    
#*************************************************************** END COMPUTE REVENUE / COMMISSION /INCOME ********************************************************************




























def inc_comm(is_franchise: bool, trx_type: str, amount: float):
    #comm = {'rev': 0, 'agent_comm': 0, 'branch_comm': 0}
    comm = (0,0,0)
    try:
        if trx_type.upper() == 'WITHDRAW':
            if amount < 1000 : token = [0, 0, 0]
            elif amount >= 1000 and amount < 4000: token = [300, 200, 230]
            elif amount >= 4000 and amount < 5000: token = [400, 200, 230]
            elif amount >= 5000 and amount < 10000: token = [550, 250, 287.5]
            elif amount >= 10000 and amount < 20000: token = [1100, 325, 373.75]
            elif amount >= 20000 and amount < 40000: token = [1300, 350, 402.5]
            elif amount >= 40000 and amount < 50000: token = [1500, 350, 402.5]
            elif amount >= 50000 and amount < 100000: token = [1800, 500, 575]
            elif amount >= 100000 and amount < 200000: token = [3350, 750, 862.5]
            elif amount >= 200000 and amount < 300000: token = [4450, 1200, 1380]
            elif amount >= 300000 and amount < 400000: token = [5400, 1400, 1610]
            elif amount >= 400000 and amount < 500000: token = [5900, 2000, 2300]
            elif amount >= 500000 and amount < 600000: token = [6300, 2000, 2300]
            elif amount >= 600000 and amount < 1000000: token = [6500, 2500, 2750]
            elif amount >= 1000000 and amount < 2000000: token = [6850, 2600, 2860]
            elif amount >= 2000000 and amount < 3000000: token = [7200, 2600, 2860]
            elif amount >= 3000000 and amount < 4000000: token = [7500, 2700, 3105]
            elif amount >= 4000000 and amount < 5000000: token = [8000, 2700, 3105]
            elif amount >= 5000000 and amount < 8000000: token = [8500, 3000, 3450]
            elif amount >= 8000000 and amount < 10000000: token = [9000, 3500, 4025]
            elif amount >= 10000000 and amount < 15000000: token = [10000, 5000, 5750]
            elif amount >= 15000000 and amount < 20000000: token = [15000, 7000, 8050]
            elif amount >= 20000000 and amount <= 24999999: token = [20000, 9000, 10350]
                
            if is_franchise == 1:
                comm = ((token[0]/1.18), token[2], (token[0]/1.18 - token[2]))
            else:
                comm = ((token[0]/1.18), token[1], (token[0]/1.18 - token[1]))
            
                
        elif trx_type.upper() == 'CUST_DEPOSIT':
            if amount < 200: token = [0, 0, 0]
            elif amount >= 200 and amount < 6000: token = [0, 100 ,105]
            elif amount >= 6000 and amount < 9000: token = [0, 140 ,147]
            elif amount >= 9000 and amount < 10000: token = [0, 150 ,158]
            elif amount >= 10000 and amount < 20000: token = [0, 200 ,210]
            elif amount >= 20000 and amount < 50000: token = [0, 250 ,263]
            elif amount >= 50000 and amount < 100000: token = [0, 300 ,315]
            elif amount >= 100000 and amount < 200000: token = [0, 450 ,473]
            elif amount >= 200000 and amount < 300000: token = [0, 550 ,578]
            elif amount >= 300000 and amount < 400000: token = [0, 800 ,840]
            elif amount >= 400000 and amount < 500000: token = [0, 900 ,945]
            elif amount >= 500000 and amount < 800000: token = [0, 1200 ,1236]
            elif amount >= 800000 and amount < 1000000: token = [0, 1300 ,1339]
            elif amount >= 1000000 and amount < 1500000: token = [0, 1500 ,1545]
            elif amount >= 1500000 and amount < 2000000: token = [0, 1600 ,1648]
            elif amount >= 2000000 and amount < 2500000: token = [0, 2000 ,2060]
            elif amount >= 2500000 and amount < 3000000: token = [0, 2500 ,2575]
            elif amount >= 3000000 and amount < 4000000: token = [0, 2600 ,2730]
            elif amount >= 4000000 and amount < 5000000: token = [0, 2800 ,2940]
            elif amount >= 5000000 and amount < 6000000: token = [0, 3000 ,3150]
            elif amount >= 6000000 and amount < 7000000: token = [0, 3000 ,3150]
            elif amount >= 7000000 and amount < 8000000: token = [0, 3000 ,3150]
            elif amount >= 8000000 and amount < 9000000: token = [0, 3000 ,3150]
            elif amount >= 9000000 and amount < 10000000: token = [0, 3000 ,3150]
            elif amount >= 10000000 and amount < 11000000: token = [0, 3200 ,3360]
            elif amount >= 11000000 and amount < 12000000: token = [0, 3200 ,3675]
            elif amount >= 12000000 and amount < 13000000: token = [0, 3200 ,3675]
            elif amount >= 13000000 and amount < 14000000: token = [0, 3200 ,3675]
            elif amount >= 14000000 and amount < 15000000: token = [0, 3200 ,3675]
            elif amount >= 15000000 and amount < 15000000: token = [0, 3500 ,4200]
            elif amount >= 15000000 and amount < 40000000: token = [0, 4000 ,4200]
            elif amount >= 40000000 and amount < 50000000: token = [0, 4500 ,4725]
            elif amount >= 50000000: token = [0, 5000, 5250]
    
            if is_franchise == 1:
                comm = (0, token[2], 0)
            else:
                comm = (0, token[1], 0)
                
        elif trx_type.upper() == 'LUKU':
            comm = (0, amount * 0.0075, 0)
        elif trx_type.upper() == 'GEPG':
            comm = (0, 200, 0)
            
    except:
        pass
    finally:
        return pd.Series(comm)