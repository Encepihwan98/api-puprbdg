from flask import Flask, Blueprint, jsonify
import gspread
import pandas as pd
from datetime import date, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

nilai_ret = Blueprint('nilai_ret', __name__)

# Load the Google Sheets service account credentials
sa = gspread.service_account(filename='sibedaspbg-logbook-cab4b99bdcae.json')

# Open the spreadsheet
sp = sa.open('rekap pbg')
sh = sp.worksheet('rekap new')

# Fetch data from the spreadsheet and process it
def fetch_data():
    data = sh.get_all_values()[1:]
    # Mengonversi nilai-nilai dari row[33] menjadi float
    nilai_retribusi = [float(row[33]) for row in data]
    
    # Kelompokkan data menjadi dua kelompok (dibawah 25 juta dan diatas 25 juta)
    nonUsahaDibawah = [nilai for nilai in nilai_retribusi if nilai < 25000000]
    nonUsahaDiatas = [nilai for nilai in nilai_retribusi if nilai >= 25000000 and nilai < 50000000]
    
    usahaDibawah = [nilai for nilai in nilai_retribusi if nilai > 50000000 and nilai < 75000000 ]
    usahaDiatas = [nilai for nilai in nilai_retribusi if nilai  and nilai > 50000000]
    # Jumlahkan data yang dibawah 25 juta
    totalNonUsahaDibawah = sum(nonUsahaDibawah)
    totalNonUsahaDiatas = sum(nonUsahaDiatas)
    totalUsahaDibawah = sum(usahaDibawah)   
    totalUsahaDiatas = sum(usahaDiatas)
    countUsahaDibawah = len(usahaDibawah)
    countUsahaDiatas = len(usahaDiatas)
    countNonUsahaDibawah = len(nonUsahaDibawah)
    countNonUsahaDiatas = len(nonUsahaDiatas)

    return totalUsahaDibawah, totalUsahaDiatas ,totalNonUsahaDiatas, totalNonUsahaDibawah, countUsahaDibawah, countUsahaDiatas, countNonUsahaDibawah, countNonUsahaDiatas


@nilai_ret.route('/', methods=['GET'])
def get_data():
    totalUsahaDibawah, totalUsahaDiatas ,totalNonUsahaDiatas, totalNonUsahaDibawah, countUsahaDibawah, countUsahaDiatas, countNonUsahaDibawah, countNonUsahaDiatas = fetch_data()
    response_data = {
        "nonUsahaDibawah": totalNonUsahaDibawah,
        "nonUsahaDiatas": totalNonUsahaDiatas,
        "usahaDibawah": totalUsahaDibawah,
        "usahaDiatas" : totalUsahaDiatas,
        "countUsahaDibawah" : countUsahaDibawah,
        "countUsahaDiatas" : countUsahaDiatas,
        "countNonUsahaDibawah" : countNonUsahaDibawah,
        "countNonUsahaDiatas" : countNonUsahaDiatas
    }
    
    return jsonify(response_data)

app.register_blueprint(nilai_ret, url_prefix='/api/nilai-retribusi/')

if __name__ == '__main__':
    app.run(debug=False)
