from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from medfam import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

class Doctor(User):
    patients = db.relationship('Patient', backref='doctor', lazy=True)

    def __repr__(self):
        return f"Doctor('{self.username}', '{self.email}')"

class Patient(User):
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    def __repr__(self):
        return f"Patient('{self.username}', '{self.email}', '{self.doctor_id}')"

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Subscription('{self.doctor_id}', '{self.patient_id}', '{self.start_date}', '{self.end_date}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))