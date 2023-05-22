import requests
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_db", user="postgres", password="Awe6ve2056E", host="localhost", port='5432')
cursor = conn.cursor()


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login4.html')


@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute('SELECT * FROM service.users WHERE login=%s AND password=%s', (str(username), str(password)))
    conn.commit()
    record = list(cursor.fetchall())
    if len(record) != 0:
        return render_template('account.html', full_name=record[0][1], login=record[0][2], password=record[0][3])
    return render_template('login4.html', flag=len(record))
