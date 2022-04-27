from flask import Flask
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
from tweet import find_mood

app = Flask(__name__)
# app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, static_folder='./sentiment-app/build', static_url='/')

# @app.after_request
# def set_headers(response):
#     response.headers["Referrer-Policy"] = 'no-referrer'
#     return response

@app.route("/<string:keyword>")
@cross_origin()
def read_item(keyword):
    sent = find_mood(keyword)
    # response = flask.jsonify(sent)
    # sent.headers.add('Access-Control-Allow-Origin', '*')
    return sent

@app.route("/")
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')
