import pandas as pd
import numpy as np
import json
pd.set_option('display.max_columns',None)
import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# !pip3 install xls2xlsx
from xls2xlsx import XLS2XLSX
# !pip install gspread
import gspread
import datetime
from IPython.display import clear_output
import shutil
import os
from datetime import datetime
from datetime import date
from datetime import timedelta
import time
today=date.today().strftime("%Y-%m-%d")
todayxls=date.today().strftime("%a-%b-%Y")
yesterday = (date.today()- timedelta(days = 1)).strftime("%Y-%m-%d")
this_year = int(date.today().strftime("%Y"))
last_year = int(this_year)-1
last_last_year = int(this_year)-2
import re
import warnings
warnings.filterwarnings('ignore')
clear_output()

sa = gspread.service_account(filename = 'sibedaspbg-logbook-cab4b99bdcae.json')
sp = sa.open('rekap pbg')

sh = sp.worksheet('Data')

logb = pd.DataFrame(sh.get_all_values()[1:])
logb.columns = sh.get_all_values()[0]
tahuns = []
for tahun, year in zip(logb['TAHUN TERBIT'], logb['Tahun Berjalan']):
    tahuns.append(max(tahun, year))
logb['Tahun'] = tahuns
logb = logb[logb['Tahun']!='']
logb.drop(columns=['2/8','TAHUN TERBIT','Tahun Berjalan'],inplace=True)

s = requests.Session()

home_url = 'https://simbg.pu.go.id/Informasi'
home_resp = s.get(home_url, verify=False)
soup = BeautifulSoup(home_resp.text, 'html.parser')
csrf_test_name = soup.find('input', {'type': 'csrf_test_name'})

all_data = []

start = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
print(f'Start time: {start}')

for step, nomor in enumerate(logb['No. Registrasi'], start=1):
    url = f'https://simbg.pu.go.id/Informasi/Lacak/{nomor}?csrf_test_name={csrf_test_name}'
    resp = requests.get(url, verify=False)
    html = '<table> ' + resp.text + ' </table>'
    
    df = pd.read_html(html)[0].fillna('')
    df.columns = ['#', 'Modul', 'Tanggal', 'Keterangan']
    df['No. Registrasi'] = nomor
    print(f"Processing: {step}/{len(logb['No. Registrasi'])} ({(step / len(logb['No. Registrasi'])) * 100:.2f}%)", end="\r")
    all_data.append(df)

end = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
print(f'End time: {end}')

altogether_df = pd.concat(all_data)
altogether_df = altogether_df.drop(columns=['#']).rename(columns={'Tanggal':'Tanggal Log','Keterangan':'Keterangan Log'})

total_time = datetime.strptime(end, '%d-%b-%Y %H:%M:%S') - datetime.strptime(start, '%d-%b-%Y %H:%M:%S')
print(f"Data retrieval and processing completed!\nTotal time: {total_time}")

# logbook = pd.merge(logb, altogether_df, how='left', on='No. Registrasi')
# logb_json = logbook.drop(columns=['']).to_json(orient='records')
# logb_list = json.loads(logb_json)

row = altogether_df.shape[0]
col = altogether_df.shape[1]

worksheet_to_delete = sp.worksheet('logbook')
wks_logb = sp.del_worksheet(worksheet_to_delete)
wks_logb = sp.add_worksheet(title='logbook',rows=row,cols=col)

output_list = altogether_df.values.astype(str).tolist()
header = altogether_df.columns.tolist()
values_to_update = [header] + output_list

wks_logb.update('A1', values_to_update)

sa = gspread.service_account(filename = 'sibedaspbg-logbook-cab4b99bdcae.json')
sp = sa.open('rekap pbg')

sh = sp.worksheet('Data')

logb = pd.DataFrame(sh.get_all_values()[1:])
logb.columns = sh.get_all_values()[0]
tahuns = []
for tahun, year in zip(logb['TAHUN TERBIT'], logb['Tahun Berjalan']):
    tahuns.append(max(tahun, year))
logb['Usulan Retribusi']
logb['Tahun'] = tahuns
logb = logb[logb['Tahun']!='']
logb.drop(columns=['2/8','TAHUN TERBIT','Tahun Berjalan'],inplace=True)

sl = sp.worksheet('logbook')

log = pd.DataFrame(sl.get_all_values()[1:])
log.columns = sl.get_all_values()[0]
log = log[['No. Registrasi','Tanggal Log']].sort_values(by=['No. Registrasi','Tanggal Log'],ascending=True).groupby('No. Registrasi').last().reset_index()
# log = log[['No. Registrasi','Tanggal Log']].sort_values(by=['No. Registrasi','Tanggal Log'],ascending=True).groupby('No. Registrasi').last().reset_index()
log['Duration'] = ''
log['Duration'][log['Tanggal Log']=='Nomor Registrasi Tidak Ditemukan'] = 0
log['Duration'] = log['Tanggal Log'][log['Tanggal Log']!='Nomor Registrasi Tidak Ditemukan'].apply(lambda x:(datetime.strptime(today, '%Y-%m-%d') - datetime.strptime(x, '%Y-%m-%d')).days)
logb = pd.merge(logb,log[['No. Registrasi','Duration']],how='left',on=['No. Registrasi'])
logb['Nama Pemilik'] = logb['Nama Pemilik'].apply(lambda x:x.lower())
logb['Tgl Permohonan'] = pd.to_datetime(logb['Tgl Permohonan'],format="%Y/%m/%d")
# Link website
frontsimbg = 'https://simbg.pu.go.id/Front'
kons = 'https://simbg.pu.go.id/Monitoring/Konsultasi'
path = "D:\Downloads\chromedriver114_win32\chromedriver.exe"

# Customize chrome display
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')
chrome_options.add_argument('disable-notifications')
chrome_options.add_argument('--disable-infobars')

driver = webdriver.Chrome(executable_path = path, options=chrome_options)
driver.get(frontsimbg)
driver.maximize_window()

wait10 = WebDriverWait(driver, 10)
wait20 = WebDriverWait(driver, 20)

html = driver.execute_script('return document.getElementsByTagName("html")[0].innerHTML')
soup = BeautifulSoup(html,'html.parser')


btn_kng = wait10.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="PanduanAplikasi2"]/b/b/div/center/button')))
btn_kng.click()

try:
    btn_msk = driver.find_element(By.XPATH,'//*[@id="hero"]/div/div/div[2]/div/a[2]')
    btn_msk.click()
except:
    btn_kng = wait10.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="PanduanAplikasi2"]/b/b/div/center/button')))
    btn_kng.click()
finally:
    try:
        btn_msk = driver.find_element(By.XPATH,'//*[@id="hero"]/div/div/div[2]/div/a[2]')
        btn_msk.click()
    except:
        pass
    
usern = wait10.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="frmLogin"]/div[2]/div/div/div/div[1]/div/input')))
usern.send_keys('Chepysaefulrachman@gmail.com')
paswd = wait10.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="frmLogin"]/div[2]/div/div/div/div[2]/div/input')))
paswd.send_keys('habibie11')

btn_ijo = driver.find_element(By.XPATH,'//*[@id="frmLogin"]/div[3]/button[1]')
btn_ijo.click()

driver.get(kons)

cetak = wait10.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="frmListVerifikasi"]/div/div/div[3]/div/div/a')))
cetak.click()

time.sleep(20)

driver.close()
x2x = XLS2XLSX(f'D:/Downloads/Cetak Monitoring{todayxls}.xls')
x2x.to_xlsx(f'D:/Downloads/Cetak Monitoring{todayxls}.xlsx')
cetak_mon = pd.read_excel(f'D:/Downloads/Cetak Monitoring{todayxls}.xlsx').drop(columns=['E-Mail', 'No', 'No Kontak', 'No. Identitas', 'Lokasi BG', 'Fungsi BG', 'Tgl Permohonan','Alamat Pemilik','Jenis Konsultasi', 'Nama Pemilik'])
cetak_mon = cetak_mon[cetak_mon['No. Registrasi'].str.contains('PBG')]
lb = pd.merge(logb,cetak_mon,how='left',on=['No. Registrasi'])
lb.info()