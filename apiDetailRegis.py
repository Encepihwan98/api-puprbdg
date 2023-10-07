from flask import Flask, Blueprint, jsonify, request
import gspread
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

detail_regis = Blueprint('detail_regis', __name__)

# Load the Google Sheets service account credentials
sa = gspread.service_account(filename='sibedaspbg-logbook-cab4b99bdcae.json')

# Open the spreadsheet
sp = sa.open('rekap pbg')
sh = sp.worksheet('logbook')

# Fetch data from the spreadsheet and process it
def fetch_data_by_no_registrasi(no_registrasi):
    data = sh.get_all_values()[1:]
    columns = sh.get_all_values()[0]
    logb = pd.DataFrame(data, columns=columns)
    
    if no_registrasi in logb['No. Registrasi'].values:
        result = logb[logb['No. Registrasi'] == no_registrasi]
        return result
    else:
        return None

@detail_regis.route('/', methods=['GET'])
def get_data():
    data = fetch_data()
    return jsonify(data.to_dict(orient='records'))

@detail_regis.route('/search', methods=['GET'])
def search_data():
    no_registrasi = request.args.get('no_registrasi')
    if no_registrasi:
        result = fetch_data_by_no_registrasi(no_registrasi)
        if result is not None:
            return jsonify(result.to_dict(orient='records'))
        else:
            return "Nomor Registrasi tidak ditemukan."
    else:
        return "Masukkan Nomor Registrasi untuk pencarian."

app.register_blueprint(detail_regis, url_prefix='/api/detail')

if __name__ == '__main__':
    app.run(debug=False)
