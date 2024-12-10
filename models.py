from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
# Initialize SQLAlchemy
db = SQLAlchemy()

# Book Model
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    title = db.Column(db.String(150), nullable=False)  # Book title
    author = db.Column(db.String(100), nullable=False)  # Author's name
    published_year = db.Column(db.Integer)  # Year of publication
    isbn = db.Column(db.String(20), unique=True, nullable=False)  # ISBN number

    def __repr__(self):
        return f"<Book {self.title}>"

# Member Model
class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    name = db.Column(db.String(100), nullable=False)  # Member's name
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unique email
    password = db.Column(db.String(200), nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"<Member {self.name}>"
