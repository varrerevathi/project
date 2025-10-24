pip install flask flask_sqlalchemy flask_cors werkzeug
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash
import os

app = Flask(_name_)
CORS(app)

# --- Database Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Models ---
class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    education = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    skill_category = db.Column(db.String(100))
    skill_sub = db.Column(db.String(100))

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    service_category = db.Column(db.String(100))
    service_sub = db.Column(db.String(100))


# --- Initialize Database ---
with app.app_context():
    db.create_all()


# --- Routes ---
@app.route('/')
def home():
    # Render your HTML frontend
    return render_template('index.html')


@app.route('/register_worker', methods=['POST'])
def register_worker():
    data = request.form
    try:
        worker = Worker(
            name=data.get('name'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password')),
            age=int(data.get('age')),
            education=data.get('education'),
            contact=data.get('contact'),
        )
        db.session.add(worker)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Worker registered successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit_worker_skills', methods=['POST'])
def submit_worker_skills():
    data = request.json
    email = data.get('email')
    category = data.get('category')
    sub = data.get('sub')

    worker = Worker.query.filter_by(email=email).first()
    if not worker:
        return jsonify({'status': 'error', 'message': 'Worker not found.'})

    worker.skill_category = category
    worker.skill_sub = sub
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Worker skills updated successfully!'})


@app.route('/register_customer', methods=['POST'])
def register_customer():
    data = request.form
    try:
        customer = Customer(
            name=data.get('name'),
            email=data.get('email'),
            age=int(data.get('age')),
            contact=data.get('contact')
        )
        db.session.add(customer)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Customer registered successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit_customer_services', methods=['POST'])
def submit_customer_services():
    data = request.json
    email = data.get('email')
    category = data.get('category')
    sub = data.get('sub')

    customer = Customer.query.filter_by(email=email).first()
    if not customer:
        return jsonify({'status': 'error', 'message': 'Customer not found.'})

    customer.service_category = category
    customer.service_sub = sub
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Customer services updated successfully!'})


if _name_ == '_main_':
    app.run(debug=True)
const formData = new FormData();
formData.append('name', name);
formData.append('email', userEmail);
formData.append('password', password);
formData.append('age', age);
formData.append('education', education);
formData.append('contact', contact);

fetch('http://127.0.0.1:5000/register_worker', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => {
  if (data.status === 'success') {
    document.getElementById('workerSignupSection').style.display = 'none';
    document.getElementById('workerSkillsSection').style.display = 'block';
  } else {
    alert(data.message);
  }
});
const formData = new FormData();
formData.append('name', name);
formData.append('email', userEmail);
formData.append('age', age);
formData.append('contact', contact);

fetch('http://127.0.0.1:5000/register_customer', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => {
  if (data.status === 'success') {
    document.getElementById('customerSignupSection').style.display = 'none';
    document.getElementById('customerServicesSection').style.display = 'block';
  } else {
    alert(data.message);
  }
});
fetch('http://127.0.0.1:5000/submit_customer_services', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    email: userEmail,
    category: selectedCategory,
    sub: selectedSub
  })
})
.then(res => res.json())
.then(data => {
  document.getElementById('customerServicesSection').style.display = 'none';
  document.getElementById('alertSection').style.display = 'block';
  document.getElementById('alerts').innerHTML = `
    <div class="alert-box">
      <p>${data.message}</p>
      <p>Selected service: <b>${selectedCategory} - ${selectedSub}</b></p>
      <p>📧 Email: <b>${userEmail}</b></p>
    </div>
  `;
});
