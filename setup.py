from models.models import Plant

def add_sample_data():
    # Create and save sample plant documents
    sample_plant1 = Plant(
        name='Sample Plant 1',
        description='This is a sample plant 1',
        image_url='https://example.com/sample_plant1.jpg',
        sunlight='Partial sunlight',
        water_needs='Moderate',
        temperature_range='20-25°C'
    )
    sample_plant1.save()

    sample_plant2 = Plant(
        name='Sample Plant 2',
        description='This is a sample plant 2',
        image_url='https://example.com/sample_plant2.jpg',
        sunlight='Full sunlight',
        water_needs='High',
        temperature_range='25-30°C'
    )
    sample_plant2.save()

    # Add more sample plants as needed

if __name__ == '__main__':
    add_sample_data()
