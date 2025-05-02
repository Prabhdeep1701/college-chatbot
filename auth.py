from flask import session
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return True
    return False

def register_user(email, password):
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return False
    
    # Use werkzeug's password hashing instead of scrypt
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False