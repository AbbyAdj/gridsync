import os
from pathlib import Path
from datetime import datetime
import fastf1
from fastf1.core import Session
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from backend.models.race_models import NextRace, Session


def next_race(from_date: datetime) -> dict:
    """
        example of the returning json:
        {
            "race_name": "Abu Dhabi Grand Prix",
            "location": "Yas Marina Circuit",
            "country": "UAE", 
            "race_date": "2024-12-08T17:00:00Z",
            "sessions": [
                {"name": "Practice 1", "datetime": "2024-12-06T10:30:00Z"},
                {"name": "Practice 2", "datetime": "2024-12-06T14:00:00Z"},
                {"name": "Practice 3", "datetime": "2024-12-07T11:30:00Z"},
                {"name": "Qualifying", "datetime": "2024-12-07T15:00:00Z"},
                {"name": "Race", "datetime": "2024-12-08T17:00:00Z"}
            ]
        }
    """
    remaining_races = fastf1.get_events_remaining(dt=from_date)
    remaining_races_df = pd.DataFrame(remaining_races)
    next_race_df = remaining_races_df.head(1)
    next_race_formatted = convert_to_next_race_object(next_race_df)
    return next_race_formatted


def convert_datetime_to_string(df: pd.DataFrame, column_name: str) -> str:
    date_obj = df[column_name].iloc[0].to_pydatetime()
    return str(date_obj)
    

def convert_to_next_race_object(df: pd.DataFrame)-> dict:
    practice_1 = Session(name="Practice 1", datetime=convert_datetime_to_string(df, "Session1DateUtc"))
    practice_2 = Session(name="Practice 2", datetime=convert_datetime_to_string(df, "Session2DateUtc"))
    practice_3 = Session(name="Practice 3", datetime=convert_datetime_to_string(df, "Session3DateUtc"))
    qualifying = Session(name="Qualifying", datetime=convert_datetime_to_string(df, "Session4DateUtc"))
    race = Session(name="Grand Prix", datetime=convert_datetime_to_string(df, "Session5DateUtc"))
    
    formatted_df = NextRace(
        race_name=df["EventName"].iloc[0],
        location=df["Location"].iloc[0],
        country=df["Country"].iloc[0],
        race_date=convert_datetime_to_string(df, "Session5DateUtc"),
        sessions=[
            practice_1,
            practice_2,
            practice_3,
            qualifying,
            race
        ]
    )
    return formatted_df.model_dump()


def create_track_image(year:int, identifier: str, session_type: str = "Q"):
    if year == datetime.now().year:
        year -= 1
    cache_dir = create_img_directory("static/track_cache")

    image_path, image_filename = create_img_file_path(cache_dir, year, identifier, session_type)

    if image_path.exists():
        return image_path, image_filename
    
    session = fastf1.get_session(year, identifier, session_type)
    session.load()
    
    track = None
    track_angle = None

    lap = session.laps.pick_fastest()
    if lap is not None:
        pos = lap.get_pos_data()
        track = pos.loc[:, ['X', 'Y']].to_numpy()

    circuit_info = session.get_circuit_info()
    if circuit_info is not None:
        track_angle = circuit_info.rotation / 180 * np.pi

    # if track != None and track_angle != None:
    rotated_track = rotate(track, angle=track_angle)
    plt.plot(rotated_track[:, 0], rotated_track[:, 1], color="black", linewidth=5.5)

    save_track_image(str(image_path))
    return image_path, image_filename


def create_img_directory(path: str):
    # Create cache directory
    cache_dir = Path(path)
    try:
        cache_dir.mkdir(parents=True)
    except FileExistsError as e:
        pass
    finally:
        return cache_dir

def create_img_file_path(cache_dir: Path, year:int, identifier:str, session_type: str):
    # Create unique filename
    cache_key = f"{year}_{identifier}_{session_type}"
    image_filename = f"{cache_key}.png"
    image_path = cache_dir / image_filename
 
    return image_path, image_filename


def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)

def save_track_image(img_name: str):
    ax = plt.gca()  # get current axes
    ax.axis('off')
    plt.xticks([])
    plt.yticks([])
    plt.axis('equal')
    plt.savefig(img_name, bbox_inches='tight', pad_inches=0, 
                transparent=True, facecolor='none')
    plt.close()


if __name__ == "__main__":
    x = Session(name="hey", datetime=str(datetime.now()))
    print(x.model_dump())