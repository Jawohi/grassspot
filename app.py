from flask import Flask, render_template, request, redirect, url_for
from models.models import Plant, db
from bson import ObjectId

app = Flask(__name__)
app.config['SECRET_KEY'] = '7763fa0b8072a082a17dd9e52721bb2e'
app.config['MONGO_URI'] = 'mongodb+srv://jawohi_gs:myedMz0mDterDuRl@grasscluster.bcqofix.mongodb.net/Grassspot_DB'



@app.route('/')
def index():
    plants = Plant.get_all()
    return render_template('plant_overview.html', plants=plants)

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

    

if __name__ == '__main__':
    app.run()