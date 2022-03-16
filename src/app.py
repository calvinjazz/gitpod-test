from flask import Flask, jsonify, request, render_template, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.safe_load(open('src/db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

todos = [
    { "label": "My first task", "done": False },
    { "label": "My second task", "done": False }
]

@app.route('/', methods=['GET'])
def index():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Contact")
    if resultValue > 0:
        contactDetails = cur.fetchall()
        return render_template('index.html',contactDetails=contactDetails)

@app.route('/create', methods=['GET', 'POST'])
def create():
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
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Contact(contactId,firstName,lastName,email,age,salary,address) VALUES(%s, %s, %s, %s, %s, %s, %s)",(contactId,firstName,lastName,email,age,salary,address))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('create.html')

@app.route("/contacts/<int:id>/update", methods=("GET", "POST"))
def update(id):
    contact = id
    if request.method == "POST":
        contactDetails = request.form
        firstName = contactDetails['firstName']
        lastName = contactDetails['lastName']
        email = contactDetails['email']
        age = contactDetails['age']
        salary = contactDetails['salary']
        address = contactDetails['address']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE Contact SET firstName = %s, lastName = %s, email = %s, age = %s, salary = %s, address = %s WHERE contactId = %s",(firstName,lastName,email,age,salary,address,id))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('update.html', contact=contact)


@app.route('/contacts/<int:id>/delete', methods=['POST'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Contact WHERE contactId = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/')

# These two lines should always be at the end of your app.py file.
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)