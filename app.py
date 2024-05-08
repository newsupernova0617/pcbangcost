from flask import Flask, render_template, jsonify, request
import sqlite3
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # CORS를 전체 앱에 적용

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/data')
def get_data():
    conn = sqlite3.connect('pc_bangs_info.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, x, y, price FROM pc_bangs")
    pc_bangs = cursor.fetchall()
    conn.close()
    pc_bangs_data = [{'name': row[0], 'x': row[1], 'y': row[2], 'price': row[3]} for row in pc_bangs]
    return jsonify(pc_bangs_data)

@app.route('/update-price', methods=['POST'])
def update_price():
    data = request.json
    conn = sqlite3.connect('pc_bangs_info.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE pc_bangs SET price = ? WHERE name = ?", (data['newPrice'], data['name']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 
