import pandas as pd
pd.set_option('display.max_columns',None)
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from xls2xlsx import XLS2XLSX
import datetime
import sidetable as stb
from IPython.display import clear_output
import shutil
import os
from datetime import date
today = date.today().strftime("%a-%b-%Y")
this_year = date.today().strftime("%Y")
last_year = int(this_year) - 1
clear_output()

app = Flask(__name__)
CORS(app)  # Menambahkan middleware CORS

# Link website
front = 'https://simbg.pu.go.id/Front'
dashb = 'https://simbg.pu.go.id/Dashboard'
kons = 'https://simbg.pu.go.id/Monitoring/Konsultasi'
path = "/home/sibedaspbg/chromedriver/chromedrivers"

# Customize chrome display
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')
chrome_options.add_argument('disable-notifications')
chrome_options.add_argument('--disable-infobars')

driver = webdriver.Chrome(executable_path=path, options=chrome_options)
driver.get(front)

wait10 = WebDriverWait(driver, 10)
wait20 = WebDriverWait(driver, 20)

html = driver.execute_script('return document.getElementsByTagName("html")[0].innerHTML')
soup = BeautifulSoup(html, 'html.parser')

btn_kng = wait10.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="PanduanAplikasi2"]/b/b/div/center/button')))
btn_kng.click()

try:
    btn_msk = driver.find_element(By.XPATH, '//*[@id="hero"]/div/div/div[2]/div/a[2]')
    btn_msk.click()
except:
    btn_kng = wait10.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="PanduanAplikasi2"]/b/b/div/center/button')))
    btn_kng.click()
finally:
    try:
        btn_msk = driver.find_element(By.XPATH, '//*[@id="hero"]/div/div/div[2]/div/a[2]')
        btn_msk.click()
    except:
        pass

usern = wait10.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmLogin"]/div[2]/div/div/div/div[1]/div/input')))
usern.send_keys('Chepysaefulrachman@gmail.com')
paswd = wait10.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmLogin"]/div[2]/div/div/div/div[2]/div/input')))
paswd.send_keys('habibie11')

btn_ijo = driver.find_element(By.XPATH, '//*[@id="frmLogin"]/div[3]/button[1]')
btn_ijo.click()

driver.get(dashb)

try:
    btn_kng1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Pemberitahuan"]/div[3]/center/button')))
    btn_kng1.click()
except:
    btn_kng1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Pemberitahuan"]/div[3]/center/button')))
    btn_kng1.click()

try:
    dd_monnit = wait10.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="headeradmin"]/div/div/ul/li[7]')))  #
    dd_monnit.click()
    dd_monnit.click()
    dd_monkot = wait10.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="headeradmin"]/div/div/ul/li[7]/ul/li/a')))
    dd_monkot.click()
except:
    btn_kng1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Pemberitahuan"]/div[3]/center/button')))
    btn_kng1.click()
finally:
    pass

driver.get(kons)

cetak = wait10.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmListVerifikasi"]/div/div/div[3]/div/div/a')))
cetak.click()

time.sleep(10)

driver.close()

x2x = XLS2XLSX(f'/home/sibedaspbg/api-puprbdg/Cetak Monitoring{today}.xls')
x2x.to_xlsx(f'/home/sibedaspbg/api-puprbdg/Cetak Monitoring{today}.xlsx')

cetak_mon = pd.read_excel(f'/home/sibedaspbg/api-puprbdg/Cetak Monitoring{today}.xlsx')[
    ['Jenis Konsultasi', 'No. Registrasi', 'Nama Pemilik', 'Lokasi BG', 'Status']]
os.remove(f'/home/sibedaspbg/api-puprbdg/Cetak Monitoring{today}.xls')
os.remove(f'/home/sibedaspbg/api-puprbdg/Cetak Monitoring{today}.xlsx')
cetak_mon['statusBaru'] = cetak_mon['Status'].copy()
cetak_mon['statusBaru'] = cetak_mon['statusBaru'].replace(['Verifikasi Kelengkapan Operator',
                                                           'Perbaikan Dokumen',
                                                           'Dikembalikan Untuk Revisi Dokumen'], 'Perbaikan Ulang')
cetak_mon['statusBaru'] = cetak_mon['statusBaru'].replace(['Verifikasi Ulang'], 'Verifikasi Ulang')
cetak_mon['statusBaru'][(cetak_mon['statusBaru'] != 'Perbaikan Ulang') &
                        (cetak_mon['statusBaru'] != 'Verifikasi Ulang')] = 'Selesai Verifikasi'
cetak_mon['Jenis'] = ""
cetak_mon['Jenis'] = cetak_mon['No. Registrasi'].apply(lambda x: x[:3])
cetak_mon = cetak_mon[cetak_mon['Jenis'] == 'PBG']

rekap = pd.read_excel('rekap pbg.xlsx')[
    ['No. Registrasi', 'TAHUN TERBIT', 'SKRD', 'Nilai Retribusi Keseluruhan']]
rekap['TAHUN TERBIT'].fillna(value=this_year, inplace=True)

simbg = pd.merge(cetak_mon, rekap, how='left',
                 on=['No. Registrasi'])  # 'No. Registrasi','Nama Pemilik','Jenis Konsultasi','Lokasi BG','Fungsi BG','Tgl Permohonan'])
simbg['TAHUN TERBIT'].fillna(value=this_year, inplace=True)
simbg['Nilai Retribusi Keseluruhan'].fillna(value=50000001, inplace=True)

total_berkas = len(simbg)
berkas_terbit_last = len(simbg[simbg['TAHUN TERBIT'] == last_year])
total_berkas_now = len(simbg[simbg['TAHUN TERBIT'] == this_year])
total_berkas_now_perc = ((total_berkas_now) / total_berkas) * 100
berkas_aktual_belum_terverifikasi = len(
    simbg['statusBaru'][(simbg['statusBaru'] != "Selesai Verifikasi") &
                        (simbg['TAHUN TERBIT'] == this_year)])
berkas_aktual_belum_terverifikasi_perc = (berkas_aktual_belum_terverifikasi / total_berkas_now) * 100
potensi_besar = len(simbg[(simbg['Nilai Retribusi Keseluruhan'] > 50000000) &
                          (simbg['statusBaru'] != "Selesai Verifikasi") &
                          (simbg['TAHUN TERBIT'] == this_year)])
potensi_besar_perc = (potensi_besar / berkas_aktual_belum_terverifikasi) * 100
potensi_kecil = len(simbg[(simbg['Nilai Retribusi Keseluruhan'] < 50000000) &
                          (simbg['statusBaru'] != "Selesai Verifikasi") &
                          (simbg['TAHUN TERBIT'] == this_year)])
potensi_kecil_perc = (potensi_kecil / berkas_aktual_belum_terverifikasi) * 100
berkas_aktual_terverifikasi_dinas_teknis = len(
    simbg['statusBaru'][(simbg['statusBaru'] == "Selesai Verifikasi") &
                        (simbg['TAHUN TERBIT'] == this_year)])
berkas_aktual_terverifikasi_dinas_teknis_perc = (
            berkas_aktual_terverifikasi_dinas_teknis / total_berkas_now) * 100
berkas_terbit_pbg = len(
    simbg[((simbg['Status'] == 'Menunggu Pengambilan Izin')
            | (simbg['Status'] == 'Penugasan Inpeksi')
            | (simbg['Status'].isna()))
            & (simbg['TAHUN TERBIT'] == this_year)])
berkas_terbit_pbg_perc = (berkas_terbit_pbg / berkas_aktual_terverifikasi_dinas_teknis) * 100
proses_penerbitan = berkas_aktual_terverifikasi_dinas_teknis - berkas_terbit_pbg
proses_penerbitan_perc = (proses_penerbitan / berkas_aktual_terverifikasi_dinas_teknis) * 100

terproses_di_ptsp = len(
    simbg[(simbg['Status'] == 'Menunggu Pembayaran Retribusi')
            | (simbg['Status'] == 'Menunggu Validasi Retribusi')
            | (simbg['Status'] == 'Pengiriman SKRD')])
terproses_di_ptsp_perc = (terproses_di_ptsp / proses_penerbitan) * 100
terproses_di_dputr = proses_penerbitan - terproses_di_ptsp
terproses_di_dputr_perc = (terproses_di_dputr / proses_penerbitan) * 100
jumlah_permohonan = total_berkas
dinas_perizinan = terproses_di_ptsp
telah_terbit_ditolak = berkas_terbit_last + berkas_terbit_pbg



@app.route('/api/monitoring', methods=['GET'])
def get_monitoring_data():
    data = {
        'total_berkas': total_berkas,
        'berkas_terbit_last': berkas_terbit_last,
        'total_berkas_now': total_berkas_now,
        'total_berkas_now_perc': total_berkas_now_perc,
        'berkas_aktual_belum_terverifikasi': berkas_aktual_belum_terverifikasi,
        'berkas_aktual_belum_terverifikasi_perc': berkas_aktual_belum_terverifikasi_perc,
        'potensi_besar': potensi_besar,
        'potensi_besar_perc': potensi_besar_perc,
        'potensi_kecil': potensi_kecil,
        'potensi_kecil_perc': potensi_kecil_perc,
        'berkas_aktual_terverifikasi_dinas_teknis': berkas_aktual_terverifikasi_dinas_teknis,
        'berkas_aktual_terverifikasi_dinas_teknis_perc': berkas_aktual_terverifikasi_dinas_teknis_perc,
        'berkas_terbit_pbg': berkas_terbit_pbg,
        'berkas_terbit_pbg_perc': berkas_terbit_pbg_perc,
        'proses_penerbitan': proses_penerbitan,
        'proses_penerbitan_perc': proses_penerbitan_perc,
        'terproses_di_ptsp': terproses_di_ptsp,
        'terproses_di_ptsp_perc': terproses_di_ptsp_perc,
        'terproses_di_dputr': terproses_di_dputr,
        'terproses_di_dputr_perc': terproses_di_dputr_perc,
        'jumlah_permohonan' : jumlah_permohonan,
        'dinas_perizinan' : dinas_perizinan,
        'telah_terbit_ditolak' : telah_terbit_ditolak


    }
    # return jsonify(data)
    
    response = make_response(jsonify({'data': data}), 200)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Mengatur header CORS
    return response

if __name__ == '__main__':
    app.run(debug=True)