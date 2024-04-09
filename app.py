from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from models.models import Plant, CareJournalEntry, db
from models.user import User
from bson import ObjectId
from datetime import datetime
import bcrypt


app = Flask(__name__)

app.config['SECRET_KEY'] = '7763fa0b8072a082a17dd9e52721bb2e'
app.config['MONGO_URI'] = 'mongodb+srv://jawohi_gs:myedMz0mDterDuRl@grasscluster.bcqofix.mongodb.net/Grassspot_DB'

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    # Implement a function to load and return the user object based on the user_id
    return User.get(user_id)
 


@app.route('/')
def index():
    print(current_user)  # Debug statement
    plants = Plant.get_all()
    return render_template('plant_overview.html', plants=plants, current_user=current_user)

@app.route('/add-plant', methods=['POST'])
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
    return render_template('care_journal.html', plant=plant, care_journal_entries=care_journal_entries)

@app.route('/add-entry/<plant_id>', methods=['GET', 'POST'])
@login_required
def add_entry(plant_id):
    if request.method == 'POST':
        # Get form data
        user_id = current_user._id
        entry_date = datetime.now().isoformat()
        notes = request.form.get('notes')
        # Handle image upload if needed
        
        # Create a new entry object
        new_entry = CareJournalEntry(plant_id=ObjectId(plant_id), user_id=user_id, entry_date=entry_date, notes=notes)
        new_entry.save()
        return redirect(url_for('view_care_journal', plant_id=plant_id))

    # Render the care_journal.html template with the add entry modal open
    return render_template('care_journal.html', plant_id=plant_id, show_add_entry_modal=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.get_by_username(username)
        if user and user.check_password(password):
            login_user(user)
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



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

 
    

if __name__ == '__main__':
    app.run()