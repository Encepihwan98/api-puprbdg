from flask import Flask, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Menambahkan middleware CORS

@app.route('/simbg/coba', methods=['GET'])
def simbg():
    data = {
        'total_berkas': 2772,
        'berkas_terbit_last': 645, #tahun 2022 
        'total_berkas_now': 2127, #tahun 2023
        'berkas_aktual_belum_terverifikasi': 1401,
        'berkas_aktual_terverifikasi_dinas_teknis': 1371,
        'terproses_di_ptsp': 66,
        'berkas_terbit_pbg': 1089
    }
    response = make_response(jsonify({'data': data}), 200)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Mengatur header CORS
    return response

if __name__ == "__main__":
    app.run()