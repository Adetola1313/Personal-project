After considering various options, I decided to go with Mongo DB, which is a document database that stores data in a type of JSON format called BSON. BSON is a binary format that extends the capabilities of JSON by providing additional data types, such as binary data and date objects, that are not natively supported in JSON.

According to this website [tutorialspoint](https://www.tutorialspoint.com/mongodb/mongodb_data_modeling.htm#:~:text=MongoDB%20provides%20two%20types%20of,model%20and%20Normalized%20data%20model.), Mongo DB has two types of data models, and they are:

### Embedded Data Model:

In this model, related data are stored in a single document as nested fields. It is useful when there is a one-to-one or one-to-many relationships between entities.

```
{
  "_id": ObjectId("615b9a63d3c3c02ab836f712"),
  "name": "John Doe",
  "age": 21,
  "university": "University of Oxford",
  "course": {
    "name": "Computer Science",
    "code": "CSC101",
    "year": 3
  },
  "grades": {
    "CSC101": {
      "midterm": 90,
      "final": 85,
      "project": 95
    },
    "CSC102": {
      "midterm": 80,
      "final": 90,
      "project": 85
    }
  },
  "address": {
    "street": "1 Oxford Street",
    "city": "Oxford",
    "postcode": "OX1 2JD"
  }
}
```

### Normalized Data Model:

In this model, related data are separated into different collections and linked using references. It is useful when there is a many-to-many relationship between entities.

Student Collection:

```
{
  "_id": ObjectId("615b9a63d3c3c02ab836f712"),
  "name": "John Doe",
  "age": 21,
  "university": "University of Oxford",
  "address_id": ObjectId("615ba4b4d3c3c02ab836f713"),
  "courses": [ObjectId("615ba5aed3c3c02ab836f716"), ObjectId("615ba5aed3c3c02ab836f717")],
  "grades": [ObjectId("615ba5aed3c3c02ab836f718"), ObjectId("615ba5aed3c3c02ab836f719")]
}
```

Address Collection:
```
{
  "_id": ObjectId("615ba4b4d3c3c02ab836f713"),
  "street": "1 Oxford Street",
  "city": "Oxford",
  "postcode": "OX1 2JD"
}
```

Course Collection:
```
{
  "_id": ObjectId("615ba5aed3c3c02ab836f716"),
  "name": "Computer Science",
  "code": "CSC101",
  "year": 3
}
{
  "_id": ObjectId("615ba5aed3c3c02ab836f717"),
  "name": "Some other course",
  "code": "CSC102",
  "year": 2
}
```

Grade Collection:
```
{
  "_id": ObjectId("615ba5aed3c3c02ab836f718"),
  "student_id": ObjectId("615b9a63d3c3c02ab836f712"),
  "course_id": ObjectId("615ba5aed3c3c02ab836f716"),
  "midterm": 90,
  "final": 85,
  "project": 95
}
{
  "_id": ObjectId("615ba5aed3c3c02ab836f719"),
  "student_id": ObjectId("615b9a63d3c3c02ab836f712"),
  "course_id": ObjectId("615ba5aed3c3c02ab836f717"),
  "midterm": 80,
  "final": 90,
  "project": 85
}
```
MONGO DB COMMUNITY EDITION INSTALLATION
---------------------------------------

1.  Download the installer from [this website](https://www.mongodb.com/try/download/community?tck=docs_server), specifying the OS and version needed.
2.  Open the installer and follow through the installation wizard while leaving default settings.
3.  The installer will install a MongoDB server along with MongoDB Compass, a query editor for MongoDB.
4.  The installed MongoDB comes with three databases: admin, config, and local.

Python Code for Data Modeling in MongoDB
----------------------------------------
```
#Importing needed libraries 

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd

#Mongo database uri
uri = "mongodb://localhost:27017"

#This gives us the ability to interact with a MongoDB instance.
client = MongoClient(uri, server_api=ServerApi('1'))

#creates a pollution-db2 database if it doesnt exist
db = client["pollution-db2"]

#create a collection for Brislington Depot if it deosnt exist
brislington_depot = db["Brisling ton Depot"]

#reads in the file as a dataframe
df = pd.read_csv('clean.csv',low_memory=False)

#select rows where the siteID is 203 because the task asked to Model the data for a specific #monitor (station)  and the chosen station is brislington depot
df = df[df['SiteID'] == 203]


# loop through rows in dataframe and insert documents into MongoDB
for _, row in df.iterrows():
    doc = {
        "DateTime": row['Date Time'],
        "station": {
            "stationId": row['SiteID'],
            "geoPoint2d": row['geo_point_2d'],
            "location": row['Location']
        },
        "NOx": row['NOx'],
        "NO2": row['NO2'],
        "NO": row['NO'],
        "PM10": row['PM10'],
        "NVPM10": row['NVPM10'],
        "VPM10": row['VPM10'],
        "NVPM2_5": row['NVPM2.5'],
        "PM2_5": row['PM2.5'],
        "VPM2_5": row['VPM2.5'],
        "CO": row['CO'],
        "O3": row['O3'],
        "SO2": row['SO2'],
        "Temperature": row['Temperature'],
        "RH": row['RH'],
        "AirPressure": row['Air Pressure'],
        "InstrumentType": row['Instrument Type']
    }
    brislington_depot.insert_one(doc)

```
#This fetches 5 documents and print them iteratively
```
result = brislington_depot.find().limit(5)
for doc in result:
    print(doc)
```