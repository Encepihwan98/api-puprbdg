from flask import Flask, Blueprint, jsonify, request
import gspread
import pandas as pd
from datetime import date, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

rekap_bp = Blueprint('rekap', __name__)

# Load the Google Sheets service account credentials
sa = gspread.service_account(filename='sibedaspbg-logbook-cab4b99bdcae.json')

# Open the spreadsheet
sp = sa.open('rekap pbg')
sh = sp.worksheet('rekap new')

# Fetch data from the spreadsheet and process it
def fetch_data(page, items_per_page):
    data = sh.get_all_values()[1:]
    columns = sh.get_all_values()[0]
    logb = pd.DataFrame(data, columns=columns)

    # Paginasi
    start_index = (page - 1) * items_per_page
    end_index = page * items_per_page
    paginated_data = logb.iloc[start_index:end_index]

    return paginated_data

@rekap_bp.route('/', methods=['GET'])
def get_data():
    # Mendapatkan nomor halaman dan item per halaman dari permintaan
    page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('items_per_page', 10))

    data = fetch_data(page, items_per_page)
    return jsonify(data.to_dict(orient='records'))

app.register_blueprint(rekap_bp, url_prefix='/api/rekap-pbg')

if __name__ == '__main__':
    app.run(debug=False)
