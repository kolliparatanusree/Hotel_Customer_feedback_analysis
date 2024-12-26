from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pandas as pd
from textblob import TextBlob
from transformers import pipeline
from datetime import datetime
import os
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import pywhatkit as kit

app = Flask(__name__)
app.secret_key = 'your_secret_key'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'  # Change to your MySQL host if it's not localhost
app.config['MYSQL_USER'] = ''  # Your MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Your MySQL password
app.config['MYSQL_DB'] = 'feedback'  # Your database name

# Initialize MySQL
mysql = MySQL(app)

# Summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Sentiment analysis function
def analyze_sentiment(review_text):
    analysis = TextBlob(review_text)
    sentiment = analysis.sentiment.polarity
    if sentiment > 0:
        return 'Positive'
    elif sentiment < 0:
        return 'Negative'
    return 'Neutral'

# Review summary function
def summarize_review(review):
    if len(review) < 100:
        return review
    return summarizer(review, max_length=50, min_length=10, do_sample=False)[0]['summary_text']

# WhatsApp alert function
def send_whatsapp_alert(phone_number, message):
    try:
        current_time = datetime.now()
        hour = current_time.hour
        minute = current_time.minute + 2  # Schedule 2 minutes later

        kit.sendwhatmsg(phone_number, message, hour, minute)
        print("WhatsApp message scheduled successfully!")
    except Exception as e:
        print(f"Failed to send WhatsApp message: {str(e)}")

# Load or initialize dataset
file_path = 'hotel_review2.csv'
if os.path.exists(file_path):
    df = pd.read_csv(file_path, parse_dates=['Date'])
else:
    df = pd.DataFrame(columns=['Review', 'Rating', 'Sentiment1', 'Date', 'Summary'])

if 'Sentiment1' not in df.columns:
    df['Sentiment1'] = df['Review'].apply(lambda x: analyze_sentiment(x) if pd.notnull(x) else 'Neutral')

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Customer page
@app.route('/customer')
def customer():
    return render_template('index.html')

# Admin page
@app.route('/admin')
def admin_page():
    return render_template('admin.html')

# Admin login
@app.route('/admin_login', methods=['POST'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('admin.html', error="Invalid username or password. Please try again.")

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin2.html')

@app.route('/view_page')
def view_page():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    managers = cursor.fetchall()
    cursor.close()
    return render_template('view.html', managers=managers)

@app.route('/register_manager', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/register_manager', methods=['POST'])
def register_manager():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        return render_template('register.html', error="Passwords do not match!")

    cursor = mysql.connection.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            return render_template('register.html', error="Username already exists!")

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cursor.close()
        return render_template('register.html', success=True)

    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return render_template('register.html', error=f"Error: {str(e)}")

@app.route('/delete_manager/<int:manager_id>', methods=['GET'])
def delete_manager(manager_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (manager_id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('view_page'))
    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return f"Error: {str(e)}"

@app.route('/submit_review', methods=['POST'])
def submit_review():
    try:
        data = request.get_json()
        review_text = data.get('review')
        rating = data.get('rating')

        if not review_text or not rating:
            return jsonify({'error': 'Review and Rating are required.'}), 400

        # Analyze sentiment and summarize review
        sentiment = analyze_sentiment(review_text)
        current_date = datetime.now()
        summary = summarize_review(review_text)

        # Save to CSV
        new_data = pd.DataFrame([{
            'Review': review_text,
            'Rating': rating,
            'Sentiment1': sentiment,
            'Date': current_date,
            'Summary': summary,
        }])

        global df
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(file_path, index=False)

        # Send WhatsApp alert
        phone_number = "+918978821139"  # Replace with recipient's number
        alert_message = (
            f"New Review Submitted!\n"
            f"Rating: {rating}\n"
            f"Sentiment: {sentiment}\n"
            f"Summary: {summary}"
        )
        send_whatsapp_alert(phone_number, alert_message)

        return jsonify({
            'message': 'Review submitted successfully!',
            'sentiment': sentiment,
            'date': current_date,
            'summary': summary,
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/manager')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and user[2] == password:
        session['logged_in'] = True
        return redirect(url_for('month_selection'))
    return render_template('login.html', error="Invalid credentials. Please try again.")

@app.route('/month_selection')
def month_selection():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    max_date = datetime.now().strftime('%Y-%m')
    return render_template('month_selection.html', max_date=max_date)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
