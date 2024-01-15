from typing import List, Optional
from ninja import HTTPException, Router, File
from ninja.files import UploadedFile
from tracks.models import Track
from tracks.schema import TrackSchema, NotFoundSchema

api = Router()

@api.get("/tracks", response=List[TrackSchema])
def tracks(request, title: Optional[str] = None):
    try:
        if title:
            return Track.objects.filter(title__icontains=title)
        return Track.objects.all()
    except Track.DoesNotExist as e:
        raise HTTPException(status_code=404, detail="No tracks found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api.get("/tracks/{track_id}", response={200: TrackSchema, 404: NotFoundSchema})
def track(request, track_id: int):
    try:
        track = Track.objects.get(pk=track_id)
        return 200, track
    except Track.DoesNotExist as e:
        raise HTTPException(status_code=404, detail="Track does not exist")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api.post("/tracks", response={201: TrackSchema})
def create_track(request, track: TrackSchema):
    try:
        track = Track.objects.create(**track.dict())
        return 201, track
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api.put("/tracks/{track_id}", response={200: TrackSchema, 404: NotFoundSchema})
def change_track(request, track_id: int, data: TrackSchema):
    try:
        track = Track.objects.get(pk=track_id)
        for attribute, value in data.dict().items():
            setattr(track, attribute, value)
        track.save()
        return 200, track
    except Track.DoesNotExist as e:
        raise HTTPException(status_code=404, detail="Track does not exist")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api.delete("/tracks/{track_id}", response={200: None, 404: NotFoundSchema})
def delete_track(request, track_id: int):
    try:
        track = Track.objects.get(pk=track_id)
        track.delete()
        return 200
    except Track.DoesNotExist as e:
        raise HTTPException(status_code=404, detail="Track not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api.post("/upload", url_name='upload')
def upload(request, file: UploadedFile = File(...)):
    try:
        data = file.read().decode()
        return {
            'name': file.name,
            'data': data
        }
    except UnicodeDecodeError as e:
        raise HTTPException(status_code=400, detail="Invalid file format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
