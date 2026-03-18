from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from pymongo import MongoClient
from django.conf import settings

# Sample data for superheroes, teams, activities, leaderboard, workouts
data = {
    "users": [
        {"name": "Clark Kent", "email": "superman@dc.com", "team": "DC"},
        {"name": "Bruce Wayne", "email": "batman@dc.com", "team": "DC"},
        {"name": "Diana Prince", "email": "wonderwoman@dc.com", "team": "DC"},
        {"name": "Tony Stark", "email": "ironman@marvel.com", "team": "Marvel"},
        {"name": "Steve Rogers", "email": "captainamerica@marvel.com", "team": "Marvel"},
        {"name": "Natasha Romanoff", "email": "blackwidow@marvel.com", "team": "Marvel"},
    ],
    "teams": [
        {"name": "Marvel", "members": ["Tony Stark", "Steve Rogers", "Natasha Romanoff"]},
        {"name": "DC", "members": ["Clark Kent", "Bruce Wayne", "Diana Prince"]},
    ],
    "activities": [
        {"user": "Clark Kent", "activity": "Flight", "duration": 60},
        {"user": "Tony Stark", "activity": "Weight Lifting", "duration": 45},
        {"user": "Diana Prince", "activity": "Sword Training", "duration": 30},
    ],
    "leaderboard": [
        {"user": "Clark Kent", "points": 100},
        {"user": "Tony Stark", "points": 90},
        {"user": "Diana Prince", "points": 80},
    ],
    "workouts": [
        {"name": "Super Strength", "description": "Heavy lifting and resistance training."},
        {"name": "Agility", "description": "Speed and flexibility drills."},
    ]
}

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop collections if they exist
        for collection in data.keys():
            db[collection].drop()

        # Insert data
        for collection, docs in data.items():
            db[collection].insert_many(docs)

        # Ensure unique index on email for users
        db['users'].create_index([('email', 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
