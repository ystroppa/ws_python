""" 
Script to parse course information from courses.json, create the appropriate databases and
collection(s) on a local instance of MongoDB, create the appropriate indices (for efficient retrieval)
and finally add the course data on the collection(s).
Adaptation du script pour la prise en compte des aspects d'authentification de la base mongodb
"""

import pymongo
import json

# Connect to MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/',
                     username='but3',
                     password='but3',
                     authSource='courses',
                     authMechanism='SCRAM-SHA-1')

db = client["courses"]
collection = db["courses"]

# Read courses from courses.json
with open("courses.json", "r") as f:
    courses = json.load(f)

# Create index for efficient retrieval
collection.create_index("name")

# add rating field to each course
for course in courses:
    course['rating'] = {'total': 0, 'count': 0}
    
# add rating filed to each chapter
for course in courses:
    for chapter in course['chapters']:
        chapter['rating'] = {'total': 0, 'count': 0}

# Add courses to collection
for course in courses:
    collection.insert_one(course)

# Close MongoDB connection
client.close()
