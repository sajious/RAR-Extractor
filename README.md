# RAR Link Extractor with GUI

## Overview

The **RAR Link Extractor** is a Python-based application that allows users to extract `.rar` download links from a list of websites. The application features a graphical user interface (GUI) built using `Tkinter`, providing an intuitive, user-friendly experience. It supports multithreading, ensuring the UI remains responsive while processing tasks in the background. Additionally, it provides real-time progress tracking, task estimation, and detailed logging.

### Key Features:
- **Multithreaded Operation**: The extraction process runs in the background, preventing the UI from freezing.
- **Progress Tracking**: A progress bar displays the percentage of URLs processed.
- **Estimated Time Remaining**: A real-time display of how much time is left to complete the task.
- **Detailed Logging**: Logs are updated with real-time status updates, showing the number of URLs processed, errors encountered, and results of the extraction.
- **Error Handling**: Robust error handling for network issues, invalid files, and other unexpected errors.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Requirements
Before running the application, ensure you have the following dependencies installed:

- **Python 3.x**
- **Requests**: for handling HTTP requests
- **BeautifulSoup4**: for parsing HTML content
- **Tkinter**: (comes pre-installed with Python)
- **Threading**: for non-blocking UI updates
- **TTK**: for progress bar widgets in the UI

You can install the required packages via `pip`:

```bash
pip install requests beautifulsoup4
```

## Usage

1. **Run the Application**:
   To launch the GUI, run the following command:
   ```bash
   python RAR-Extractor.py
   ```

2. **Input File**:  
   - Prepare a `.txt` file containing a list of website URLs, each on a new line.
   - Use the "Browse" button to select your input `.txt` file.

3. **Output File**:  
   - Specify the output `.txt` file where the extracted `.rar` links will be saved.
   - Click "Browse" to select the output location.

4. **Start Extraction**:
   - Click "Start Extraction" to begin the process.
   - The log window will show real-time progress, including the number of URLs processed and any errors encountered.
   - A progress bar tracks the percentage of tasks completed.
   - An estimated time remaining will be shown based on the processing speed.

### Example Input File (`websites.txt`):
```
http://example.com/page1
http://example.com/page2
http://another-site.com/downloads
```

### Output File:
- All extracted `.rar` links will be saved in the specified output file, one per line.

## How It Works

### Multithreading
The extraction process runs in a separate thread to ensure that the main GUI thread, responsible for user interactions, remains responsive. This allows users to view the progress, cancel the operation, or close the window without any delays or freezes.

### Progress Tracking & Time Estimation
- **Progress Bar**: Updates as each URL is processed, showing the percentage completion of the task.
- **Time Remaining**: The average time per task is calculated dynamically, and the remaining time is estimated and updated regularly.

### Error Handling
Each URL is processed independently, so if an error occurs (e.g., a URL is unreachable or invalid), it is logged, and the program continues to the next URL without interruption.

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository.
2. Create a new branch with your feature or bug fix:  
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:  
   ```bash
   git commit -m 'Add some feature'
   ```
4. Push to the branch:  
   ```bash
   git push origin feature-name
   ```
5. Open a pull request on GitHub.


---

## Future Enhancements

Here are some ideas for additional features or improvements that could be added to the project:

- **Progress Export**: Save the progress log to a file for further review.
- **Support for Other File Types**: Extend the extractor to support `.zip` or other file formats.
- **Pause/Resume**: Add the ability to pause and resume the extraction process.
- **UI Enhancements**: Improve the interface with more advanced features like dark mode or custom themes.

---

## Contact

For any issues, suggestions, or feedback, feel free to open an issue in the GitHub repository or contact me via:

- GitHub: [sajious](https://github.com/sajious)
- Email: sajedyousefi.sy@gmail.com

---
