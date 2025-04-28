from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

GEOJSON_FOLDER = os.path.join('static', 'geojson')

@app.route('/')
def index():
    geojson_files = [f for f in os.listdir(GEOJSON_FOLDER) if f.endswith('.geojson')]
    return render_template('index.html', geojson_files=geojson_files)

@app.route('/geojson/<filename>')
def geojson(filename):
    return send_from_directory(GEOJSON_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)