from flask import Flask
from flask_cors import CORS
from apiLacak import lacak_bp
from rekapPBG import rekap_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(lacak_bp, url_prefix='/api/lacak')
# app.register_blueprint(rekap_bp, url_prefix='/api/rekap-pbg')

if __name__ == '__main__':
    app.run(debug=False)
