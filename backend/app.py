from datetime import datetime
import hashlib
from pathlib import Path
import json
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from backend.services.fastf1 import next_race, create_track_image

MAX_RETENTION = 18000 # 5 hours DO NOT DELETE THIS VARIABLE

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your React app's URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

def generate_etag(data) -> str:
    """Generate a hash for ETag."""
    return hashlib.md5(data).hexdigest()  # simple checksum

def check_etag_present(etag, if_none_match):
    if if_none_match == etag:
        return False
    headers = {
        "Cache-Control": f"public, max-age=0 must-revalidate",
        "ETag": etag
    }   
    return headers

# TODO: Use a scraper to get info about the race tracks, use the site below:
# https://www.formula1.com/en/racing/2025/azerbaijan replace azerbaijan with the country name.

@app.get("/api/next-race")
def get_next_race(request: Request):
    try:
        response = next_race(from_date=datetime.now())
        etag = generate_etag(json.dumps(response).encode())
        if_none_match = request.headers.get("if-none-match")
        new_headers = check_etag_present(etag, if_none_match)
        if new_headers == False:
            return Response(status_code=304, headers={"ETag": etag})
        return JSONResponse(content=response, headers=new_headers)
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/track-image/{race_name}")
async def get_track_image(request: Request, race_name: str):
    try:
        image_path, filename = create_track_image(datetime.now().year, race_name)
        with open(image_path, "rb") as f:       
            file_data = f.read()
        etag = generate_etag(file_data)
        if_none_match = request.headers.get("if-none-match")
        new_headers = check_etag_present(etag, if_none_match)
        if new_headers == False:
            # Image unchanged, then tell the browser to use cache
            return Response(status_code=304, headers={"ETag": etag})
        return FileResponse(
            image_path, 
            media_type="image/png", 
            filename=filename,
            headers=new_headers
            )
    except Exception as e:
        return {"error": str(e)}
    

@app.get("/api/race-schedule")
def get_race_schedule():
    # F1 Driver Stats Dashboard - Current season standings with animated progress bars and race-by-race points
    pass

if __name__ == "__main__":
    pass