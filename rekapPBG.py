# from flask import Blueprint, jsonify
# import gspread
# import pandas as pd
# from flask_cors import CORS

# rekap_bp = Blueprint('rekap', __name__)
# CORS(rekap_bp)  # Enable CORS for this Blueprint

# # Load the Google Sheets service account credentials
# try:
#     gc = gspread.service_account(filename='sibedaspbg-logbook-cab4b99bdcae.json')
#     sh = gc.open('rekap pbg').worksheet('Data')
# except Exception as e:
#     print(f"Error loading Google Sheets: {str(e)}")
#     sh = None

# # Fetch data from the spreadsheet and process it
# def fetch_data():
#     if sh:
#         try:
#             data = sh.get_all_values()[1:]
#             columns = sh.get_all_values()[0]
#             logbook = pd.DataFrame(data, columns=columns)
#             logbook['Tahun'] = logbook[['TAHUN TERBIT', 'Tahun Berjalan']].max(axis=1)
#             logbook = logbook.drop(columns=['2/8', 'TAHUN TERBIT', 'Tahun Berjalan'])
#             logbook = logbook[logbook['Tahun'] != '']
#             return logbook
#         except Exception as e:
#             print(f"Error fetching data from Google Sheets: {str(e)}")
#             return pd.DataFrame()
#     else:
#         return pd.DataFrame()

# @rekap_bp.route('/', methods=['GET'])
# def get_data():
#     data = fetch_data()
#     return jsonify(data.to_dict(orient='records'))


from flask import Blueprint, jsonify
import gspread
import pandas as pd
from datetime import date, timedelta
from flask_cors import CORS

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