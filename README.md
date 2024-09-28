# File Link Extractor

This Python-based application extracts links from multiple websites and saves them to a text file. It supports various file types (e.g., `.rar`, `.zip`, `.tar`, `.gz`, `.7z`, `.docx`, `.xlsx`, `.pdf`), and features a user-friendly graphical user interface (GUI) with real-time logging, a progress bar, and pause/resume functionality.

## Features

- **Support for Multiple File Types**: You can select which file types to extract using checkboxes in the GUI. Supported file types include:
  - `.rar`, `.zip`, `.tar`, `.gz`, `.7z`
  - `.docx`, `.xlsx`, `.pdf`
  
- **Real-time Logging**: 
  - A log box in the GUI shows real-time logs of the extraction process. It logs connection attempts, the number of files found, errors, and completion messages.
  - The log is continuously updated, and users can see the progress of the extraction process in real-time as each website is processed.

- **Saving Logs**: 
  - Upon completion, the logs from the real-time logging box are saved in a `.log` file with the same name as the output file (but with a `.log` extension). This allows users to review the details of the extraction process at a later time.

- **Pause/Resume Functionality**: 
  - The application allows users to pause and resume the extraction process at any time with a single button click. When paused, the extraction process will wait until resumed.

- **Progress Bar and Time Estimation**: 
  - The application includes a progress bar that visually represents the extraction progress as websites are processed.
  - It also shows an estimated remaining time to complete the task, which is dynamically updated during the extraction.

- **Dark-Themed GUI**: 
  - The user interface is styled with a dark theme, providing a modern and visually comfortable experience. It uses the `ttkthemes` library to ensure consistency in the appearance.

## Installation

### Prerequisites
- Python 3.7 or higher
- The following Python libraries are required:
  - `requests`
  - `beautifulsoup4`
  - `ttkthemes`
  - `tkinter`

You can install the required libraries using `pip`:

```bash
pip install requests beautifulsoup4 ttkthemes
```

### Running the Application

1. Download or clone this repository.
2. Ensure you have the required Python libraries installed.
3. Run the `main.py` file:

```bash
python main.py
```

## How to Use

1. **Input File**: 
   - Prepare a `.txt` file with the list of website URLs, one URL per line.
   - Click the **Browse** button next to the **Input File** field to select the `.txt` file containing the URLs.

2. **Output File**: 
   - Select the location where the extracted links will be saved.
   - Click the **Browse** button next to the **Output File** field to specify the output file (with `.txt` extension).

3. **Select File Types**:
   - Use the checkboxes to select which types of files you want to extract (e.g., `.rar`, `.zip`, `.docx`, etc.).

4. **Start Extraction**:
   - Click the **Start Extraction** button to begin processing.
   - The real-time log box will display the current progress, and the progress bar will update as websites are processed.

5. **Pause/Resume**:
   - During extraction, you can click the **Pause** button to pause the process.
   - Click **Resume** (the button will toggle) to continue the extraction from where it was paused.

6. **Completion**:
   - Once the extraction is complete, the extracted links will be saved to the output file you specified.
   - Additionally, a log file with the extraction details will be saved in the same directory as the output file, with a `.log` extension.

### Example:

- If you provided `output_links.txt` as the output file, you will also find a `output_links.txt.log` file that contains the detailed logs of the extraction process.

## GUI Overview

- **Input File**: Select a `.txt` file containing the list of URLs.
- **Output File**: Specify the name of the file where the extracted links will be saved.
- **File Type Checkboxes**: Choose which file types to search for on the websites.
- **Start Extraction Button**: Starts the extraction process.
- **Pause Button**: Pauses or resumes the extraction process.
- **Progress Bar**: Shows the current progress of the extraction.
- **Estimated Time Remaining**: Displays how much time is left for the extraction to complete.
- **Log Box**: Displays real-time log messages during the extraction process.

## File Types Supported

The following file types can be selected for extraction:

- **Archive files**: `.rar`, `.zip`, `.tar`, `.gz`, `.7z`
- **Document files**: `.docx`, `.xlsx`, `.pdf`

## Real-time Logging and Error Handling

The application provides real-time feedback via a log box. It logs the following types of information:

- **Connection attempts**: When trying to connect to a website.
- **Number of files found**: How many files of the selected types were found on each website.
- **Errors**: If there is a connection error, a broken URL, or other issues.
- **Completion messages**: When the process is done for each website and for the entire process.

## Pause and Resume Feature

While the extraction is running, you can pause the process using the **Pause** button. This allows the user to temporarily halt the extraction and later resume from where they left off. The button toggles between **Pause** and **Resume** to indicate the current action.

## Saving Logs

After the extraction process is complete, the content of the log box is saved into a `.log` file, making it easy to review the extraction history and any errors that occurred.

## Contributions

If you’d like to contribute to the project by improving the functionality or adding new features, feel free to submit a pull request. We appreciate all contributions.

---

## Contact

For any issues, suggestions, or feedback, feel free to open an issue in the GitHub repository or contact me via:

- GitHub: [sajious](https://github.com/sajious)
- Email: sajedyousefi.sy@gmail.com

---
