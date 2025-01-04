from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = '../data/experts.db'

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        search_query = f"""
        SELECT * FROM expert_profiles
        WHERE name LIKE ?
        OR label LIKE ?
        OR profile LIKE ?
        """
        cursor.execute(search_query, (f'%{query}%', f'%{query}%', f'%{query}%'))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Traditional Search API is running!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)