# from flask import Flask, jsonify, make_response
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Menambahkan middleware CORS


# @app.route("/simbg/coba", methods=["GET"])
# def simbg():
#     data = {
#         "berkas_aktual_belum_terverifikasi": 1435,  # sudah
#         "berkas_aktual_belum_terverifikasi_perc": 45,  # sudah
#         "berkas_aktual_terverifikasi_dinas_teknis": 968,  # sudah
#         "berkas_aktual_terverifikasi_dinas_teknis_perc": 55,  # sudah
#         "berkas_terbit_last": 645,  # sudah
#         "berkas_terbit_pbg": 572,  # sudah
#         "berkas_terbit_pbg_perc": 78,  # sudah
#         "dinas_perizinan": 86,
#         "jumlah_permohonan": 3079,
#         "potensi_besar": 55,  # sudah
#         "potensi_besar_perc": 48,  # sudah
#         "potensi_kecil": 1380,  # sudah
#         "potensi_kecil_perc": 52,  # sudah
#         "proses_penerbitan": 396,  # sudah
#         "proses_penerbitan_perc": 22,  # sudah
#         "telah_terbit_ditolak": 780,
#         "terproses_di_dputr": 304,  # sudah
#         "terproses_di_dputr_perc": 82,  # sudah
#         "terproses_di_ptsp": 92,  # sudah
#         "terproses_di_ptsp_perc": 18,  # sudah
#         "total_berkas": 3048,  # sudah
#         "total_berkas_now": 2403,  # sudah
#         "total_berkas_now_perc": 95,  # sudahfd

#         "total_berkas_rp": "31.986.879.472",  # sudah  #done
#         "berkas_terbit_last_year_rp": 8214151978,  # sudah  #done
#         "total_berkas_this_year_rp": 23772727494,  # sudah #done
#         "deviasi_target_potensi_rp": 6901294751, #done
#         "deviasi_target_potensi_perc": 28, #done
#         "berkas_aktual_belum_terverifikasi_rp": 10658604517,  # sudah #done
#         "berkas_aktual_terverifikasi_dinas_teknis_rp": 13114122977,  # sudah #done
#         "potensi_besar_rp": 5101660400,  # sudah #done
#         "potensi_kecil_rp": 5556944117,  # sudah #done
#         "proses_penerbitan_rp": 2842759647,  # sudah #done
#         "berkas_terbit_pbg_rp": 10271363330,  # sudah #done
#         "terproses_di_ptsp_rp": 507818510,  # sudah #done
#         "terproses_di_dputr_rp": 2334941137, #done
#     }
#     response = make_response(jsonify({"data": data}), 200)
#     response.headers.add("Access-Control-Allow-Origin", "*")  # Mengatur header CORS
#     return response


# if __name__ == "__main__":
#     app.run(debug=False)

from flask import Flask
from flask_cors import CORS
from apiLacak import lacak_bp
from rekapPBG import rekap_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(lacak_bp, url_prefix='/api/lacak')
app.register_blueprint(rekap_bp, url_prefix='/api/rekap-pbg')

if __name__ == '__main__':
    app.run(debug=True)

