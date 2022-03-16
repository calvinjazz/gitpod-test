from flask import Flask, jsonify, request, render_template, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

todos = [
    { "label": "My first task", "done": False },
    { "label": "My second task", "done": False }
]

@app.route('/todos', methods=['GET'])
def hello_world():
    jsonified = jsonify(todos)

    return jsonified

@app.route('/todos', methods=['POST'])
def add_new_todo():
    request_body = request.get_json(force=True)
    print("Incoming request with the following body", request_body)
    todos.append(request_body)
    jsonified = jsonify(todos)
    return jsonified

@app.route('/todos/<int:position>', methods=['DELETE'])
def delete_todo(position):
    print("This is the position to delete: ",position)
    del todos[position]
    jsonified = jsonify(todos)
    return jsonified

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        contactDetails = request.form
        contactId = contactDetails['contactId']
        firstName = contactDetails['firstName']
        lastName = contactDetails['lastName']
        email = contactDetails['email']
        age = contactDetails['age']
        salary = contactDetails['salary']
        address = contactDetails['address']
        cur = mysql.connetion.cursor()
        cur.execute("INSERT INTO Contact(contactId,firstName,lastName,email,age,salary,address) VALUES(%d, %s, %s, %s, %d, %d, %s)",(contactId,firstName,lastName,email,age,salary,address))
        mysql.connection.commit()
        cur.close()
        return redirect('/contacts')
    return render_template('index.html')

@app.route('/contacts', methods=['GET'])
def contacts():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM contacts")
    if resultValue > 0:
        contactDetails = cur.fetchall()
        return render_template('contacts.html',contactDetails=contactDetails)


# These two lines should always be at the end of your app.py file.
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)