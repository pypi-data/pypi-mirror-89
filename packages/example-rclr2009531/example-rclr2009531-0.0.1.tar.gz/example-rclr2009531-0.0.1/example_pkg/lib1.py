# 引進相關套件
import requests
from io import StringIO
import pandas as pd
import numpy as np


def max1(list2):
    max_no=list2[0]
    for i in list2:
        if i>max_no:
            max_no=i
    return max_no    
    
def calc_BMI(height, weight):
    '''
    1. 計算 BMI
    2. 判斷 體重是否過重
    '''
    BMI = float(weight)/((float(height)/100)**2)

    if BMI<18.5:
        message = "注意：您的體重太輕，要注意攝取營養。"
    elif 18.5<=BMI<25:
        message = "恭喜您！您的體重正常，請保持。"
    elif 25<=BMI<30:
        message = "注意：您的體重過重，請保持好的生活習慣來維持健康。"
    else:
        message = "注意：您體重已達肥胖，請保持好的生活習慣來維持健康。"
    
    return BMI, message
    
def print_9x9(x, y):
    out = ''
    for i in range(1, x+1):
        for j in range(1, y+1):
            out += f'{i:2d}*{j:2d}={i*j:2d}\t'
        out += '\n'
    return out
    
def check_prime(x):
    is_prime = True # 是質數
    for i in range(2, x):
        if x%i == 0:
            is_prime = False
            break
        
    return is_prime
    
    
def get_quote(stockNo, date1):
    '''
    1. 取得個股日成交資訊
    2. 用法：get_quote('2330', '20201210')
    '''
    # 網址
    url= 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date={}&stockNo={}'.format(date1, stockNo)

    # 送出要求，並取得回應資料
    response = requests.post(url)
    clean_data=[]
    for row in response.text.split('\n'):
        fields=row.split('",')
        if len(fields) == 10 and row[0] != '=':
            clean_data.append(row.replace(' ',''))

    csv_data = "\n".join(clean_data)
    
    df = pd.read_csv(StringIO(csv_data))

    # 刪除無用的欄位
    df.drop(df.columns[-1], axis=1, inplace=True)

    # 將以下欄位轉為數值
    numeric_columns=['成交股數','成交金額','成交筆數']
    for i in numeric_columns:
        df[i]=df[i].map(lambda x:x.replace(',', '').replace('--', ''))
        df[i]=pd.to_numeric(df[i])

    file_name = stockNo + '_' + date1 + '_成交資訊.xlsx'
    # append：df.to_csv('filepath', mode='a', index = False, header=None)
    df.to_excel(file_name, index=False)
    
    return file_name