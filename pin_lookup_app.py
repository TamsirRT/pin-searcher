from flask import Flask, render_template, request, jsonify, session
import requests
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Supabase config
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
TEACHER_PASSWORD = os.environ.get('TEACHER_PASSWORD', 'teacher123')

# Headers for Supabase REST API
def get_headers():
    return {
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'apikey': SUPABASE_KEY
    }

def init_supabase():
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError('SUPABASE_URL and SUPABASE_KEY environment variables are required')

@app.route('/')
def index():
    if 'logged_in' in session:
        return render_template('lookup.html')
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def login():
    password = request.json.get('password', '')
    
    if password != TEACHER_PASSWORD:
        return jsonify({'error': 'Incorrect password'}), 401
    
    try:
        # Test connection to Supabase
        url = f'{SUPABASE_URL}/rest/v1/students?select=id&limit=1'
        response = requests.get(url, headers=get_headers())
        
        if response.status_code != 200:
            return jsonify({'error': 'Database connection error'}), 400
        
        session['logged_in'] = True
        session['login_time'] = datetime.now().isoformat()
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 400

@app.route('/api/search', methods=['GET'])
def search():
    if 'logged_in' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    query = request.args.get('q', '').lower().strip()
    
    if not query or len(query) < 1:
        return jsonify([])
    
    try:
        # Fetch all students
        url = f'{SUPABASE_URL}/rest/v1/students?select=id,last_name,first_name,grade_level,pin'
        response = requests.get(url, headers=get_headers())
        
        if response.status_code != 200:
            return jsonify({'error': 'Database error'}), 400
        
        results = []
        for student in response.json():
            first_name = (student.get('first_name') or '').lower()
            last_name = (student.get('last_name') or '').lower()
            full_name = f"{student.get('first_name', '')} {student.get('last_name', '')}".lower()
            
            if (query in first_name or 
                query in last_name or 
                query in full_name):
                results.append({
                    'id': student.get('id'),
                    'first_name': student.get('first_name'),
                    'last_name': student.get('last_name'),
                    'full_name': f"{student.get('first_name', '')} {student.get('last_name', '')}",
                    'grade_level': student.get('grade_level'),
                    'pin': student.get('pin')
                })
        
        return jsonify(results[:20])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    try:
        init_supabase()
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ValueError as e:
        print(f'Error: {e}')
        print('Please set SUPABASE_URL and SUPABASE_KEY environment variables')
