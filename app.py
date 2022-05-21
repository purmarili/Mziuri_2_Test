import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)
try:
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE USERS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT ,
            USERNAME TEXT NOT NULL UNIQUE ,
            PASSWORD TEXT NOT NULL 
            CHECK ( length(PASSWORD) >= 6 AND length(USERNAME) >= 4 )
        )
    ''')
    connection.close()
except sqlite3.OperationalError:
    pass


@app.route('/')
def get_main():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def get_login():
    username_ = request.form['username']
    password_ = request.form['password']
    try:
        curr_connection = sqlite3.connect('users.db')
        curr_cursor = curr_connection.cursor()
        curr_cursor.execute('''
            INSERT INTO USERS (USERNAME, PASSWORD)
            VALUES (?, ?)
        ''', (username_, password_))
        curr_connection.commit()
        curr_connection.close()
    except sqlite3.IntegrityError:
        return 'User already exists!'

    return f'Welcome {username_}'


@app.route('/users')
def get_users():
    curr_connection = sqlite3.connect('users.db')
    curr_cursor = curr_connection.cursor()
    curr_cursor.execute('SELECT USERNAME, PASSWORD FROM USERS')
    all_users = curr_cursor.fetchmany(50)
    curr_connection.close()
    return render_template('users.html', users=all_users)


if __name__ == '__main__':
    app.run()
