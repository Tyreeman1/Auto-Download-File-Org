# 📁 Automatic File Organizer

A Python script that automatically monitors your Downloads folder and organizes files into a hierarchical folder structure based on filename keywords and file types. No more messy Downloads folder!

## ✨ Features

- **Automatic Monitoring**: Continuously watches your Downloads folder and organizes files as soon as they're downloaded
- **Smart Organization**: Files are organized by:
  - **Filename keywords** (Work, Personal, School, Invoices, etc.) → Main folders
  - **File type** (Documents, Images, Videos, etc.) → Subfolders
- **Hierarchical Structure**: Creates organized main folders with type-specific subfolders
- **Duplicate Handling**: Automatically renames duplicate files instead of overwriting
- **Customizable**: Easy to add your own categories, keywords, and folder structures
- **Real-time Feedback**: Shows you exactly what's being organized as it happens

## 📋 Requirements

- Python 3.7 or higher
- `watchdog` library

## 🚀 Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/file-organizer.git
   cd file-organizer
   ```

2. **Install required dependencies:**
   ```bash
   pip install watchdog
   ```
   
   Or on Mac/Linux:
   ```bash
   pip3 install watchdog
   ```

## 💻 Usage

1. **Run the script:**
   ```bash
   python organize_files.py
   ```
   
   Or on Mac/Linux:
   ```bash
   python3 organize_files.py
   ```

2. **Choose whether to organize existing files** when prompted

3. **Leave it running!** The script will continue monitoring and organizing new downloads automatically

4. **To stop:** Press `Ctrl + C` in the terminal

## 📂 Folder Structure

The script creates the following organization structure:

```
Downloads/
├── Work/
│   ├── Documents/      (PDFs, Word docs, spreadsheets, presentations)
│   ├── Images/         (JPG, PNG, GIF, etc.)
│   └── Other/
├── Personal/
│   ├── Documents/
│   ├── Images/
│   ├── Videos/
│   └── Other/
├── Invoices/
│   ├── PDFs/
│   ├── Images/
│   └── Other/
├── Screenshots/
│   └── Images/
├── School/
│   ├── Documents/
│   ├── PDFs/
│   └── Other/
└── General/            (Files not matching any keywords)
    ├── Images/
    ├── PDFs/
    ├── Word Documents/
    ├── Spreadsheets/
    ├── Presentations/
    ├── Text Files/
    ├── Videos/
    ├── Audio/
    ├── Archives/
    ├── Code/
    ├── Installers/
    └── Other/
```

## ⚙️ Customization

### Adding New Main Categories

Edit the `MAIN_CATEGORIES` dictionary in the script:

```python
MAIN_CATEGORIES = {
    "YourCategory": {
        "keywords": ["keyword1", "keyword2", "keyword3"],
        "subfolders": ["Documents", "Images", "Other"]
    },
}
```

### Adding File Types

Edit the `FILE_TYPES` dictionary to recognize new file extensions:

```python
FILE_TYPES = {
    "Your File Type": [".ext1", ".ext2", ".ext3"],
}
```

### Changing the Monitored Folder

By default, the script monitors your Downloads folder. To change this, edit the `DOWNLOADS_FOLDER` variable:

```python
DOWNLOADS_FOLDER = str(Path.home() / "Downloads")  # Change to your desired folder
```

## 🎯 How It Works

1. **File Detection**: Uses the `watchdog` library to monitor the Downloads folder for new files
2. **Keyword Matching**: Checks if the filename contains any keywords from `MAIN_CATEGORIES`
3. **File Type Recognition**: Identifies the file type based on its extension
4. **Smart Placement**: 
   - If keywords match → File goes to Main Category/Subfolder (e.g., `Work/Documents/`)
   - If no keywords match → File goes to General/FileType (e.g., `General/PDFs/`)
5. **Automatic Organization**: Moves the file to the appropriate location instantly

## 🛠️ Troubleshooting

### "pip is not recognized"
- Make sure Python is added to your system PATH
- Try using `py -m pip install watchdog` instead

### Script runs but files aren't organized
- Ensure the terminal window stays open
- Check that your browser downloads to the Downloads folder
- Verify you're downloading to the correct monitored folder

### Files go to "Other" instead of correct categories
- Check that the file extension is listed in `FILE_TYPES`
- Add the extension if it's missing

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with Python's `watchdog` library for file system monitoring
- Inspired by the need for a cleaner Downloads folder

## 📧 Contact

If you have questions or suggestions, feel free to open an issue!

---

**⭐ If you find this useful, please consider giving it a star on GitHub!**
