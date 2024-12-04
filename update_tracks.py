import tkinter as tk  # Importing Tkinter for GUI
from tkinter import ttk  # Importing ttk for styled widgets
from track_library import library, save_library, list_tracks  # Importing functions and data from track_library
import os  # Importing os module to interact with the operating system

class UpdateTracks:
    def __init__(self, window):  # Constructor for UpdateTracks class
        self.window = window  # Assigning window parameter to instance
        self.window.title("Update Tracks")  # Setting window title
        self.window.geometry("900x400")  # Setting window size
        
        go_back_btn = tk.Button(window, text="Go Back", command=lambda: self.go_back(window))  # Go back button
        go_back_btn.grid(row=0, column=2, sticky="e", padx=10, pady=5)  # Positioning the button

        columns = ("ID", "Song Name", "Artist", "Rating", "Play Count")  # Defining columns for Treeview
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=15)  # Creating Treeview widget
        self.tree.grid(row=1, column=0, rowspan=6, padx=10, pady=10)  # Positioning Treeview

        for col in columns:  # Looping through columns to set headers and column width
            self.tree.heading(col, text=col)  # Setting column headers
            self.tree.column(col, width=120, anchor="center")  # Setting column width and alignment

        self.tree.bind("<<TreeviewSelect>>", self.on_select)  # Binding selection event to on_select method

        validate_numeric = self.window.register(self.validate_numeric)  # Registering validation function for numeric entries

        tk.Label(self.window, text="ID:").grid(row=1, column=1, sticky="w", padx=10, pady=5)  # Label for ID field
        self.id_entry = tk.Entry(self.window, width=20, validate="key", validatecommand=(validate_numeric, "%P"))  # Entry field for ID
        self.id_entry.grid(row=1, column=2, sticky="w", padx=10)  # Positioning ID entry

        tk.Label(self.window, text="Artist:").grid(row=2, column=1, sticky="w", padx=10, pady=5)  # Label for Artist field
        self.artist_entry = tk.Entry(self.window, width=20)  # Entry field for Artist
        self.artist_entry.grid(row=2, column=2, sticky="w", padx=10)  # Positioning Artist entry

        tk.Label(self.window, text="Rating (1-5):").grid(row=3, column=1, sticky="w", padx=10, pady=5)  # Label for Rating field
        self.rating_entry = tk.Entry(self.window, width=20, validate="key", validatecommand=(validate_numeric, "%P"))  # Entry field for Rating
        self.rating_entry.grid(row=3, column=2, sticky="w", padx=10)  # Positioning Rating entry

        self.update_btn = tk.Button(self.window, text="Update", command=self.update_track)  # Button to update track
        self.update_btn.grid(row=4, column=2, sticky="w", padx=10, pady=10)  # Positioning Update button

        self.status_label = tk.Label(self.window, text="", fg="green")  # Label to show status messages
        self.status_label.grid(row=5, column=1, columnspan=2)  # Positioning Status label

        self.refresh_track_list()  # Refreshing the track list when the window is created

    def refresh_track_list(self):  # Method to refresh the list of tracks in the Treeview
        self.tree.delete(*self.tree.get_children())  # Deleting existing Treeview entries
        for file, info in library.items():  # Looping through the library
            song_name = file.replace(".mp3", "")  # Extracting song name by removing .mp3
            self.tree.insert("", "end", values=(  # Inserting new row into Treeview
                info["id"], song_name, info["artist"], info["rating"], info.get("play_count", 0)
            ))

    def on_select(self, event):  # Method called when a track is selected in the Treeview
        selected_item = self.tree.selection()  # Getting selected item
        if selected_item:  # If a track is selected
            values = self.tree.item(selected_item, "values")  # Retrieving selected track values
            self.id_entry.delete(0, tk.END)  # Clearing the ID entry field
            self.id_entry.insert(0, values[0])  # Inserting selected ID into the field
            self.artist_entry.delete(0, tk.END)  # Clearing the Artist entry field
            self.artist_entry.insert(0, values[2])  # Inserting selected Artist into the field
            self.rating_entry.delete(0, tk.END)  # Clearing the Rating entry field
            self.rating_entry.insert(0, values[3])  # Inserting selected Rating into the field

    def update_track(self):  # Method to update the selected track
        selected_item = self.tree.selection()  # Getting selected item
        if selected_item:  # If a track is selected
            values = self.tree.item(selected_item, "values")  # Retrieving selected track values
            file_name = f"{values[1]}.mp3"  # Constructing file name based on song name

            new_id = self.id_entry.get().strip()  # Getting new ID from entry

            if any(info['id'] == new_id for track, info in library.items() if track != file_name):  # Checking if ID already exists
                self.status_label.config(text="The ID is already used.", fg="red")  # Showing error message
                return

            library[file_name] = {  # Updating track information in the library
                "id": new_id,
                "artist": self.artist_entry.get(),
                "rating": int(self.rating_entry.get()),
                "play_count": library[file_name].get("play_count", 0),
            }
            save_library()  # Saving updated library

            self.refresh_track_list()  # Refreshing the track list
            self.status_label.config(text="Track updated successfully!", fg="green")  # Success message
        else:
            self.status_label.config(text="No track selected.", fg="red")  # Error message if no track is selected

    def validate_numeric(self, input_value):  # Validation function for numeric input
        if input_value == "" or input_value.isdigit():  # Allowing empty or numeric input
            return True
        return False
    
    def go_back(self, window):  # Method to close current window and open track player
        window.destroy()  # Destroying current window
        try:
            os.system("python track_player.py")  # Running track_player.py
        except Exception as e:  # Catching exceptions if track_player.py fails
            print(f"Error launching track_player.py: {e}")

if __name__ == "__main__":  # Main block to run the program
    root = tk.Tk()  # Creating Tkinter window
    app = UpdateTracks(root)  # Creating UpdateTracks object
    root.mainloop()  # Running the main loop

