import tkinter as tk  # Import tkinter for GUI
import pygame  # Import pygame for audio stuffs
from track_library import library, list_tracks, save_library  # Import custom library functions
import os  # Importing os module to interact with the operating system

class CreateTrackList:  
    def __init__(self, window):  # Initialize with the window parameter
        self.window = window  # Set the window for GUI
        self.window.title("Create Track List")  # Set window title
        self.window.geometry("900x600")  # Set window size
        
        pygame.init()  # Initialize pygame
        pygame.mixer.init()  # Initialize pygame mixer for audio

        self.playlist = []  # Initialize empty playlist
        self.current_track_index = -1  # Set initial track index to -1
        self.is_playing = False  # Set initial play status to False
        self.track_length = 0  # Initialize track length
        self.current_time = 0  # Initialize current time of track

        self.go_back_btn = tk.Button(window, text="Go Back", command=self.go_back)  # Create Go Back button
        self.go_back_btn.place(relx=0.95, rely=0.02, anchor="ne")  # Place Go Back button on screen

        tk.Label(window, text="Enter Track ID:").pack(pady=5)  # Label to prompt track ID input

        self.id_var = tk.StringVar()  # Create a StringVar for tracking user input
        self.id_var.trace_add("write", self.validate_id_input)  # Add validation on ID input
        self.id_entry = tk.Entry(window, textvariable=self.id_var, width=50)  # Create input field for ID
        self.id_entry.pack(pady=5)  # Place ID input field

        self.add_btn = tk.Button(window, text="Add to Playlist", command=self.add_to_playlist)  # Add button
        self.add_btn.pack(pady=5)  # Place Add button

        self.clear_btn = tk.Button(window, text="Clear Playlist", command=self.clear_playlist)  # Clear button
        self.clear_btn.pack(pady=5)  # Place Clear button

        self.notification_label = tk.Label(window, text="", fg="red")  # Label for notifications
        self.notification_label.pack(pady=5)  # Place notification label

        self.playlist_text = tk.Text(window, height=10, width=100, state="disabled")  # Text widget for playlist
        self.playlist_text.pack(pady=10)  # Place playlist text display

        self.play_btn = tk.Button(window, text="Play Playlist", command=self.play_playlist)  # Play button
        self.play_btn.pack(pady=5)  # Place Play button

        self.controls_frame = tk.Frame(window)  # Create a frame for control buttons
        self.controls_frame.pack(pady=10)  # Place control frame

        self.timer_label = tk.Label(self.controls_frame, text="00:00")  # Label for current time
        self.timer_label.grid(row=0, column=0, padx=10)  # Place timer label

        self.progress_frame = tk.Frame(self.controls_frame)  # Frame for progress bar
        self.progress_frame.grid(row=0, column=1, padx=10)  # Place progress frame
        self.progress_bar = tk.Canvas(self.progress_frame, width=400, height=10, bg="white")  # Canvas for progress bar
        self.progress_bar.pack(side="left")  # Place progress bar
        self.progress_marker = self.progress_bar.create_line(0, 0, 0, 10, fill="red", width=3)  # Red marker for progress
        

        self.track_length_label = tk.Label(self.controls_frame, text="00:00")  # Label for total track length
        self.track_length_label.grid(row=0, column=2, padx=10)  # Place track length label

        self.go_back_btn = tk.Button(self.controls_frame, text="Back", command=self.back)  # Back button in controls
        self.go_back_btn.grid(row=1, column=0, pady=10)  # Place Back button

        self.pause_play_btn = tk.Button(self.controls_frame, text="Pause", command=self.pause_or_play)  # Pause/Play button
        self.pause_play_btn.grid(row=1, column=1, pady=10)  # Place Pause/Play button

        self.next_btn = tk.Button(self.controls_frame, text="Next", command=self.next_track)  # Next button
        self.next_btn.grid(row=1, column=2, pady=10)  # Place Next button

        self.update_timer()  # Start updating timer

    def validate_id_input(self, *args):  # Function to validate ID input
        current_input = self.id_var.get()  # Get current input
        if not current_input.isdigit():  # Check if input is not a digit
            self.id_var.set("".join(filter(str.isdigit, current_input)))  # Remove non-digit characters

    def add_to_playlist(self):  # Function to add track to playlist
        track_id = self.id_entry.get().strip()  # Get track ID from input field
        self.notification_label.config(text="")  # Clear notification
        for track, info in library.items():  # Iterate through library
            if info['id'] == track_id:  # If track ID matches
                self.playlist.append((track, info))  # Add track to playlist
                self.update_playlist_display()  # Update playlist display
                return
        self.notification_label.config(text="ID not found. Please enter a valid ID.")  # Invalid ID message

    def clear_playlist(self):  # Function to clear playlist
        self.playlist = []  # Reset playlist
        self.update_playlist_display()  # Update playlist display
        if self.is_playing:  # If currently playing
            pygame.mixer.music.stop()  # Stop music
            self.is_playing = False  # Set playing status to False
            self.pause_play_btn.config(text="Play")  # Change button text to Play

    def update_playlist_display(self):  # Function to update playlist display
        self.playlist_text.config(state="normal")  # Enable text widget
        self.playlist_text.delete(1.0, tk.END)  # Clear existing playlist display
        for i, (track, info) in enumerate(self.playlist, start=1):  # Iterate through playlist
            file_name = os.path.splitext(track)[0]  # Get track name without extension
            artist = info.get("artist", "Unknown Artist")  # Get artist name
            rating = "*" * info.get("rating", 0)  # Get rating as stars
            self.playlist_text.insert(tk.END, f"{i}. {info['id']} {file_name} by {artist} {rating}\n")  # Display track info
        self.playlist_text.config(state="disabled")  # Disable text widget for editing

    def play_playlist(self):  # Function to play the playlist
        if not self.playlist:  # If playlist is empty
            self.notification_label.config(text="Playlist is empty!")  # Display error message
            return
        self.current_track_index = 0  # Start from the first track
        self.play_track(self.current_track_index)  # Play first track

    def play_track(self, index):  # Function to play a specific track
        if index < 0 or index >= len(self.playlist):  # Check if index is valid
            return
        track_path = os.path.join("Tracks", self.playlist[index][0])  # Get track path
        if os.path.exists(track_path):  # If track file exists
            pygame.mixer.music.load(track_path)  # Load track
            pygame.mixer.music.play()  # Play track
            self.track_length = pygame.mixer.Sound(track_path).get_length()  # Get track length
            self.is_playing = True  # Set play status to True
            self.increment_play_count(self.playlist[index][0])  # Increment play count

        else:
            self.notification_label.config(text="Track file not found!")  # Display error if file not found

    def increment_play_count(self, track_name):  # Function to increment play count
        if track_name in library:  # If track is in library
            library[track_name]['play_count'] = library[track_name].get('play_count', 0) + 1  # Increment play count
            save_library()  # Save updated library

    def back(self):  # Function to play the previous track
        if self.current_track_index > 0:  # If not at the first track
            self.current_track_index -= 1  # Move to previous track
            self.play_track(self.current_track_index)  # Play previous track

    def pause_or_play(self):  # Function to toggle between pause and play
        if self.is_playing:  # If currently playing
            pygame.mixer.music.pause()  # Pause music
            self.is_playing = False  # Set play status to False
            self.pause_play_btn.config(text="Play")  # Change button text to Play
        else:
            pygame.mixer.music.unpause()  # Unpause music
            self.is_playing = True  # Set play status to True
            self.pause_play_btn.config(text="Pause")  # Change button text to Pause

    def next_track(self):  # Function to play the next track
        if self.current_track_index < len(self.playlist) - 1:  # If not the last track
            self.current_track_index += 1  # Move to next track
            self.play_track(self.current_track_index)  # Play next track
        else:
            self.current_track_index = 0  # Loop back to first track
            self.play_track(self.current_track_index)  # Play first track

    def update_timer(self):  # Function to update the timer
        if self.is_playing:  # If currently playing
            self.current_time = pygame.mixer.music.get_pos() // 1000  # Get current time in seconds
            minutes, seconds = divmod(self.current_time, 60)  # Convert to minutes and seconds
            total_minutes, total_seconds = divmod(self.track_length, 60)  # Get total track length
            self.timer_label.config(text=f"{minutes:02}:{seconds:02}")  # Update current time label
            self.track_length_label.config(text=f"{int(total_minutes):02}:{int(total_seconds):02}")  # Update track length label
            progress_ratio = self.current_time / self.track_length if self.track_length else 0  # Calculate progress ratio
            self.progress_bar.coords(self.progress_marker, 400 * progress_ratio, 0, 400 * progress_ratio, 10)  # Update progress bar
        self.window.after(500, self.update_timer)  # Update timer every 500ms

    

    def go_back(self):  # Function to go back to the previous screen
        if self.is_playing:  # If currently playing
            pygame.mixer.music.stop()  # Stop music
            self.is_playing = False  # Set play status to False
            self.pause_play_btn.config(text="Play")  # Change button text to Play
        self.window.destroy()  # Close current window
        os.system("python track_player.py")  # Launch track_player.py script

if __name__ == "__main__":  # If running as main program
    root = tk.Tk()  # Create a Tkinter window
    app = CreateTrackList(root)  # Initialize the CreateTrackList app
    root.mainloop()  # Start Tkinter event loop

