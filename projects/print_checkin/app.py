import tkinter as tk
from tkinter import filedialog, ttk
import subprocess
import os
# Import the modified overlay_stickers function
from overlay_stickers import run_overlay_stickers

class OverlayApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Schedule Overlay Application")
        self.schedule_file_path = None
        self.selected_file = tk.StringVar()
        self.status_label = tk.Label(self, text="")
        self.status_label.pack(pady=5)
        self.create_widgets()

    def create_widgets(self):
        # Button to upload the schedule
        upload_button = tk.Button(self, text="Upload Schedule", command=self.upload_schedule)
        upload_button.pack(pady=10)

        # Button to run the script
        run_button = tk.Button(self, text="Run", command=self.run_script)
        run_button.pack(pady=10)

        # Dropdown menu for selecting a file
        self.update_file_dropdown()
        file_dropdown = ttk.Combobox(self, textvariable=self.selected_file, state="readonly")
        file_dropdown.pack(pady=10)

        # Button to open the selected file
        open_button = tk.Button(self, text="Open Selected File", command=self.open_file)
        open_button.pack(pady=10)

    def upload_schedule(self):
        self.schedule_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.schedule_file_path:
            print("Selected file:", self.schedule_file_path)

    def run_script(self):
        if self.schedule_file_path:
            run_overlay_stickers(self.schedule_file_path)
            self.status_label.config(text="PDF files processed. You can open them now.")
            self.update_file_dropdown()
        else:
            print("No schedule file selected")

    def update_file_dropdown(self):
        output_dir = 'output'  # Directory where PDFs are stored
        if os.path.exists(output_dir):
            files = [f for f in os.listdir(output_dir) if f.endswith('.pdf')]
            self.selected_file.set(files[0] if files else '')
            self.dropdown_menu = ttk.Combobox(self, values=files, textvariable=self.selected_file, state="readonly")
            self.dropdown_menu.pack(pady=10)
        else:
            print("Output directory does not exist.")

    def open_file(self):
        file_path = os.path.join('output', self.selected_file.get())
        if file_path and os.path.exists(file_path):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(file_path)
                else:  # macOS, Linux, Unix etc.
                    subprocess.call(['open', file_path] if os.name == 'posix' else ['xdg-open', file_path])
            except Exception as e:
                print(f"Error opening file: {e}")
        else:
            print("File does not exist or path is incorrect.")

# Creating and running the application
app = OverlayApplication()
app.mainloop()
