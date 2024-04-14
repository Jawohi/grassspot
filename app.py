from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from models.models import Plant, CareJournalEntry, db
from models.user import User
from bson import ObjectId
from datetime import datetime
from flask_uploads import UploadSet, configure_uploads, IMAGES
import bcrypt


app = Flask(__name__)

app.config['SECRET_KEY'] = '7763fa0b8072a082a17dd9e52721bb2e'
app.config['MONGO_URI'] = 'mongodb+srv://jawohi_gs:myedMz0mDterDuRl@grasscluster.bcqofix.mongodb.net/Grassspot_DB'

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.unauthorized_handler
def unauthorized():
    print("Unauthorized access detected")  # Debug statement
    print("Current user:", current_user)  # Debug statement
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    # Implement a function to load and return the user object based on the user_id
    print("User loader called with user_id:", user_id)  # Debug statement
    print("User.get:", User.get(user_id))
    return User.get(user_id)
 

# Konfiguration für Bild-Uploads
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'  # Pfad zum Speichern der Bilder
configure_uploads(app, photos)


@app.route('/')
def index():
    # Überprüfen Sie, ob der Benutzer authentifiziert ist
    print("INDEX - current user:",current_user)
    print("INDEX - current user auth:",current_user.is_authenticated)
    if current_user.is_authenticated:
        # Wenn ja, rufen Sie die Hauptseite normal auf
        print(current_user)  # Debug statement
        print("INDEX")
        
        print("Next URL stored in session:", session.get('next'))  # Debug statement

        
        plants = Plant.get_all()
        return render_template('plant_overview.html', plants=plants, current_user=current_user)
    else:
        # Wenn der Benutzer nicht authentifiziert ist, speichern Sie die angeforderte URL in der Sitzung und leiten Sie ihn zur Login-Seite weiter
        print("Session before saving next URL:", session)  # Debug statement
        session['next'] = request.path
        print("Session after saving next URL:", session)  # Debug statement

        return redirect(url_for('login'))

@app.route('/add-plant', methods=['POST'])
@login_required
def add_plant():
    name = request.form.get('name')
    description = request.form.get('description')
    image_url = request.form.get('image_url')
    sunlight = request.form.get('sunlight')
    water_needs = request.form.get('water_needs')
    temperature_range = request.form.get('temperature_range')

    # Create a new plant object
    plant = Plant(ObjectId(),name, description, image_url, sunlight, water_needs, temperature_range)
    plant.save()

    return redirect(url_for('index'))


@app.route('/care-journal/<plant_id>', methods=['GET'])
def care_journal(plant_id):
    # Fetch the plant details based on the provided plant_id
    plant = Plant.get_by_id(plant_id)
    # Fetch the care journal entries for the plant from the database
    care_journal_entries = CareJournalEntry.get_entries_by_plant_id(plant_id)
    # Render the care journal template with the plant details and care journal entries
    return render_template('care_journal.html', plant=plant, plant_id=plant_id, care_journal_entries=care_journal_entries)



@app.route('/add-entry/<plant_id>', methods=['POST'])
@login_required
def add_entry(plant_id):
    if request.method == 'POST':
        user_id = current_user.id
        entry_date = request.form.get('entry_date')
        notes = request.form.get('notes')

        # Handle image upload
        if 'image' in request.files:
            image_filename = photos.save(request.files['image'])
            image_url = photos.url(image_filename)
        else:
            image_url = None

        # Erstellen eines neuen Eintrags
        new_entry = CareJournalEntry(ObjectId(), plant_id=ObjectId(plant_id), user_id=user_id, entry_date=entry_date, notes=notes, images=[image_url])
        new_entry.save()

        return redirect(url_for('care_journal', plant_id=plant_id))





@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Login function called")
    
    print("Login route called with method:", request.method)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.get_by_username(username)
        print("User :",user)
        if user and user.check_password(password):
            login_user(user)
            print("User successfully logged in:", current_user)  # Debug statement
            
            # Redirect to the requested URL stored in session or to the index page if there is none
            next_url = session.get('next', None)
            print("Next URL:", next_url)  # Debug statement
            
            if next_url:
                session.pop('next')  # Clear the stored URL from session
                return redirect(next_url)
            else:
                return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.get_by_username(username):
            return render_template('register.html', error='Username already exists')

        user_data = {
            'username': username,
            'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        }
        user = User(user_data)
        user.save()

        login_user(user)
        return redirect(url_for('index'))

    return render_template('register.html')



@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

 
    

if __name__ == '__main__':
    app.run()