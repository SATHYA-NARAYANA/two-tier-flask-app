import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL database from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')

# Initialize MySQL connection
mysql = MySQL(app)

# Route to display messages
@app.route('/')
def display_messages():
    # Create a cursor to interact with the database
    cur = mysql.connection.cursor()
    # Execute SQL query to fetch messages from the 'messages' table
    cur.execute('SELECT message FROM messages')
    # Fetch all messages from the query result
    messages = cur.fetchall()
    # Close the cursor
    cur.close()
    # Render the 'index.html' template with the messages
    return render_template('index.html', messages=messages)

# Route to submit new messages
@app.route('/submit', methods=['POST'])
def submit_message():
    # Get the new message from the form
    new_message = request.form.get('new_message')
    # Create a cursor to interact with the database
    cur = mysql.connection.cursor()
    # Execute SQL query to insert the new message into the 'messages' table
    cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
    # Commit the changes to the database
    mysql.connection.commit()
    # Close the cursor
    cur.close()
    # Redirect to the display_messages route after submission
    return redirect(url_for('display_messages'))

# Run the Flask application
if __name__ == '__main__':
    # Start the Flask app on specified host and port, enabling debugging
    app.run(host='0.0.0.0', port=5000, debug=True)
