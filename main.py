import os
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from urllib.parse import urljoin
import threading
import time
from ttkthemes import ThemedTk

# Global variables to handle pause/resume and stop the process
is_paused = False
stop_thread = False

def log_func(text):
    """Function to update the log in real-time."""
    log_textbox.insert(tk.END, text)
    log_textbox.see(tk.END)  # Scroll to the end to show the latest log entry
    window.update_idletasks()  # Ensure real-time UI update

def extract_links(url, selected_types, log_func):
    """Extract selected file type links from a given URL."""
    try:
        log_func(f"Connecting to {url}...\n")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)

        # Retrieve the file types selected using .get() on IntVar()
        file_extensions = tuple(f".{ftype}" for ftype in selected_types if selected_types[ftype].get())

        extracted_links = [
            urljoin(url, link['href']) for link in links
            if link['href'].lower().endswith(file_extensions)
        ]

        log_func(f"Found {len(extracted_links)} files in {url}.\n")
        return extracted_links
    except requests.RequestException as e:
        log_func(f"Error fetching {url}: {e}\n")
        return []

def process_websites(input_file, output_file, selected_types, log_func, update_progress, update_time_remaining):
    """Read websites from the input file, extract links based on selected types, and save to output file."""
    global is_paused, stop_thread
    if not os.path.isfile(input_file):
        log_func(f"Error: The input file '{input_file}' does not exist.\n")
        return

    log_func(f"Reading URLs from {input_file}...\n")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            websites = [line.strip() for line in f if line.strip()]
    except UnicodeDecodeError:
        log_func("Error: Unable to read the input file with UTF-8 encoding.\n")
        return

    all_links = []
    total_urls = len(websites)
    start_time = time.time()

    for i, website in enumerate(websites):
        while is_paused:
            time.sleep(0.1)
            if stop_thread:
                return

        if stop_thread:
            return

        log_func(f"Processing {i + 1}/{total_urls}: {website}\n")
        links = extract_links(website, selected_types, log_func)
        all_links.extend(links)

        # Update progress and remaining time estimate
        update_progress(i + 1, total_urls)
        elapsed_time = time.time() - start_time
        avg_time_per_task = elapsed_time / (i + 1)
        remaining_time = avg_time_per_task * (total_urls - (i + 1))
        update_time_remaining(remaining_time)

    # Remove duplicates
    unique_links = list(set(all_links))

    log_func(f"Saving {len(unique_links)} unique links to {output_file}...\n")
    with open(output_file, 'w', encoding='utf-8') as f:
        for link in unique_links:
            f.write(f"{link}\n")

    log_func(f"Links have been successfully saved to {output_file}.\n")
    update_progress(total_urls, total_urls)  # Set progress bar to 100%
    update_time_remaining(0)  # Reset time remaining to 0

    # Save log to a file
    with open(f"{output_file}.log", 'w', encoding='utf-8') as log_file:
        log_file.write(log_textbox.get("1.0", tk.END))

def start_extraction_thread(input_file, output_file, selected_types, log_func, update_progress, update_time_remaining):
    """Run the extraction process in a separate thread to avoid blocking the UI."""
    global stop_thread
    stop_thread = False
    thread = threading.Thread(
        target=process_websites,
        args=(input_file, output_file, selected_types, log_func, update_progress, update_time_remaining),
        daemon=True
    )
    thread.start()

def start_extraction():
    """Start the extraction process with selected file, output path, and file types."""
    input_file = input_file_entry.get()
    output_file = output_file_entry.get()
    if not input_file or not output_file:
        messagebox.showerror("Input Error", "Please select an input file and specify an output file.")
        return

    log_textbox.delete(1.0, tk.END)  # Clear log box before starting

    # Pass the actual IntVar() objects instead of their values
    selected_types = {ftype: var for ftype, var in file_types.items()}

    def update_progress(completed, total):
        progress_var.set(completed / total * 100)
        progress_bar.update()

    def update_time_remaining(seconds):
        if seconds > 0:
            mins, secs = divmod(int(seconds), 60)
            time_label.config(text=f"Estimated Time Remaining: {mins} min {secs} sec")
        else:
            time_label.config(text="Estimated Time Remaining: 0 sec")

    start_extraction_thread(input_file, output_file, selected_types, log_func, update_progress, update_time_remaining)

def pause_extraction():
    """Pause the extraction process."""
    global is_paused
    is_paused = not is_paused
    if is_paused:
        pause_button.config(text="Resume")
    else:
        pause_button.config(text="Pause")

def select_input_file():
    """Open a file dialog to select the input .txt file."""
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        input_file_entry.delete(0, tk.END)
        input_file_entry.insert(0, file_path)

def select_output_file():
    """Open a file dialog to specify the output file location."""
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, file_path)

# Create the main window with a dark theme
window = ThemedTk(theme="equilux")
window.title("File Link Extractor")
window.geometry("650x550")

# Dark color styles
dark_bg = "#2E2E2E"
light_text = "#FFFFFF"
accent_color = "#FF6347"

style = ttk.Style(window)
style.configure('TButton', background=dark_bg, foreground=light_text, padding=6, relief='flat', font=('Helvetica', 10))
style.configure('TLabel', background=dark_bg, foreground=light_text, font=('Helvetica', 10))
style.configure('TEntry', fieldbackground=dark_bg, foreground=light_text, relief='flat')
style.configure('TText', background=dark_bg, foreground=light_text, highlightbackground=dark_bg, highlightcolor=accent_color)
style.configure('TCheckbutton', background=dark_bg, foreground=light_text, font=('Helvetica', 10))
style.configure('TProgressbar', troughcolor=dark_bg, background=accent_color)

# Configure grid layout
window.columnconfigure(1, weight=1)
window.configure(background=dark_bg)

# File type selection checkboxes
file_types_label = ttk.Label(window, text="Select File Types:")
file_types_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

file_types = {
    'rar': tk.IntVar(),
    'zip': tk.IntVar(),
    'tar': tk.IntVar(),
    'gz': tk.IntVar(),
    '7z': tk.IntVar(),
    'docx': tk.IntVar(),
    'xlsx': tk.IntVar(),
    'pdf': tk.IntVar()
}

row_count = 1
for ftype, var in file_types.items():
    checkbutton = ttk.Checkbutton(window, text=ftype.upper(), variable=var)
    checkbutton.grid(row=row_count, column=0, sticky=tk.W, padx=10, pady=5)
    row_count += 1

# Input file selection
input_label = ttk.Label(window, text="Input File (.txt):")
input_label.grid(row=row_count, column=0, sticky=tk.W, padx=10, pady=10)
input_file_entry = ttk.Entry(window, width=50)
input_file_entry.grid(row=row_count, column=1, padx=10, pady=10, sticky=tk.W + tk.E)
input_file_button = ttk.Button(window, text="Browse", command=select_input_file)
input_file_button.grid(row=row_count, column=2, padx=10, pady=10)

# Output file selection
row_count += 1
output_label = ttk.Label(window, text="Output File (.txt):")
output_label.grid(row=row_count, column=0, sticky=tk.W, padx=10, pady=10)
output_file_entry = ttk.Entry(window, width=50)
output_file_entry.grid(row=row_count, column=1, padx=10, pady=10, sticky=tk.W + tk.E)
output_file_button = ttk.Button(window, text="Browse", command=select_output_file)
output_file_button.grid(row=row_count, column=2, padx=10, pady=10)

# Start and Pause buttons
row_count += 1
start_button = ttk.Button(window, text="Start Extraction", command=start_extraction)
start_button.grid(row=row_count, column=1, padx=10, pady=10, sticky=tk.E)

pause_button = ttk.Button(window, text="Pause", command=pause_extraction)
pause_button.grid(row=row_count, column=2, padx=10, pady=10, sticky=tk.W)

# Progress bar
row_count += 1
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(window, variable=progress_var, maximum=100)
progress_bar.grid(row=row_count, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W + tk.E)

# Time remaining label
row_count += 1
time_label = ttk.Label(window, text="Estimated Time Remaining: 0 sec")
time_label.grid(row=row_count, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W)

# Log display
row_count += 1
log_label = ttk.Label(window, text="Log:")
log_label.grid(row=row_count, column=0, sticky=tk.NW, padx=10, pady=10)
log_textbox = tk.Text(window, height=10, wrap='word', font=('Helvetica', 10))
log_textbox.grid(row=row_count, column=1, columnspan=2, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)

# Allow vertical and horizontal expansion by configuring grid weights
window.grid_rowconfigure(row_count, weight=1)
window.grid_columnconfigure(1, weight=1)

# Start the main loop
window.mainloop()
