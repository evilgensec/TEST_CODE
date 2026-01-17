import os
import sqlite3
from flask import Flask, request, render_template_string

# CRITICAL: Hardcoded Secrets (Triggers Secret Scanner)
AWS_ACCESS_KEY_ID = "AKIAVGHOU65432EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DB_PASSWORD = "super_secret_password_123!"

app = Flask(__name__)

# CRITICAL: Weak Cryptography & Hardcoded Config (Triggers Vuln Scanner)
app.config['SECRET_KEY'] = '12345'
app.config['DEBUG'] = True

@app.route('/')
def index():
    return """
    <h1>Vulnerable Demo App</h1>
    <p>This application contains multiple security flaws for demonstration.</p>
    <ul>
        <li><a href="/login?username=admin">SQL Injection Demo</a></li>
        <li><a href="/ping?ip=8.8.8.8">Command Injection Demo</a></li>
        <li><a href="/hello?name=<script>alert(1)</script>">XSS Demo</a></li>
    </ul>
    """

@app.route('/login')
def login():
    username = request.args.get('username', '')
    
    # CRITICAL: SQL Injection (Triggers Vuln Scanner/Semgrep)
    # The query is constructed using string concatenation with user input
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            return f"Logged in as: {user[0]}"
        return "Login failed"
    except Exception as e:
        return f"Error: {e}"

@app.route('/ping')
def ping():
    ip = request.args.get('ip', '127.0.0.1')
    
    # CRITICAL: Command Injection (Triggers Vuln Scanner/Semgrep)
    # User input is passed directly to os.system
    os.system("ping -c 1 " + ip)
    
    return f"Pinged {ip}"

@app.route('/hello')
def hello():
    name = request.args.get('name', 'World')
    
    # CRITICAL: Cross-Site Scripting (XSS) (Triggers Vuln Scanner)
    # User input is rendered directly without escaping
    template = f"<h2>Hello {name}</h2>"
    
    # Also triggers "eval with user input" detection if we were crazy enough to use it
    # eval(name) 
    
    return render_template_string(template)

@app.route('/debug')
def debug():
    # CRITICAL: Information Disclosure
    import subprocess
    # Prints environment variables including secrets
    return str(os.environ)

if __name__ == '__main__':
    # CRITICAL: Runs on 0.0.0.0 (Triggers IaC/Config Scanner)
    app.run(host='0.0.0.0', port=5000)
