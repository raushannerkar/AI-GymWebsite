from datetime import timedelta
import time
from website_folder import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    calculation_results = db.relationship('CalculationResult', backref='user', lazy='dynamic')

    def get_token(self, expires_sec=300):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id, 'exp': time.time() + expires_sec})
    
    @staticmethod
    def verify_token(token):
        serial=Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    



class CalculationResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bmi = db.Column(db.Float)
    bmr = db.Column(db.Float)
    ideal_weight = db.Column(db.Float)
    body_fat_percentage = db.Column(db.Float)
    lean_body_mass = db.Column(db.Float)
    waist_to_hip_ratio = db.Column(db.Float)
    waist_to_height_ratio = db.Column(db.Float)
    protein_intake = db.Column(db.Float)
    calorie_intake = db.Column(db.Float)
    fat_intake = db.Column(db.Float)
    carbohydrate_intake = db.Column(db.Float)
    water_intake = db.Column(db.Float)
    tdee = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

