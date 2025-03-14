from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, UTC
import os
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    avatar_path = db.Column(db.String(100), default='default_avatar.png')
    tasks = db.relationship('Task', backref='user', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    finished_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_avatar(file, username):
    if file and allowed_file(file.filename):
        try:
            # Create a secure filename with timestamp to prevent collisions
            timestamp = datetime.now(UTC).strftime('%Y%m%d_%H%M%S')
            filename = secure_filename(f'avatar_{username}_{timestamp}_{file.filename}')
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save the file
            file.save(file_path)
            
            # Validate the image
            try:
                with Image.open(file_path) as img:
                    img.verify()
                return f'uploads/{filename}'
            except Exception as e:
                # If image validation fails, remove the file
                if os.path.exists(file_path):
                    os.remove(file_path)
                raise ValueError('Invalid image file')
        except Exception as e:
            raise ValueError(f'Error saving avatar: {str(e)}')
    return None

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role='user'
        )
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    overdue_tasks = Task.query.filter_by(
        user_id=current_user.id,
        status='pending'
    ).filter(Task.due_date < datetime.now(UTC)).all()
    
    overdue_count = len(overdue_tasks)
    return render_template('dashboard.html', 
                         tasks=tasks, 
                         overdue_tasks=overdue_tasks,
                         overdue_count=overdue_count)

@app.route('/task/add', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%d')
    
    task = Task(
        title=title,
        description=description,
        due_date=due_date,
        user_id=current_user.id
    )
    
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/task/complete/<int:task_id>')
@login_required
def complete_task(task_id):
    task = db.session.get(Task, task_id)
    if task and task.user_id == current_user.id:
        task.status = 'completed'
        task.finished_time = datetime.now(UTC)
        db.session.commit()
        flash('Task marked as complete!')
    return redirect(url_for('dashboard'))

@app.route('/task/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!')
    return redirect(url_for('dashboard'))

@app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = db.session.get(Task, task_id)
    if not task or task.user_id != current_user.id:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%d')
        db.session.commit()
        flash('Task updated successfully!')
        return redirect(url_for('dashboard'))
    
    # Calculate overdue tasks count for the base template
    overdue_tasks = Task.query.filter_by(
        user_id=current_user.id,
        status='pending'
    ).filter(Task.due_date < datetime.now(UTC)).all()
    overdue_count = len(overdue_tasks)
        
    return render_template('edit_task.html', task=task, overdue_count=overdue_count)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/update_avatar', methods=['POST'])
@login_required
def update_avatar():
    if 'avatar' not in request.files:
        flash('No file selected')
        return redirect(url_for('dashboard'))
        
    file = request.files['avatar']
    if not file.filename:
        flash('No file selected')
        return redirect(url_for('dashboard'))
        
    try:
        avatar_path = save_avatar(file, current_user.username)
        if avatar_path:
            # Delete old avatar if it exists
            if current_user.avatar_path:
                old_avatar_path = os.path.join('static', current_user.avatar_path)
                if os.path.exists(old_avatar_path):
                    try:
                        os.remove(old_avatar_path)
                    except Exception as e:
                        app.logger.error(f'Error deleting old avatar: {str(e)}')
            
            current_user.avatar_path = avatar_path
            db.session.commit()
            flash('Avatar updated successfully!')
        else:
            flash('Invalid file type. Please upload an image file.')
    except ValueError as e:
        flash(str(e))
    except Exception as e:
        app.logger.error(f'Error updating avatar: {str(e)}')
        flash('An error occurred while updating your avatar.')
        
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 