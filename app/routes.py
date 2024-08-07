from flask import render_template, request, flash, redirect, url_for, jsonify
import requests
from app import app

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required!', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('register.html')

        # Send data to the server
        data = {
            "email": email,
            "userName": username,
            "password": password
        }
        try:
            response = requests.post("http://199.247.17.44:3001/users/register", json=data)
            if response.status_code == 201:
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('register'))
            else:
                flash(f'Registration failed: {response.status_code} - {response.text}', 'error')
        except requests.exceptions.RequestException as e:
            flash(f'Server error: {e}', 'error')
        
        return redirect(url_for('register'))
    
    return render_template('register.html')
