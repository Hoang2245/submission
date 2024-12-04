import tkinter as tk  # Import Tkinter for GUI
import os  # Import os module for interacting with the operating system
import font_manager as fonts  # Import custom font manager 

def close_program():  
    window.destroy()  # Function to close the window

def create_track_list_clicked():  
    close_program()  # Close the window
    os.system("python create_track_list.py")  # Execute 'create_track_list.py' script

def update_tracks_clicked():  
    close_program()  # Close the window
    os.system("python update_tracks.py")  # Execute 'update_tracks.py' script

window = tk.Tk()  # Create a  window object
window.geometry("500x300")  # Set the window size 
window.title("JukeBox")  # Set the window title to "JukeBox"

fonts.configure()  # Configure fonts (custom font management)

header_lbl = tk.Label(  # Create a label widget
    window, text="Select an option by clicking one of the buttons below"  # Set the label text
)
header_lbl.grid(padx=10, pady=10)  # Place the label on the grid with padding

create_track_list_btn = tk.Button(  # Create a button widget for creating track list
    window, text="Create Track List", command=create_track_list_clicked  # Set text and command
)
create_track_list_btn.grid(pady=20)  # Place the button on the grid with padding

update_tracks_btn = tk.Button(  # Create a button widget for updating tracks
    window, text="Update Tracks", command=update_tracks_clicked  # Set text and command
)
update_tracks_btn.grid(pady=20)  # Place the button on the grid with padding

window.mainloop()  # Start the Tkinter event loop

