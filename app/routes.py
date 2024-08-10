from flask import render_template, request, flash, redirect, url_for, jsonify, session
import requests
from app import app

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Validation
        if not email or not password:
            flash('All fields are required!', 'error')
            return render_template('login.html')
        
        # Send data to the server
        data = {
            "email": email,
            "password": password
        }
        try:
            response = requests.post("http://199.247.17.44:3001/users/verify", json=data)
            if response.status_code == 200:
                # Assuming the API returns a success status and possibly a message
                flash('Login successful! Please enter your OTP.', 'success')
                session['email'] = email
                session['password'] = password
                return redirect(url_for('otp'))
            else:
                flash(f'Login failed: {response.status_code} - {response.text}', 'error')
        except requests.exceptions.RequestException as e:
            flash(f'Server error: {e}', 'error')
        
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/otp', methods=['GET', 'POST'])
def otp():
    if request.method == 'POST':
        otp = request.form['otp']
        email = session.get('email')
        password = session.get('password')
        
        if not otp or not email or not password:
            flash('OTP and login credentials are required!', 'error')
            return render_template('otp.html')
        
        # Send data to the server
        data = {
            "email": email,
            "password": password,
            "otp": otp
        }
        try:
            response = requests.post("http://199.247.17.44:3001/auth/login", json=data)
            if response.status_code == 201:
                # Check if the response contains the accessToken
                response_json = response.json()
                access_token = response_json.get('accessToken')  
                
                if access_token:
                    # Store access token in the session (or use secure cookies)
                    session['jwt_token'] = access_token
                    flash('OTP verification successful! You are now logged in.', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Access token not received.', 'error')
            else:
                flash(f'OTP verification failed: {response.status_code} - {response.text}', 'error')
        except requests.exceptions.RequestException as e:
            flash(f'Server error: {e}', 'error')
        
        return redirect(url_for('otp'))
    
    return render_template('otp.html')



@app.route('/dashboard')
def dashboard():
    jwt_token = session['jwt_token']
    if not jwt_token:
        flash('You are not authorized to access this page. Please log in.', 'error')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))
