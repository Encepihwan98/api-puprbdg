from flask import Flask, Blueprint, jsonify
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
from xls2xlsx import XLS2XLSX
import gspread
import datetime
from IPython.display import clear_output
import shutil
import os
from datetime import datetime
from datetime import date
from datetime import timedelta
import time
from flask_cors import CORS
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

app = Flask(__name__)
CORS(app)

macetplan = Blueprint('macetplan', __name__)

sa = gspread.service_account(filename = 'sibedaspbg-logbook-cab4b99bdcae.json')

def fetch_data():
    sp = sa.open('rekap pbg')

# sh = sp.worksheet('Data')
    srn = sp.worksheet('rekap new')

    rekap_new = pd.DataFrame(srn.get_all_values()[1:])
    rekap_new.columns = srn.get_all_values()[0]
    rekap_new['Duration'] = rekap_new['Duration'].apply(lambda x:float(x))
    rekap_new['Usulan Retribusi'] = rekap_new['Usulan Retribusi'].apply(lambda x:float(x))

    # Print hasil
    berkas_aktual_belum_terverifikasi = rekap_new[(rekap_new['Status Permohonan']!="Selesai Verifikasi")&
                                            (rekap_new['Tahun']==str(this_year))]
    berkas_aktual_belum_terverifikasi_und7 = berkas_aktual_belum_terverifikasi['No. Registrasi'][(berkas_aktual_belum_terverifikasi['Duration']<=7)|
                                                                                                (berkas_aktual_belum_terverifikasi['Duration'].isna())].nunique()

    berkas_aktual_belum_terverifikasi_7to14 = berkas_aktual_belum_terverifikasi['No. Registrasi'][(berkas_aktual_belum_terverifikasi['Duration']>7)&
                                                                                                (berkas_aktual_belum_terverifikasi['Duration']<=14)].nunique()

    berkas_aktual_belum_terverifikasi_ov14 = berkas_aktual_belum_terverifikasi['No. Registrasi'][(berkas_aktual_belum_terverifikasi['Duration']>14)].nunique()
    # ----------------------------------------------------------------------------------------------------------------------------
    potensi_besar = rekap_new[(rekap_new['Usulan Retribusi']>50000000)&
                        (rekap_new['Status Permohonan']!="Selesai Verifikasi")&
                        (rekap_new['Tahun']==str(this_year))]

    potensi_besar_und7 = potensi_besar['No. Registrasi'][(potensi_besar['Duration'].isna())&
                                                        (potensi_besar['Duration']<=7)].nunique()

    potensi_besar_7to14 = potensi_besar['No. Registrasi'][(potensi_besar['Duration']>7)&
                                                        (potensi_besar['Duration']<=14)].nunique()

    potensi_besar_ov14 = potensi_besar['No. Registrasi'][(potensi_besar['Duration']>14)].nunique()
    # ----------------------------------------------------------------------------------------------------------------------------
    potensi_kecil = rekap_new[(rekap_new['Usulan Retribusi']<50000000)&
                        (rekap_new['Status Permohonan']!="Selesai Verifikasi")&
                        (rekap_new['Tahun']==str(this_year))]

    potensi_kecil_und7 = potensi_kecil['No. Registrasi'][(potensi_kecil['Duration'].isna())|
                                                        (potensi_kecil['Duration']<=7)].nunique()

    potensi_kecil_7to14 = potensi_kecil['No. Registrasi'][(potensi_kecil['Duration']>7)&
                                                        (potensi_kecil['Duration']<=14)].nunique()

    potensi_kecil_ov14 = potensi_kecil['No. Registrasi'][(potensi_kecil['Duration']>14)].nunique()
    # ----------------------------------------------------------------------------------------------------------------------------
    berkas_aktual_terverifikasi_dinas_teknis = rekap_new[(rekap_new['Status Permohonan']=="Selesai Verifikasi")&
                                                    (rekap_new['Tahun']==str(this_year))]

    berkas_aktual_terverifikasi_dinas_teknis_und7 = berkas_aktual_terverifikasi_dinas_teknis['No. Registrasi'][(berkas_aktual_terverifikasi_dinas_teknis['Duration']<=7)|
                                                                                                            (berkas_aktual_terverifikasi_dinas_teknis['Duration'].isna())].nunique()

    berkas_aktual_terverifikasi_dinas_teknis_7to14 = berkas_aktual_terverifikasi_dinas_teknis['No. Registrasi'][(berkas_aktual_terverifikasi_dinas_teknis['Duration']>7)&
                                                                                                                (berkas_aktual_terverifikasi_dinas_teknis['Duration']<=14)].nunique()

    berkas_aktual_terverifikasi_dinas_teknis_ov14 = berkas_aktual_terverifikasi_dinas_teknis['No. Registrasi'][(berkas_aktual_terverifikasi_dinas_teknis['Duration']>14)].nunique()
    # ----------------------------------------------------------------------------------------------------------------------------
    berkas_terbit_pbg = rekap_new[((rekap_new['Status']=='Menunggu Pengambilan Izin')|
                                (rekap_new['Status']=='Penugasan Inpeksi')|
                                (rekap_new['Status'].isna()))&
                                (rekap_new['Tahun']==str(this_year))]

    berkas_terbit_pbg_und7 = berkas_terbit_pbg['No. Registrasi'][(berkas_terbit_pbg['Duration'].isna())|
                                                                (berkas_terbit_pbg['Duration']<=7)].nunique()

    berkas_terbit_pbg_7to14 = berkas_terbit_pbg['No. Registrasi'][(berkas_terbit_pbg['Duration']>7)&
                                                                (berkas_terbit_pbg['Duration']<=14)].nunique()

    berkas_terbit_pbg_ov14 = berkas_terbit_pbg['No. Registrasi'][(berkas_terbit_pbg['Duration']>14)].nunique()
    # ----------------------------------------------------------------------------------------------------------------------------
    proses_penerbitan_concat = pd.concat([berkas_aktual_terverifikasi_dinas_teknis,berkas_terbit_pbg])
    proses_penerbitan = proses_penerbitan_concat.drop_duplicates(keep=False)

    proses_penerbitan_und7 = proses_penerbitan['No. Registrasi'][(proses_penerbitan['Duration'].isna())|
                                                                (proses_penerbitan['Duration']<=7)].nunique()

    proses_penerbitan_7to14 = proses_penerbitan['No. Registrasi'][(proses_penerbitan['Duration']>7)&
                                                                (proses_penerbitan['Duration']<=14)].nunique()

    proses_penerbitan_ov14 = proses_penerbitan['No. Registrasi'][(proses_penerbitan['Duration']>14)].nunique()
    # ----------------------------------------------------------------------------------------------------------------------------
    terproses_di_ptsp = rekap_new[((rekap_new['Status']=='Menunggu Pembayaran Retribusi')|
                                (rekap_new['Status']=='Menunggu Validasi Retribusi')|
                                (rekap_new['Status']=='Pengiriman SKRD'))&
                                (rekap_new['Tahun']==str(this_year))]

    terproses_di_ptsp_und7 = terproses_di_ptsp['No. Registrasi'][(terproses_di_ptsp['Duration'].isna())|
                                                                (terproses_di_ptsp['Duration']<=7)].nunique()

    terproses_di_ptsp_7to14 = terproses_di_ptsp['No. Registrasi'][(terproses_di_ptsp['Duration']>7)&
                                                                (terproses_di_ptsp['Duration']<=14)].nunique()

    terproses_di_ptsp_ov14 = terproses_di_ptsp['No. Registrasi'][(terproses_di_ptsp['Duration']>14)].nunique()
    # ----------------------------------------------------------------------------------------------------------------------------
    terproses_di_dputr_concat = pd.concat([proses_penerbitan,terproses_di_ptsp])
    terproses_di_dputr = terproses_di_dputr_concat.drop_duplicates(keep=False)

    terproses_di_dputr_und7 = terproses_di_dputr['No. Registrasi'][(terproses_di_dputr['Duration'].isna())|
                                                                (terproses_di_dputr['Duration']<=7)].nunique()

    terproses_di_dputr_7to14 = terproses_di_dputr['No. Registrasi'][(terproses_di_dputr['Duration']>7)&
                                                                    (terproses_di_dputr['Duration']<=14)].nunique()

    terproses_di_dputr_ov14 = terproses_di_dputr['No. Registrasi'][(terproses_di_dputr['Duration']>14)].nunique()
    

    return (
        berkas_aktual_belum_terverifikasi_und7,
        berkas_aktual_belum_terverifikasi_7to14,
        berkas_aktual_belum_terverifikasi_ov14,
        potensi_besar_und7,
        potensi_besar_7to14,
        potensi_besar_ov14,
        potensi_kecil_und7,
        potensi_kecil_7to14,
        potensi_kecil_ov14,
        berkas_aktual_terverifikasi_dinas_teknis_und7,
        berkas_aktual_terverifikasi_dinas_teknis_7to14,
        berkas_aktual_terverifikasi_dinas_teknis_ov14,
        berkas_terbit_pbg_und7,
        berkas_terbit_pbg_7to14,
        berkas_terbit_pbg_ov14,
        proses_penerbitan_und7,
        proses_penerbitan_7to14,
        proses_penerbitan_ov14,
        terproses_di_ptsp_und7,
        terproses_di_ptsp_7to14,
        terproses_di_ptsp_ov14,
        terproses_di_dputr_und7,
        terproses_di_dputr_7to14,
        terproses_di_dputr_ov14
        )

@macetplan.route('/', methods=['GET'])
def get_data():
    (
        berkas_aktual_belum_terverifikasi_und7,
        berkas_aktual_belum_terverifikasi_7to14,
        berkas_aktual_belum_terverifikasi_ov14,
        potensi_besar_und7,
        potensi_besar_7to14,
        potensi_besar_ov14,
        potensi_kecil_und7,
        potensi_kecil_7to14,
        potensi_kecil_ov14,
        berkas_aktual_terverifikasi_dinas_teknis_und7,
        berkas_aktual_terverifikasi_dinas_teknis_7to14,
        berkas_aktual_terverifikasi_dinas_teknis_ov14,
        berkas_terbit_pbg_und7,
        berkas_terbit_pbg_7to14,
        berkas_terbit_pbg_ov14,
        proses_penerbitan_und7,
        proses_penerbitan_7to14,
        proses_penerbitan_ov14,
        terproses_di_ptsp_und7,
        terproses_di_ptsp_7to14,
        terproses_di_ptsp_ov14,
        terproses_di_dputr_und7,
        terproses_di_dputr_7to14,
        terproses_di_dputr_ov14    
     )= fetch_data()
    response_data = {
          "berkas_aktual_belum_terverifikasi_und7" : berkas_aktual_belum_terverifikasi_und7,
          "berkas_aktual_belum_terverifikasi_7to14" : berkas_aktual_belum_terverifikasi_7to14,
          "berkas_aktual_belum_terverifikasi_ov14" : berkas_aktual_belum_terverifikasi_ov14,
          
          "potensi_besar_und7" : potensi_besar_und7,
          "potensi_besar_7to14" : potensi_besar_7to14,
          "potensi_besar_ov14" : potensi_besar_ov14,
          "potensi_kecil_und7" : potensi_kecil_und7,
          "potensi_kecil_7to14" : potensi_kecil_7to14,
          "potensi_kecil_ov14" : potensi_kecil_ov14,
          "berkas_aktual_terverifikasi_dinas_teknis_und7" : berkas_aktual_terverifikasi_dinas_teknis_und7,
          "berkas_aktual_terverifikasi_dinas_teknis_7to14" : berkas_aktual_terverifikasi_dinas_teknis_7to14,
          "berkas_aktual_terverifikasi_dinas_teknis_ov14" : berkas_aktual_terverifikasi_dinas_teknis_ov14,
          "berkas_terbit_pbg_und7" : berkas_terbit_pbg_und7,
          "berkas_terbit_pbg_7to14" : berkas_terbit_pbg_7to14,
          "berkas_terbit_pbg_ov14" : berkas_terbit_pbg_ov14,
          "proses_penerbitan_und7" : proses_penerbitan_und7,
          "proses_penerbitan_7to14" : proses_penerbitan_7to14,
          "proses_penerbitan_ov14" : proses_penerbitan_ov14,
          "terproses_di_ptsp_und7" : terproses_di_ptsp_und7,
          "terproses_di_ptsp_7to14" : terproses_di_ptsp_7to14,
          "terproses_di_ptsp_ov14" : terproses_di_ptsp_ov14,
          "terproses_di_dputr_und7" : terproses_di_dputr_und7,
          "terproses_di_dputr_7to14" : terproses_di_dputr_7to14,
          "terproses_di_dputr_ov14" : terproses_di_dputr_ov14
     }
     
    return jsonify(response_data)

app.register_blueprint(macetplan, url_prefix='/api/macet-plan/')

if __name__ == '__main__':
    app.run(debug=False)