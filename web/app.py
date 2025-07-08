# web/app.py
import os
import pandas as pd
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Make sure it matches your actual file
CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'emotion_log.csv'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    if not os.path.exists(CSV_PATH):
        return jsonify([])

    df = pd.read_csv(CSV_PATH)
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
