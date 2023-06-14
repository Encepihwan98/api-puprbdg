from flask import Flask, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Menambahkan middleware CORS


@app.route("/simbg/coba", methods=["GET"])
def simbg():
    data = {
        "berkas_aktual_belum_terverifikasi": 1491,
        "berkas_aktual_belum_terverifikasi_perc": 76.18804292284108,
        "berkas_aktual_terverifikasi_dinas_teknis": 466,
        "berkas_aktual_terverifikasi_dinas_teknis_perc": 23.811957077158915,
        "berkas_terbit_last": 641,
        "berkas_terbit_pbg": 116,
        "berkas_terbit_pbg_perc": 24.892703862660944,
        "dinas_perizinan": 101,
        "jumlah_permohonan": 3040,
        "potensi_besar": 218,
        "potensi_besar_perc": 14.621059691482227,
        "potensi_kecil": 1273,
        "potensi_kecil_perc": 85.37894030851777,
        "proses_penerbitan": 350,
        "proses_penerbitan_perc": 75.10729613733905,
        "telah_terbit_ditolak": 757,
        "terproses_di_dputr": 249,
        "terproses_di_dputr_perc": 71.14285714285714,
        "terproses_di_ptsp": 101,
        "terproses_di_ptsp_perc": 28.857142857142858,
        "total_berkas": 3040,
        "total_berkas_now": 1957,
        "total_berkas_now_perc": 64.375,
    }
    response = make_response(jsonify({"data": data}), 200)
    response.headers.add("Access-Control-Allow-Origin", "*")  # Mengatur header CORS
    return response


if __name__ == "__main__":
    app.run(debug=False)
