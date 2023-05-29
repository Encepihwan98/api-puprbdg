from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class SIMBG(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('total_berkas', type=int, required=True)
        parser.add_argument('berkas_terbit_2022', type=int, required=True)
        parser.add_argument('total_berkas_2023', type=int, required=True)
        parser.add_argument('berkas_aktual_belum_terverifikasi', type=int, required=True)
        parser.add_argument('berkas_aktual_terverifikasi_dinas_teknis', type=int, required=True)
        parser.add_argument('terproses_di_ptsp', type=int, required=True)
        parser.add_argument('berkas_terbit_pbg', type=int, required=True)

        args = parser.parse_args()

        return {
            'Total Berkas': args['total_berkas'],
            'Berkas Terbit 2022': args['berkas_terbit_2022'],
            'Total Berkas 2023': args['total_berkas_2023'],
            'Berkas Aktual Belum Terverifikasi': args['berkas_aktual_belum_terverifikasi'],
            'Berkas Aktual Terverifikasi Dinas Teknis': args['berkas_aktual_terverifikasi_dinas_teknis'],
            'Terproses di PTSP': args['terproses_di_ptsp'],
            'Berkas Terbit PBG': args['berkas_terbit_pbg']
        }

api.add_resource(SIMBG, "/simbg")

if __name__ == "__main__":
    app.run(debug=True)