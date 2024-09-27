import os
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from urllib.parse import urljoin
import threading
import time

# Function to extract .rar links from a given URL
def extract_rar_links(url, log_func):
    """Extract all .rar links from a given URL."""
    try:
        log_func(f"Connecting to {url}...\n")
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        rar_links = [urljoin(url, link['href']) for link in links if link['href'].lower().endswith('.rar')]
        log_func(f"Found {len(rar_links)} .rar links in {url}.\n")
        return rar_links
    except requests.RequestException as e:
        log_func(f"Error fetching {url}: {e}\n")
        return []

# Function to process the websites and extract .rar links
def process_websites(input_file, output_file, log_func, update_progress, update_time_remaining):
    """Read the websites from the input file, extract links, and save to output file."""
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

    all_rar_links = []
    total_urls = len(websites)
    start_time = time.time()

    for i, website in enumerate(websites):
        log_func(f"Processing {i + 1}/{total_urls}: {website}\n")
        rar_links = extract_rar_links(website, log_func)
        all_rar_links.extend(rar_links)

        # Update progress and remaining time estimate
        update_progress(i + 1, total_urls)
        elapsed_time = time.time() - start_time
        avg_time_per_task = elapsed_time / (i + 1)
        remaining_time = avg_time_per_task * (total_urls - (i + 1))
        update_time_remaining(remaining_time)

    # Remove duplicates
    unique_rar_links = list(set(all_rar_links))

    log_func(f"Saving {len(unique_rar_links)} unique .rar links to {output_file}...\n")
    with open(output_file, 'w', encoding='utf-8') as f:
        for link in unique_rar_links:
            f.write(f"{link}\n")

    log_func(f"RAR download links have been successfully saved to {output_file}.\n")
    update_progress(total_urls, total_urls)  # Set progress bar to 100%
    update_time_remaining(0)  # Reset time remaining to 0

# Wrapper function to handle threading
def start_extraction_thread(input_file, output_file, log_func, update_progress, update_time_remaining):
    """Run the extraction process in a separate thread to avoid blocking the UI."""
    threading.Thread(target=process_websites, args=(input_file, output_file, log_func, update_progress, update_time_remaining), daemon=True).start()

# Function that handles the start of extraction from the UI
def start_extraction():
    """Start the extraction process with selected file and output path."""
    input_file = input_file_entry.get()
    output_file = output_file_entry.get()
    if not input_file or not output_file:
        messagebox.showerror("Input Error", "Please select an input file and specify an output file.")
        return

    log_textbox.delete(1.0, tk.END)  # Clear log box before starting
    
    # Define a function to log messages in the Text widget
    def log_func(text):
        log_textbox.insert(tk.END, text)
        log_textbox.see(tk.END)  # Auto scroll to the end
    
    # Function to update progress bar
    def update_progress(completed, total):
        progress_var.set(completed / total * 100)
        progress_bar.update()
    
    # Function to update remaining time display
    def update_time_remaining(seconds):
        if seconds > 0:
            mins, secs = divmod(int(seconds), 60)
            time_label.config(text=f"Estimated Time Remaining: {mins} min {secs} sec")
        else:
            time_label.config(text="Estimated Time Remaining: 0 sec")

    # Start the extraction process in a new thread
    start_extraction_thread(input_file, output_file, log_func, update_progress, update_time_remaining)

# Function to select the input file from file dialog
def select_input_file():
    """Open a file dialog to select the input .txt file."""
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        input_file_entry.delete(0, tk.END)
        input_file_entry.insert(0, file_path)

# Function to select the output file location from file dialog
def select_output_file():
    """Open a file dialog to specify the output file location."""
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, file_path)

# Create the main window
window = tk.Tk()
window.title("RAR Link Extractor")

# Configure grid layout
window.columnconfigure(1, weight=1)

# Input file selection
tk.Label(window, text="Input File (.txt):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
input_file_entry = tk.Entry(window, width=50)
input_file_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
input_file_button = tk.Button(window, text="Browse", command=select_input_file)
input_file_button.grid(row=0, column=2, padx=5, pady=5)

# Output file selection
tk.Label(window, text="Output File (.txt):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
output_file_entry = tk.Entry(window, width=50)
output_file_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
output_file_button = tk.Button(window, text="Browse", command=select_output_file)
output_file_button.grid(row=1, column=2, padx=5, pady=5)

# Start button
start_button = tk.Button(window, text="Start Extraction", command=start_extraction, bg='lightblue')
start_button.grid(row=2, column=1, pady=10)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(window, variable=progress_var, maximum=100)
progress_bar.grid(row=3, column=1, pady=5, sticky=tk.W + tk.E)

# Time remaining label
time_label = tk.Label(window, text="Estimated Time Remaining: 0 sec")
time_label.grid(row=4, column=1, pady=5, sticky=tk.W)

# Log display
tk.Label(window, text="Log:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
log_textbox = tk.Text(window, height=15, width=70)
log_textbox.grid(row=5, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)

# Start the main loop
window.mainloop()
