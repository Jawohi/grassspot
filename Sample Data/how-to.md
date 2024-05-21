Die Files im Sample Data können zum Testen der Anwendung verwendet werden bzw. durch eigne Daten ersetzt werden.


Für die Generierung eigner Test-Einträge kann man diesem Schema folgen, bei _id handelt es sich um eine objectID die von MongoDB erzeugt wird wenn man Daten in die Datenbank hineinlädt.

Beispiel für eine Pflanze:
{
  "_id": {
    "$oid": "647db5f5fb73c14c308af04c"
  },
  "name": "Rose",
  "description": "A beautiful flowering plant known for its captivating scent.",
  "image_url": "https://example.com/rose.jpg",
  "sunlight": "Full sunlight",
  "water_needs": "Moderate",
  "temperature_range": "15-25°C",
  "status": "active"
}


Beispiel für einen Pflegeeintrag:
{
  "_id": {
    "$oid": "661d02486303d5e204e275ee"
  },
  "plant_id": {
    "$oid": "647db5f5fb73c14c308af054"
  },
  "user_id": "66196b7ba20cc7084a659114",
  "entry_date": {
    "$date": "2024-04-15T00:00:00.000Z"
  },
  "notes": "Äste gestutzt",
  "images": [
    "images/plant.jpg"
  ],
  "status": "active"
}

Beispiel für einen User:
{
  "_id": {
    "$oid": "66196b7ba20cc7084a659114"
  },
  "username": "test2",
  "password": {
    "$binary": {
      "base64": "JDJiJDEyJFpzQXJWWFk0T3RTVzdiWFV2cy5BZS5mazNieDlYUnpDY3lkOG41ZTZnSUouMmlxdk9TNmtx",
      "subType": "00"
    }
  },
  "status": "active"
}
