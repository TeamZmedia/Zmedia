from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your actual secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Replace with your database URI

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # This redirects unauthorized users to the login page

# User model for Flask-Login
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('home.html')  # Ensure you have a home.html template

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Add logic to check username and password
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:  # Simplified password check
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html')  # Ensure you have a login.html template

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)  # Ensure you have a profile.html template

# Database creation
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
