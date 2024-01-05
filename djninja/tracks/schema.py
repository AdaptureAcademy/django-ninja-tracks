from datetime import datetime
from ninja import Schema, ModelSchema
from ninja.orm import create_schema
from tracks.models import Track

TrackSchema = create_schema(Track, fields=['title', 'last_play', 'artist', 'duration'])

class NotFoundSchema(Schema):
    message: str