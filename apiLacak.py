from flask import Flask, Blueprint, jsonify
import requests
import pandas as pd
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

lacak_bp = Blueprint("lacak", __name__)

def scrape_data(nomor):
    s = requests.Session()

    home_url = 'https://simbg.pu.go.id/Informasi'
    home_resp = s.get(home_url, verify=False)
    soup = BeautifulSoup(home_resp.text, 'lxml')  # Menggunakan 'lxml' sebagai parser
    csrf_test_name = soup.find('input', {'type': 'csrf_test_name'})

    url = f'https://simbg.pu.go.id/Informasi/Lacak/{nomor}?csrf_test_name={csrf_test_name}'
    resp = requests.get(url, verify=False)
    html = '<table> ' + resp.text + ' </table>'

    soup = BeautifulSoup(html, 'lxml')  # Menggunakan 'lxml' sebagai parser
    table = soup.find('table')
    df = pd.read_html(str(table))[0].fillna('')

    df.columns = ['No.', 'Modul', 'Tanggal', 'Keterangan']
    return df.to_dict(orient='records')

@lacak_bp.route('/<string:nomor>', methods=['GET'])
def get_lacak_data(nomor):
    data = scrape_data(nomor)
    return jsonify(data)

app.register_blueprint(lacak_bp, url_prefix='/api/lacak')

if __name__ == '__main__':
    app.run(debug=False)
