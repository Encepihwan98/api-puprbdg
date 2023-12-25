from flask import Flask, Blueprint, jsonify, request
import gspread
import pandas as pd
from datetime import date, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

rekap_pbg2 = Blueprint('rekap2', __name__)

# Load the Google Sheets service account credentials
sa = gspread.service_account(filename='sibedaspbg-logbook-cab4b99bdcae.json')

# Open the spreadsheet
sp = sa.open('rekap pbg')
sh = sp.worksheet('rekap new')

# Fetch data from the spreadsheet and process it
def fetch_data(page, items_per_page, tahun=None, potensi=None, status=None, filtered=None, search=None):
    data = sh.get_all_values()[1:]
    columns = sh.get_all_values()[0]
    logb = pd.DataFrame(data, columns=columns)

    # Apply filter by year if 'tahun' parameter is provided
    if tahun:
        logb = logb[logb['Tahun'] == tahun]

     # Apply filter by 'besar' (large) or 'kecil' (small) if 'potensi' parameter is provided
    if potensi:
        if potensi.lower() == 'besar':
            logb = logb[logb['Capitals'].astype(float) > 50000000]
        elif potensi.lower() == 'kecil':
            logb = logb[logb['Capitals'].astype(float) <= 50000000]

    # Apply filter by 'status' if 'status' parameter is provided
    if status:
        status_values = status.split(',')  # Split the comma-separated values into a list
        logb = logb[logb['Status'].isin(status_values)]

    if filtered:
        if filtered.lower() == 'berkas_aktual_belum_terverifikasi' :
            logb = logb[logb['berkas_aktual_belum_terverifikasi'] == 'True']
        if filtered.lower() == 'berkas_aktual_belum_terverifikasi14' :
            logb = logb[logb['berkas_aktual_belum_terverifikasi'] == 'True']
            logb = logb[logb['Dur_Cat'] == '>14']
        if filtered.lower() == 'berkas_aktual_terverifikasi_dinas_teknis' :
            logb = logb[logb['berkas_aktual_terverifikasi_dinas_teknis'] == 'True']
        if filtered.lower() == 'berkas_aktual_terverifikasi_dinas_teknis14' :
            logb = logb[logb['berkas_aktual_terverifikasi_dinas_teknis'] == 'True']
            logb = logb[logb['Dur_Cat'] == '>14']
        if filtered.lower() == 'berkas_terbit_pbg' :
            logb = logb[logb['berkas_terbit_pbg'] == 'True']
        if filtered.lower() == 'proses_penerbitan' :
            logb = logb[logb['proses_penerbitan'] == 'True']
        if filtered.lower() == 'proses_penerbitan14' :
            logb = logb[logb['proses_penerbitan'] == 'True']
            logb = logb[logb['Dur_Cat'] == '>14']
        if filtered.lower() == 'terproses_di_ptsp' :
            logb = logb[logb['terproses_di_ptsp'] == 'True']
        if filtered.lower() == 'terproses_di_ptsp14' :
            logb = logb[logb['terproses_di_ptsp'] == 'True']
            logb = logb[logb['Dur_Cat'] == '>14']
        if filtered.lower() == 'terproses_di_dputr' :
            logb = logb[logb['terproses_di_dputr'] == 'True']
        if filtered.lower() == 'terproses_di_dputr14' :
            logb = logb[logb['terproses_di_dputr'] == 'True']
            logb = logb[logb['Dur_Cat'] == '>14']
        if filtered.lower() == 'potensi_kecil14' :
            logb = logb[logb['potensi_kecil'] == 'True']
            logb = logb[logb['Dur_Cat'] == '>14']
        if filtered.lower() == 'potensi_besar14' :
            logb = logb[logb['potensi_besar'] == 'True']
            logb = logb[logb['Dur_Cat'] == '>14']

    if search:
        logb = logb[logb.apply(lambda row: any(row.astype(str).str.contains(search, case=False)), axis=1)]
        # logb = logb[logb.apply(lambda row: any([str(val).lower().find(search.lower()) != -1 for val in row]), axis=1)]
        


    # Paginasi
    start_index = (page - 1) * items_per_page
    end_index = page * items_per_page
    paginated_data = logb.iloc[start_index:end_index]

    return paginated_data, logb.shape[0]

@rekap_pbg2.route('/', methods=['GET'])
def get_data():
    # Mendapatkan nomor halaman dan item per halaman dari permintaan
    page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('items_per_page', 10))

     # Get the 'tahun' (year) filter parameter from the request
    tahun = request.args.get('tahun')

    # Get the 'potensi' (large) or 'kecil' (small) filter parameter from the request
    potensi = request.args.get('potensi')

    # Get the 'status' filter parameter from the request
    status = request.args.get('status')

    # Get the 'search' parameter from the request
    search = request.args.get('search')

    #filtered
    filtered = request.args.get('filtered')


    data , total_rows = fetch_data(page, items_per_page, tahun=tahun, potensi=potensi, status=status, search=search, filtered=filtered)

        # Calculate total pages
    total_pages = (total_rows // items_per_page) + (1 if total_rows % items_per_page > 0 else 0)

    response = {
        'data': data.to_dict(orient='records'),
        'total_page': total_pages,
        'current_page': page
    }


    return jsonify(response)

app.register_blueprint(rekap_pbg2, url_prefix='/api/rekap-pbg2')

if __name__ == '__main__':
    app.run(debug=False)
