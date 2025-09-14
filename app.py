app.py
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import random

# Configure logging (use INFO in production)
logging.basicConfig(level=logging.INFO)

# Admin configuration
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "password")  # CRITICAL: Set in production

# Security validation
if not os.environ.get("SESSION_SECRET"):
    print("WARNING: SESSION_SECRET not set! This is insecure for production.")
if not os.environ.get("ADMIN_PASSWORD") and os.environ.get("FLASK_ENV") == "production":
    print("CRITICAL: ADMIN_PASSWORD must be set in production!")

# Global data storage variables (initialized before functions)
users_db = {}  # {username: {'id': int, 'password_hash': str, 'is_admin': bool}}
global_vocabulary = []  # Global vocabulary for all users: [{'deutsch': str, 'spanisch': str}]
user_progress = {}  # {user_id: {'known': [vocab_ids], 'review': [vocab_ids], 'current_index': int}}
user_counter = 0
chapters = {}  # {chapter_id: {'name': str, 'vocabulary': []}}
chapter_counter = 0

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1) # needed for url_for to generate with https

# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Security configuration for production
app.config["SESSION_COOKIE_SECURE"] = True  # HTTPS only in production
app.config["SESSION_COOKIE_HTTPONLY"] = True  # Prevent XSS access
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # CSRF protection
app.config["REMEMBER_COOKIE_SECURE"] = True  # Secure remember-me cookies
app.config["REMEMBER_COOKIE_HTTPONLY"] = True  # Prevent XSS on remember cookies
app.config["REMEMBER_COOKIE_SAMESITE"] = "Lax"  # Additional CSRF protection
# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Bitte melden Sie sich an, um diese Seite zu besuchen.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    from models import User
    return User.query.get(int(user_id))

@app.before_request
def sync_session_with_current_user():
    """Sync session data when user is restored via remember cookie"""
    if current_user.is_authenticated:
        # If Flask-Login restored user but session is empty, hydrate it
        if "username" not in session or "user_id" not in session:
            session["username"] = current_user.username
            session["user_id"] = current_user.id
            session["accepted"] = True  # Auto-accept for remember users

# Database migration functions must be defined before use
def migrate_data_to_db():
    """Migrate in-memory data to PostgreSQL database."""
    from models import User, Chapter, Vocabulary, UserProgress
    
    # Migrate admin user if not exists
    admin_user = User.query.filter_by(username=ADMIN_USERNAME).first()
    if not admin_user:
        admin_user = User(
            username=ADMIN_USERNAME,
            email=f"{ADMIN_USERNAME}@admin.local",
            password_hash=generate_password_hash(ADMIN_PASSWORD),
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        logging.info(f"Admin user migrated to database: {ADMIN_USERNAME}")
    
    # Migrate chapters if not exist
    if Chapter.query.count() == 0:
        init_sample_chapters_db()
        logging.info("Sample chapters migrated to database")
        
    # Initialize in-memory data from database for backward compatibility
    load_data_from_db()

def init_sample_chapters_db():
    """Initialize empty chapter 1 in database."""
    from models import Chapter
    
    # Only create empty Chapter 1
    chapter1 = Chapter(name='Kapitel 1')
    db.session.add(chapter1)
    
    db.session.commit()
    logging.info("Empty Chapter 1 created")

def load_data_from_db():
    """Load data from database into in-memory structures for backward compatibility."""
    from models import User, Chapter, Vocabulary
    global users_db, chapters, user_counter, chapter_counter
    
    # Load users
    users_db = {}
    for user in User.query.all():
        users_db[user.username] = {
            'id': user.id,
            'password_hash': user.password_hash,
            'is_admin': user.is_admin
        }
        user_counter = max(user_counter, user.id)
    
    # Load chapters
    chapters = {}
    for chapter in Chapter.query.all():
        vocab_list = []
        for vocab in chapter.vocabularies:
            vocab_list.append({
                'deutsch': vocab.deutsch,
                'spanisch': vocab.spanisch
            })
        
        chapters[chapter.id] = {
            'name': chapter.name,
            'vocabulary': vocab_list
        }
        chapter_counter = max(chapter_counter, chapter.id)

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    from models import User, Chapter, Vocabulary, UserProgress  # noqa: F401
    db.create_all()
    
    # Migrate in-memory data to database
    migrate_data_to_db()

# In-memory data storage (legacy, will be migrated to database)
# Global variables initialized above before functions


# Initialize admin user (legacy function - now uses database)
def init_admin():
    """Legacy function - admin user is now handled in database migration."""
    logging.info("Admin initialization handled via database migration")


init_admin()

# Initialize sample chapters (legacy function - now uses database)
def init_sample_chapters():
    global chapter_counter, chapters
    if not chapters:
        chapter_counter += 1
        chapters[chapter_counter] = {
            'name': 'Kapitel 1 - Begrüßungen',
            'vocabulary': [
                {'deutsch': 'Hallo', 'spanisch': 'Hola'},
                {'deutsch': 'Guten Morgen', 'spanisch': 'Buenos días'},
                {'deutsch': 'Guten Tag', 'spanisch': 'Buenas tardes'},
                {'deutsch': 'Gute Nacht', 'spanisch': 'Buenas noches'},
                {'deutsch': 'Auf Wiedersehen', 'spanisch': 'Adiós'},
                {'deutsch': 'Bis bald', 'spanisch': 'Hasta pronto'},
                {'deutsch': 'Wie geht es dir?', 'spanisch': '¿Cómo estás?'},
                {'deutsch': 'Danke', 'spanisch': 'Gracias'},
                {'deutsch': 'Bitte', 'spanisch': 'Por favor'},
                {'deutsch': 'Entschuldigung', 'spanisch': 'Perdón'}
            ]
        }
        
        chapter_counter += 1
        chapters[chapter_counter] = {
            'name': 'Kapitel 2 - Familie',
            'vocabulary': [
                {'deutsch': 'Familie', 'spanisch': 'Familia'},
                {'deutsch': 'Mutter', 'spanisch': 'Madre'},
                {'deutsch': 'Vater', 'spanisch': 'Padre'},
                {'deutsch': 'Bruder', 'spanisch': 'Hermano'},
                {'deutsch': 'Schwester', 'spanisch': 'Hermana'},
                {'deutsch': 'Großmutter', 'spanisch': 'Abuela'},
                {'deutsch': 'Großvater', 'spanisch': 'Abuelo'},
                {'deutsch': 'Sohn', 'spanisch': 'Hijo'},
                {'deutsch': 'Tochter', 'spanisch': 'Hija'},
                {'deutsch': 'Onkel', 'spanisch': 'Tío'}
            ]
        }
        
        chapter_counter += 1
        chapters[chapter_counter] = {
            'name': 'Kapitel 3 - Zahlen',
            'vocabulary': [
                {'deutsch': 'Eins', 'spanisch': 'Uno'},
                {'deutsch': 'Zwei', 'spanisch': 'Dos'},
                {'deutsch': 'Drei', 'spanisch': 'Tres'},
                {'deutsch': 'Vier', 'spanisch': 'Cuatro'},
                {'deutsch': 'Fünf', 'spanisch': 'Cinco'},
                {'deutsch': 'Sechs', 'spanisch': 'Seis'},
                {'deutsch': 'Sieben', 'spanisch': 'Siete'},
                {'deutsch': 'Acht', 'spanisch': 'Ocho'},
                {'deutsch': 'Neun', 'spanisch': 'Nueve'},
                {'deutsch': 'Zehn', 'spanisch': 'Diez'}
            ]
        }

init_sample_chapters()

# -----------------------
# Hilfsfunktionen
# -----------------------
def get_user_id():
    if current_user.is_authenticated:
        return current_user.id
    return session.get("user_id")  # Fallback for legacy sessions

def is_admin():
    """Check if current user is admin"""
    if current_user.is_authenticated:
        return current_user.is_admin
    username = session.get("username")
    return username and users_db.get(username, {}).get('is_admin', False)

def require_admin():
    """Decorator function to require admin access"""
    if not get_user_id():
        return redirect(url_for("login"))
    if not is_admin():
        flash("Zugriff verweigert! Admin-Berechtigung erforderlich.", "error")
        return redirect(url_for("index"))
    return None

# -----------------------
# Routen
# -----------------------
@app.route("/")
def disclaimer():
    if "accepted" in session:
        return redirect(url_for("index"))
    return render_template("disclaimer.html")

@app.route("/accept")
def accept():
    session["accepted"] = True
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        email = request.form.get("email", f"{username}@student.local").strip()
        
        if not username or not password:
            flash("Benutzername und Passwort sind erforderlich!", "error")
            return render_template("register.html")
        
        # Check database first
        from models import User
        existing_user = User.query.filter_by(username=username).first()
        if existing_user or username in users_db:
            flash("Benutzername existiert bereits!", "error")
            return render_template("register.html")
        
        password_hash = generate_password_hash(password)
        
        # Create user in database
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            is_admin=False
        )
        db.session.add(new_user)
        db.session.commit()
        
        # Also add to legacy in-memory storage for backward compatibility
        global user_counter
        user_counter += 1
        users_db[username] = {
            'id': new_user.id,
            'password_hash': password_hash,
            'is_admin': False
        }
        
        flash("Registrierung erfolgreich! Sie können sich jetzt anmelden.", "success")
        logging.info(f"New user registered: {username}")
        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        
        # Check database first, fallback to in-memory users_db
        from models import User
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)  # remember=True for persistent sessions
            session["accepted"] = True  # Auto-accept terms on successful login
            session["username"] = user.username  # Fix: Set username in session
            session["user_id"] = user.id  # Keep for compatibility
            flash(f"Willkommen zurück, {username}!", "success")
            logging.info(f"User logged in: {username}")
            return redirect(url_for("index"))
        elif username in users_db and check_password_hash(users_db[username]['password_hash'], password):
            # Fallback for legacy users not yet in database
            session["user_id"] = users_db[username]['id']
            session["username"] = username
            session["accepted"] = True
            flash(f"Willkommen zurück, {username}!", "success")
            logging.info(f"User logged in: {username}")
            return redirect(url_for("index"))
        else:
            flash("Falscher Benutzername oder Passwort!", "error")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    username = current_user.username if current_user.is_authenticated else session.get("username")
    logout_user()  # CRITICAL FIX: Properly logout user and clear remember cookie
    # Clear specific session keys (NOT session.clear() - it breaks Flask-Login remember cookie clearing)
    for key in ('username', 'user_id', 'accepted', 'selected_chapter'):
        session.pop(key, None)
    if username:
        flash(f"Auf Wiedersehen, {username}!", "info")
    return redirect(url_for("disclaimer"))

@app.route("/index")
def index():
    if not get_user_id():
        return redirect(url_for("login"))
    if "accepted" not in session:
        return redirect(url_for("disclaimer"))
    
    # Show chapter selection
    return render_template("index.html", 
                         username=session["username"],
                         chapters=chapters,
                         is_admin=is_admin())

@app.route("/select_chapter/<int:chapter_id>")
def select_chapter(chapter_id):
    if not get_user_id():
        return redirect(url_for("login"))
    
    if chapter_id not in chapters:
        flash("Kapitel nicht gefunden!", "error")
        return redirect(url_for("index"))
    
    # Store selected chapter in session
    session['selected_chapter'] = chapter_id
    flash(f"Kapitel '{chapters[chapter_id]['name']}' ausgewählt!", "success")
    return redirect(url_for("chapter_overview"))

@app.route("/chapter_overview")
def chapter_overview():
    if not get_user_id():
        return redirect(url_for("login"))
    
    chapter_id = session.get('selected_chapter')
    if not chapter_id or chapter_id not in chapters:
        flash("Bitte wählen Sie zuerst ein Kapitel aus!", "warning")
        return redirect(url_for("index"))
    
    chapter = chapters[chapter_id]
    vocab_count = len(chapter['vocabulary'])
    
    # Calculate progress for this chapter
    user_id = get_user_id()
    if user_id not in user_progress:
        user_progress[user_id] = {'known': [], 'review': [], 'current_index': 0}
    
    # Progress is based on chapter vocabulary indices
    chapter_progress = {
        'known': 0,
        'review': 0,
        'total': vocab_count
    }
    
    for i in range(vocab_count):
        if i in user_progress[user_id]['known']:
            chapter_progress['known'] += 1
        elif i in user_progress[user_id]['review']:
            chapter_progress['review'] += 1
    
    return render_template("chapter_overview.html", 
                         username=session["username"],
                         chapter=chapter,
                         chapter_id=chapter_id,
                         progress=chapter_progress,
                         is_admin=is_admin())

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if not get_user_id():
        return redirect(url_for("login"))
    
    chapter_id = session.get('selected_chapter')
    if not chapter_id or chapter_id not in chapters:
        flash("Bitte wählen Sie zuerst ein Kapitel aus!", "warning")
        return redirect(url_for("index"))
    
    chapter_vocabulary = chapters[chapter_id]['vocabulary']
    if not chapter_vocabulary:
        flash("Dieses Kapitel enthält noch keine Vokabeln!", "warning")
        return redirect(url_for("chapter_overview"))
    
    user_id = get_user_id()
    
    if request.method == "POST":
        current_vocab_index = int(request.form.get("vocab_index", 0))
        spanisch = request.form["spanisch"].strip()
        
        if not spanisch:
            flash("Bitte geben Sie die spanische Übersetzung ein!", "error")
            return render_template("quiz.html")
        
        # Get the current vocabulary item from chapter
        if current_vocab_index < len(chapter_vocabulary):
            current_vocab = chapter_vocabulary[current_vocab_index]
            correct_answer = current_vocab['spanisch']
            
            if correct_answer.lower() == spanisch.lower():
                result = "Richtig! ✅"
                result_class = "success"
                # Mark as known
                if user_id not in user_progress:
                    user_progress[user_id] = {'known': [], 'review': [], 'current_index': 0}
                if current_vocab_index not in user_progress[user_id]['known']:
                    user_progress[user_id]['known'].append(current_vocab_index)
                    if current_vocab_index in user_progress[user_id]['review']:
                        user_progress[user_id]['review'].remove(current_vocab_index)
            else:
                result = f"Falsch ❌ – richtig wäre: {correct_answer}"
                result_class = "error"
                # Mark for review if wrong
                if user_id not in user_progress:
                    user_progress[user_id] = {'known': [], 'review': [], 'current_index': 0}
                if current_vocab_index not in user_progress[user_id]['review']:
                    user_progress[user_id]['review'].append(current_vocab_index)
        else:
            result = "Vokabel nicht gefunden!"
            result_class = "warning"
        
        # Get next random vocabulary from chapter
        next_vocab = random.choice(chapter_vocabulary)
        next_index = chapter_vocabulary.index(next_vocab)
        
        # Calculate progress
        total_vocab = len(chapter_vocabulary)
        known_count = len(user_progress[user_id]['known']) if user_id in user_progress else 0
        
        return render_template("quiz.html", 
                             result=result, 
                             result_class=result_class,
                             current_vocab=next_vocab,
                             vocab_index=next_index,
                             chapter_name=chapters[chapter_id]['name'],
                             progress_text=f"{known_count} von {total_vocab}")
    
    # GET request - show random vocabulary from chapter
    current_vocab = random.choice(chapter_vocabulary)
    vocab_index = chapter_vocabulary.index(current_vocab)
    
    # Calculate progress
    total_vocab = len(chapter_vocabulary)
    known_count = len(user_progress[user_id]['known']) if user_id in user_progress else 0
    
    return render_template("quiz.html", 
                         current_vocab=current_vocab,
                         vocab_index=vocab_index,
                         chapter_name=chapters[chapter_id]['name'],
                         progress_text=f"{known_count} von {total_vocab}")

@app.route("/learn")
def learn():
    """Redirect to flashcards for general learning"""
    if not get_user_id():
        return redirect(url_for("login"))
    
    # Set default chapter if none selected
    if not session.get('selected_chapter'):
        session['selected_chapter'] = 1  # Default to first chapter
    
    return redirect(url_for('flashcards'))

@app.route("/flashcards")
def flashcards():
    if not get_user_id():
        return redirect(url_for("login"))
    
    chapter_id = session.get('selected_chapter')
    if not chapter_id or chapter_id not in chapters:
        flash("Bitte wählen Sie zuerst ein Kapitel aus!", "warning")
        return redirect(url_for("index"))
    
    chapter_vocabulary = chapters[chapter_id]['vocabulary']
    if not chapter_vocabulary:
        flash("Dieses Kapitel enthält noch keine Vokabeln!", "warning")
        return redirect(url_for("chapter_overview"))
    
    user_id = get_user_id()
    if user_id not in user_progress:
        user_progress[user_id] = {'known': [], 'review': [], 'current_index': 0}
    
    # Calculate progress
    total_vocab = len(chapter_vocabulary)
    known_count = len(user_progress[user_id]['known'])
    progress_text = f"{known_count} von {total_vocab}"
    
    return render_template("flashcards.html", 
                         vokabeln=chapter_vocabulary,
                         chapter_name=chapters[chapter_id]['name'],
                         progress_text=progress_text,
                         user_progress=user_progress[user_id])


@app.route("/set_theme", methods=["POST"])
def set_theme():
    """Set user's theme preference explicitly"""
    if not current_user.is_authenticated:
        return '', 401  # Return 401 instead of redirect for AJAX
    
    theme = request.form.get('theme')
    if theme not in ['light', 'dark']:
        return '', 400  # Bad request for invalid theme
    
    current_user.theme_preference = theme
    db.session.commit()
    
    return '', 204  # Return 204 No Content for successful AJAX requests

@app.route("/flashcard_action", methods=["POST"])
def flashcard_action():
    if not get_user_id():
        return redirect(url_for("login"))
    
    user_id = get_user_id()
    action = request.form.get("action")
    vocab_index = int(request.form.get("vocab_index", 0))
    
    if user_id not in user_progress:
        user_progress[user_id] = {'known': [], 'review': [], 'current_index': 0}
    
    if action == "known":
        if vocab_index not in user_progress[user_id]['known']:
            user_progress[user_id]['known'].append(vocab_index)
        if vocab_index in user_progress[user_id]['review']:
            user_progress[user_id]['review'].remove(vocab_index)
    elif action == "review":
        if vocab_index not in user_progress[user_id]['review']:
            user_progress[user_id]['review'].append(vocab_index)
        if vocab_index in user_progress[user_id]['known']:
            user_progress[user_id]['known'].remove(vocab_index)
    
    return '', 204  # No content response

@app.route("/review")
def review_words():
    if not get_user_id():
        return redirect(url_for("login"))
    
    chapter_id = session.get('selected_chapter')
    if not chapter_id or chapter_id not in chapters:
        flash("Bitte wählen Sie zuerst ein Kapitel aus!", "warning")
        return redirect(url_for("index"))
    
    user_id = get_user_id()
    if user_id not in user_progress or not user_progress[user_id]['review']:
        flash("Keine Vokabeln zum Wiederholen vorhanden!", "info")
        return redirect(url_for("chapter_overview"))
    
    # Get vocabulary items marked for review from current chapter
    chapter_vocabulary = chapters[chapter_id]['vocabulary']
    review_vocabulary = []
    for vocab_index in user_progress[user_id]['review']:
        if 0 <= vocab_index < len(chapter_vocabulary):
            review_vocabulary.append(chapter_vocabulary[vocab_index])
    
    if not review_vocabulary:
        flash("Keine Vokabeln zum Wiederholen in diesem Kapitel!", "info")
        return redirect(url_for("chapter_overview"))
    
    # Calculate progress
    total_vocab = len(chapter_vocabulary)
    known_count = len(user_progress[user_id]['known'])
    progress_text = f"{known_count} von {total_vocab}"
    
    return render_template("review.html", 
                         vokabeln=review_vocabulary,
                         chapter_name=chapters[chapter_id]['name'],
                         progress_text=progress_text,
                         user_progress=user_progress[user_id])

@app.route("/admin", methods=["GET", "POST"])
def admin_panel():
    admin_check = require_admin()
    if admin_check:
        return admin_check
    
    from models import User, Chapter, Vocabulary, UserProgress
    
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "add_chapter":
            name = request.form["chapter_name"].strip()
            description = request.form.get("chapter_description", "").strip()
            
            if not name:
                flash("Kapitelname ist erforderlich!", "error")
            else:
                try:
                    # Check if chapter already exists
                    existing_chapter = Chapter.query.filter_by(name=name).first()
                    if existing_chapter:
                        flash("Ein Kapitel mit diesem Namen existiert bereits!", "warning")
                    else:
                        new_chapter = Chapter(name=name, description=description or None)
                        db.session.add(new_chapter)
                        db.session.commit()
                        # CRITICAL FIX: Reload in-memory data after DB change
                        load_data_from_db()
                        flash(f"Kapitel '{name}' erfolgreich erstellt!", "success")
                        logging.info(f"New chapter created: {name}")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Fehler beim Erstellen des Kapitels: {str(e)}", "error")
                    logging.error(f"Error creating chapter {name}: {str(e)}")
        
        elif action == "add_vocabulary":
            chapter_id = request.form.get("chapter_id")
            deutsch = request.form["deutsch"].strip()
            spanisch = request.form["spanisch"].strip()
            
            if not chapter_id or not deutsch or not spanisch:
                flash("Alle Felder sind erforderlich!", "error")
            else:
                try:
                    # CRITICAL FIX: Proper type casting
                    chapter_id = int(chapter_id)
                    chapter = db.session.get(Chapter, chapter_id)
                    if not chapter:
                        flash("Kapitel nicht gefunden!", "error")
                    else:
                        # Check if vocabulary already exists in this chapter
                        existing_vocab = Vocabulary.query.filter_by(
                            chapter_id=chapter_id,
                            deutsch=deutsch
                        ).first()
                        
                        if existing_vocab:
                            flash(f"Diese deutsche Vokabel existiert bereits in '{chapter.name}'!", "warning")
                        else:
                            new_vocab = Vocabulary(
                                chapter_id=chapter_id,
                                deutsch=deutsch,
                                spanisch=spanisch
                            )
                            db.session.add(new_vocab)
                            db.session.commit()
                            # CRITICAL FIX: Reload in-memory data after DB change
                            load_data_from_db()
                            flash(f"Vokabel '{deutsch} - {spanisch}' zu '{chapter.name}' hinzugefügt!", "success")
                            logging.info(f"New vocabulary added: {deutsch} - {spanisch} to chapter {chapter.name}")
                except (ValueError, TypeError) as e:
                    flash(f"Ungültige Kapitel-ID: {str(e)}", "error")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Fehler beim Hinzufügen der Vokabel: {str(e)}", "error")
                    logging.error(f"Error adding vocabulary {deutsch}: {str(e)}")
        
        elif action == "delete_vocabulary":
            vocab_id = request.form.get("vocab_id")
            if vocab_id:
                try:
                    vocab_id = int(vocab_id)
                    vocab = db.session.get(Vocabulary, vocab_id)
                    if vocab:
                        # Delete related progress entries first
                        UserProgress.query.filter_by(vocabulary_id=vocab_id).delete()
                        chapter_name = vocab.chapter.name
                        deutsch = vocab.deutsch
                        db.session.delete(vocab)
                        db.session.commit()
                        # CRITICAL FIX: Reload in-memory data after DB change
                        load_data_from_db()
                        flash(f"Vokabel '{deutsch}' aus '{chapter_name}' wurde gelöscht!", "success")
                        logging.info(f"Vocabulary deleted: {deutsch} from chapter {chapter_name}")
                    else:
                        flash("Vokabel nicht gefunden!", "error")
                except (ValueError, TypeError) as e:
                    flash(f"Ungültige Vokabel-ID: {str(e)}", "error")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Fehler beim Löschen der Vokabel: {str(e)}", "error")
                    logging.error(f"Error deleting vocabulary {vocab_id}: {str(e)}")
        
        elif action == "delete_chapter":
            chapter_id = request.form.get("chapter_id")
            if chapter_id:
                try:
                    chapter_id = int(chapter_id)
                    chapter = db.session.get(Chapter, chapter_id)
                    if chapter:
                        chapter_name = chapter.name
                        # Delete all vocabulary and progress entries for this chapter
                        for vocab in chapter.vocabularies:
                            UserProgress.query.filter_by(vocabulary_id=vocab.id).delete()
                        Vocabulary.query.filter_by(chapter_id=chapter_id).delete()
                        db.session.delete(chapter)
                        db.session.commit()
                        # CRITICAL FIX: Reload in-memory data after DB change
                        load_data_from_db()
                        flash(f"Kapitel '{chapter_name}' und alle zugehörigen Vokabeln wurden gelöscht!", "success")
                        logging.info(f"Chapter deleted: {chapter_name}")
                    else:
                        flash("Kapitel nicht gefunden!", "error")
                except (ValueError, TypeError) as e:
                    flash(f"Ungültige Kapitel-ID: {str(e)}", "error")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Fehler beim Löschen des Kapitels: {str(e)}", "error")
                    logging.error(f"Error deleting chapter {chapter_id}: {str(e)}")
        
        elif action == "delete_user":
            user_id = request.form.get("user_id")
            if user_id:
                try:
                    user_id = int(user_id)
                    user = db.session.get(User, user_id)
                    if user and not user.is_admin:
                        username = user.username
                        # Delete user progress first
                        UserProgress.query.filter_by(user_id=user_id).delete()
                        db.session.delete(user)
                        db.session.commit()
                        # Update in-memory users_db
                        if username in users_db:
                            del users_db[username]
                        flash(f"Benutzer '{username}' wurde gelöscht!", "success")
                        logging.info(f"User deleted: {username}")
                    elif user and user.is_admin:
                        flash("Admin-Account kann nicht gelöscht werden!", "error")
                    else:
                        flash("Benutzer nicht gefunden!", "error")
                except (ValueError, TypeError) as e:
                    flash(f"Ungültige Benutzer-ID: {str(e)}", "error")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Fehler beim Löschen des Benutzers: {str(e)}", "error")
                    logging.error(f"Error deleting user {user_id}: {str(e)}")
    
    # Get all data for template
    chapters = Chapter.query.order_by(Chapter.created_at.desc()).all()
    users = User.query.order_by(User.username).all()
    
    # Calculate statistics
    total_vocabulary = Vocabulary.query.count()
    total_users = User.query.filter_by(is_admin=False).count()
    
    return render_template("admin.html", 
                         chapters=chapters, 
                         users=users,
                         total_vocabulary=total_vocabulary,
                         total_users=total_users)

@app.route("/progress")
def show_progress():
    if not get_user_id():
        return redirect(url_for("login"))
    
    user_id = get_user_id()
    if user_id not in user_progress:
        user_progress[user_id] = {'known': [], 'review': [], 'current_index': 0}
    
    total_vocab = len(global_vocabulary)
    known_count = len(user_progress[user_id]['known'])
    review_count = len(user_progress[user_id]['review'])
    remaining_count = total_vocab - known_count - review_count
    
    progress_percentage = (known_count / total_vocab * 100) if total_vocab > 0 else 0
    
    return render_template("progress.html",
                         total_vocab=total_vocab,
                         known_count=known_count,
                         review_count=review_count,
                         remaining_count=remaining_count,
                         progress_percentage=progress_percentage,
                         user_progress=user_progress[user_id])

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        
        # Check database first, then fallback to in-memory users_db
        from models import User
        admin_user = User.query.filter_by(username=username, is_admin=True).first()
        
        if (username == ADMIN_USERNAME and admin_user and 
            check_password_hash(admin_user.password_hash, password)):
            # Database login success
            login_user(admin_user, remember=True)
            session["username"] = username
            session["user_id"] = admin_user.id
            session["accepted"] = True
            flash(f"Admin-Anmeldung erfolgreich, {username}!", "success")
            logging.info(f"Admin logged in: {username}")
            return redirect(url_for("admin_panel"))
        elif (username == ADMIN_USERNAME and 
              username in users_db and users_db[username].get('is_admin') and
              check_password_hash(users_db[username]['password_hash'], password)):
            # Fallback legacy login
            session["user_id"] = users_db[username]['id']
            session["username"] = username
            session["accepted"] = True
            flash(f"Admin-Anmeldung erfolgreich, {username}!", "success")
            logging.info(f"Admin logged in (legacy): {username}")
            return redirect(url_for("admin_panel"))
        else:
            flash("Falsche Admin-Anmeldedaten!", "error")
            logging.warning(f"Failed admin login attempt: {username}")
    
    return render_template("admin_login.html")

# -----------------------
# Start
# -----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


vokabeln = {
    "Kapitel 1": [
        ("Wir sprechen Spanisch!", "¡Hablamos español!"),
        ("Spanisch (Sprache)", "el español"),
        ("Hallo!", "¡Hola!"),
        ("ich heiße", "me llamo"),
        ("ich komme aus", "soy de"),
        ("ich bin", "soy"),
        ("aus, von", "de"),
        ("Hauptstadt Spaniens", "Madrid"),
        ("ich spreche", "hablo"),
        ("und", "y"),
        ("ein bisschen", "un poco (de)"),
        ("Englisch (Sprache)", "el inglés"),
        ("ich", "yo"),
        ("Stadt in Spanien", "Sevilla"),
        ("auch", "también"),
        ("Deutsch (Sprache)", "el alemán"),
        ("Wie geht’s?", "¿Qué tal?"),
        ("Stadt (in Spanien)", "La Coruña"),
        ("Galicisch (Sprache)", "el gallego"),
        ("Französisch (Sprache)", "el francés"),
        ("Hauptstadt Perus", "Lima"),
        ("die Hauptstadt", "la capital"),
        ("Peru", "Perú"),
        ("Quechua (Sprache)", "el quechua"),
        ("du", "tú"),
        ("Wie heißt du?", "¿Cómo te llamas?"),
        ("wie?", "¿cómo?"),
        ("Woher bist/kommst du?", "¿De dónde eres?"),
        ("woher?", "¿de dónde?"),
        ("du bist", "eres"),
        ("Welche Sprachen sprichst du?", "¿Qué lenguas hablas?"),
        ("was?; welche?, welcher?, welches?", "¿qué?"),
        ("die Sprache", "la lengua"),
        ("du sprichst", "hablas"),
        ("das Beispiel", "el ejemplo"),
        ("hier: Los geht’s!", "¡Vamos!"),
        ("sehr gut", "muy bien"),
        ("sehr", "muy"),
        ("gut", "bien"),
        ("großartig", "fenomenal"),
        ("danke", "gracias"),
        ("er/sie", "él/ella"),
        ("wer?", "¿quién?"),
        ("er/sie ist", "es"),
        ("Sieh mal!", "¡Mira!"),
        ("ein, eine", "un, una"),
        ("der Freund, die Freundin", "el amigo, la amiga"),
        ("Deutschland", "Alemania"),
        ("angenehm, sehr erfreut (Begrüßung)", "encantado, encantada"),
        ("angenehm; sehr erfreut (Begrüßung)", "mucho gusto"),
        ("Los! hier: also", "¡Venga!"),
        ("Bis später!, Bis dann!", "¡Hasta luego!"),
        ("Auf Wiedersehen!", "¡Adiós!"),
        ("Guten Tag!", "¡Buenos días!"),
        ("Guten Tag!/Guten Abend!", "¡Buenas tardes!"),
        ("Guten Abend!/Gute Nacht!", "¡Buenas noches!"),
        ("mehr oder weniger, hier: geht so", "más o menos"),
        ("schlecht", "mal"),
        ("mies, furchtbar", "fatal"),
        ("der Mitschüler, die Mitschülerin", "el compañero, la compañera (de clase)"),
        ("die Klasse, der Unterricht", "la clase"),
        ("der Arbeitskollege, die Arbeitskollegin", "el compañero de trabajo, la compañera de trabajo"),
        ("die Arbeit", "el trabajo"),
        ("lernen, hier: zur Schule gehen, studieren", "estudiar"),
        ("oder", "o"),
        ("arbeiten", "trabajar"),
        ("quatschen, sich unterhalten", "charlar"),
        ("in, an, auf", "en"),
        ("der Platz", "la plaza"),
        ("nein", "no"),
        ("nicht; kein, keine", "no"),
        ("hier", "aquí"),
        ("aber", "pero"),
        ("jetzt", "ahora"),
        ("mein, meine", "mi, mis"),
        ("die Mutter", "la madre"),
        ("sein", "ser"),
        ("stimmt’s?, nicht wahr?", "¿verdad?"),
        ("ja", "sí"),
        ("die weiterführende Schule", "el instituto"),
        ("noch (immer)", "todavía"),
        ("Hör mal!, hier: Sag mal!", "¡Oye!"),
        ("sprechen", "hablar"),
        ("naja, also", "pues"),
        ("(na) klar, natürlich", "claro"),
        ("der Vater", "el padre"),
        ("München", "Múnich"),
        ("deshalb", "por eso"),
        ("zu Hause", "en casa"),
        ("das Haus", "la casa"),
        ("genial", "genial"),
        ("schwierig", "difícil"),
        ("sich verabreden, sich treffen", "quedar"),
        ("etw. üben", "practicar algo"),
        ("Okay, in Ordnung", "vale"),
        ("die Universität", "la universidad"),
        ("die Cafeteria", "la cafetería"),
        ("das Hotel", "el hotel"),
        ("das Unternehmen, der Betrieb", "la empresa"),
        ("das Restaurant", "el restaurante"),
        ("der Supermarkt", "el supermercado"),
        ("die Diskothek", "la discoteca"),
        ("dein, deine", "tu, tus"),
        ("der Herr, die Frau (Anrede)", "el señor, la señora"),
        ("Marokko", "Marruecos"),
        ("Arabisch (Sprache)", "el árabe")
    ]
}
