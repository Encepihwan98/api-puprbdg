import requests
import json

BASE = "http://127.0.0.1:5000/"

params = {
    'total_berkas': 2772,
    'berkas_terbit_2022': 645,
    'total_berkas_2023': 2127,
    'berkas_aktual_belum_terverifikasi': 1401,
    'berkas_aktual_terverifikasi_dinas_teknis': 1371,
    'terproses_di_ptsp': 66,
    'berkas_terbit_pbg': 1089
}

headers = {'Content-Type': 'application/json'}
data = json.dumps(params)

response = requests.get(BASE + "simbg", data=data, headers=headers)
print(response.json())