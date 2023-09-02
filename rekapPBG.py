from flask import Flask, jsonify, Blueprint

app = Flask(_name_)

# Data yang akan digunakan dalam respons
data = {
    "total_berkas": 23,
    "berkas_terbit_last": 13,
    "total_berkas_now": 14,
    "total_berkas_now_perc": 14,
    "berkas_aktual_belum_terverifikasi": 14,
    "berkas_aktual_belum_terverifikasi_perc": 15,
    "potensi_besar": 15,
    "potensi_besar_perc": 16,
}

# Blueprint
rekap_bp = Blueprint('rekap', _name_)

@rekap_bp.route('/', methods=['GET'])
def get_data():
    return jsonify(data)
