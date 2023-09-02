from flask import Flask, Blueprint, jsonify
import gspread
import pandas as pd
from datetime import date, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

rekap_bp = Blueprint('rekap', __name__)

# Load the Google Sheets service account credentials
sa = gspread.service_account(filename='sibedaspbg-logbook-cab4b99bdcae.json')

# Open the spreadsheet
sp = sa.open('rekap pbg')
sh = sp.worksheet('Data')

# Fetch data from the spreadsheet and process it
def fetch_data():
    data = sh.get_all_values()[1:]
    columns = sh.get_all_values()[0]
    logb = pd.DataFrame(data, columns=columns)
    tahuns = []
    for tahun, year in zip(logb['TAHUN TERBIT'], logb['Tahun Berjalan']):
        tahuns.append(max(tahun, year))
    logb['Tahun'] = tahuns
    logb = logb[logb['Tahun'] != '']
    logb.drop(columns=['2/8', 'TAHUN TERBIT', 'Tahun Berjalan'], inplace=True)
    return logb

@rekap_bp.route('/', methods=['GET'])
def get_data():
    data = fetch_data()
    return jsonify(data.to_dict(orient='records'))

app.register_blueprint(rekap_bp, url_prefix='/api/rekap-pbg')

if __name__ == '__main__':
    app.run(debug=False)
    