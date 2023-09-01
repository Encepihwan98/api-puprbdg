# from flask import Blueprint, jsonify
# import requests
# import pandas as pd
# from bs4 import BeautifulSoup

# lacak_bp = Blueprint('lacak', __name__)

# def scrape_data(nomor):
#     s = requests.Session()

#     home_url = 'https://simbg.pu.go.id/Informasi'
#     home_resp = s.get(home_url, verify=False)
#     soup = BeautifulSoup(home_resp.text, 'html.parser')
#     csrf_test_name = soup.find('input', {'type': 'csrf_test_name'})

#     url = f'https://simbg.pu.go.id/Informasi/Lacak/{nomor}?csrf_test_name={csrf_test_name}'
#     resp = requests.get(url, verify=False)
#     html = '<table> ' + resp.text + ' </table>'

#     df = pd.read_html(html)[0].fillna('')
#     df.columns = ['No.', 'Modul', 'Tanggal', 'Keterangan']
#     return df.to_dict(orient='records')

# @lacak_bp.route('/<string:nomor>', methods=['GET'])
# def get_lacak_data(nomor):
#     data = scrape_data(nomor)
#     return jsonify(data)


from flask import Blueprint, jsonify
import requests
import pandas as pd
from bs4 import BeautifulSoup

lacak_bp = Blueprint("lacak", __name__)


def scrape_data(nomor):
    try:
        s = requests.Session()

        home_url = "https://simbg.pu.go.id/Informasi"
        home_resp = s.get(home_url, verify=False)
        home_resp.raise_for_status()  # Raise an exception if the request was not successful

        soup = BeautifulSoup(home_resp.text, "html.parser")
        csrf_test_name = soup.find("input", {"type": "csrf_test_name"})

        url = f"https://simbg.pu.go.id/Informasi/Lacak/{nomor}?csrf_test_name={csrf_test_name}"
        resp = requests.get(url, verify=False)
        resp.raise_for_status()

        html = "<table> " + resp.text + " </table>"

        df = pd.read_html(html)[0].fillna('')
        df.columns = ['No.', 'Modul', 'Tanggal', 'Keterangan']

        return df.to_dict(orient="records")

    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        return {"error": "Network error occurred"}

    except Exception as e:
        # Handle other unexpected errors
        return {"error": str(e)}


@lacak_bp.route("/<string:nomor>", methods=["GET"])
def get_lacak_data(nomor):
    data = scrape_data(nomor)

    if "error" in data:
        return jsonify(data), 500  # HTTP status code 500 for internal server error

    return jsonify(data)


if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    app.register_blueprint(lacak_bp, url_prefix="/lacak")

    app.run(debug=False)
