import json  # Importing the json module to handle JSON data
import os  # Importing the os module to interact with the operating system

track_folder = "Tracks"  # Folder where the track files are stored
data_file = "track_data.json"  # File where track data is saved
library = {}  # Initialize an empty dictionary to store track data

def load_library():  # Function to load track data from the JSON file
    global library  # Use the global library variable
    if os.path.exists(data_file):  # Check if the data file exists
        with open(data_file, "r") as f:  # Open the data file in read mode
            library = json.load(f)  # Load the JSON data into the library dictionary
    else:
        library = {}  # If no data file, initialize an empty dictionary

def save_library():  # Function to save track data to the JSON file
    with open(data_file, "w") as f:  # Open the data file in write mode
        json.dump(library, f, indent=4)  # Write the library dictionary to the file with indentation

def list_tracks():  # Function to list all the MP3 tracks in the folder
    files = [f for f in os.listdir(track_folder) if f.endswith(".mp3")]  # Get all MP3 files in the track folder
    for file in files:  # Loop through each track file
        if file not in library:  # If the track is not in the library
            library[file] = {"id": "", "artist": "", "rating": 0}  # Add the track with empty data
    save_library()  # Save the updated library to the data file
    return files  # Return the list of MP3 files

load_library()  # Load the existing track data when the program starts
list_tracks()  # List the tracks and update the data
