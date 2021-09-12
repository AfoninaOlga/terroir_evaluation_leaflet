from flask import Flask, render_template, json, jsonify

from canton_repository import get_canton_data, get_grape, get_filtered_cantons, get_cantons_by_grape
from evaluation import get_suitability

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def map():
    return render_template('map.html')


@app.route('/canton/<int:code>', methods=['GET'])
def get_data(code):
    data = get_canton_data(code)
    return jsonify(data)


@app.route('/cantons/<int:grape_id>', methods=['GET'])
def get_by_grape(grape_id):
    data = get_cantons_by_grape(grape_id)
    return jsonify(data)



@app.route('/suitability/<int:code>', methods=['GET'])
def get_canton(code):
    data = get_suitability(code)
    return jsonify(data)


@app.route('/grape/<int:code>', methods=['GET'])
def get_variety(code):
    data = get_grape(code)
    return jsonify(data)


@app.route('/filter/<string:filter>/<string:val>', methods=['GET'])
def get_cantons(filter, val):
    data = get_filtered_cantons(filter, val)
    return jsonify(data)


if __name__ == '__main__':
    app.run()
