from flask import Flask
from flask_cors import CORS
from apiLacak import lacak_bp
from apiDetailRegis import detail_regis
from rekapPBG import rekap_bp
from apiNilaiRetribusi import nilai_ret
from scrapingMacetPlan import macetplan

app = Flask(__name__)
CORS(app)

app.register_blueprint(rekap_bp, url_prefix='/api/rekap-pbg/')
app.register_blueprint(nilai_ret, url_prefix='/api/nilai-retribusi')
app.register_blueprint(lacak_bp, url_prefix='/api/lacak')
app.register_blueprint(detail_regis, url_prefix='/api/detail_regis/')
app.register_blueprint(macetplan, url_prefix='/api/macet-plan/')

if __name__ == '__main__':
    app.run(debug=False)

