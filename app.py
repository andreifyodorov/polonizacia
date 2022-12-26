#!.venv/bin/python3

from flask import Flask, send_from_directory, request
import polonizacyia

app = Flask(__name__, static_folder="")

@app.route("/", methods=['GET'])
def index_page():
    return app.send_static_file('index.html')

@app.route('/texts/<path:path>')
def send_texts(path):
    return send_from_directory('texts', path)

@app.route("/trans", methods=['POST'])
def trans():
    return polonizacyia.process([request.get_json()])


if __name__ == '__main__':
    app.run(debug=True, port=8080)
