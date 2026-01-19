import os
import shutil
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# === CONFIGURATION ===
# The folder to monitor (your Downloads folder)
DOWNLOADS_FOLDER = str(Path.home() / "Downloads")

# Define file type categories (these will be subfolders within main categories)
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "PDFs": [".pdf"],
    "Documents": [".doc", ".docx"],
    "Spreadsheets": [".xlsx", ".xls", ".csv"],
    "Presentations": [".ppt", ".pptx"],
    "Text Files": [".txt"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".json"],
    "Installers": [".exe", ".dmg", ".pkg", ".deb", ".msi"],
"Revit Files": [".rvt", ".rfa"],
"CAD Files": [".dwg", ".bak", ".pcp", ".stl"]
}

# Main category rules based on filename keywords
# Files matching these keywords go into main folders, then subfolders by file type
MAIN_CATEGORIES = {
    "RTA_WORK_FILES": {
        "keywords": ["PLAN", "project", "meeting", "client", "rta", "st", "ave", "springfield", "new bedford", "fall river", "floor plan", "floor plans", "elevations", "exist" "existing", "demo", "proposed", "street", "window", "door", "wall", "family", "profile", "furniture", "accessory", "hvac"],
        "subfolders": ["Documents", "Images", "PDFs", "Spreadsheets", "Presentations", "Text Files", "Videos", "Audio", "Archives", "Code", "Installers", "Revit Files", "CAD Files"]  # Subfolders within Work
    },
    "FDC": {
        "keywords": ["FDC", "freeman", "design", "freeman design company"],
        "subfolders": ["Documents", "Images", "PDFs", "Spreadsheets", "Presentations", "Text Files", "Videos", "Audio", "Archives", "Code", "Installers", "Revit Files", "CAD Files"]
    },
    "DUNWOODY": {
        "keywords": ["dunwoody", "edu", "floor plan", "floor plans", "assignment", "presentation", "tf", "arch", "elevation", "map", "light", "Buford"],
        "subfolders": ["Documents", "Images", "PDFs", "Spreadsheets", "Presentations", "Text Files", "Videos", "Audio", "Archives", "Code", "Installers", "Revit Files", "CAD Files"]
    },
    "Screenshots": {
        "keywords": ["screenshot", "screen shot", "capture"],
        "subfolders": ["Images"]  # Screenshots are usually just images
    },
  "TIMESHEETS": {
        "keywords": ["timesheet", "rta"],
        "subfolders": ["PDFs", "Spreadsheets"]
    },
}

# Files that don't match any main category go here, organized by file type
GENERAL_FOLDER = "General"

def create_folder_structure(base_path):
    """Create all main folders and their subfolders"""
    # Create main category folders with subfolders
    for category, settings in MAIN_CATEGORIES.items():
        category_path = os.path.join(base_path, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
        
        # Create subfolders within each main category
        for subfolder in settings["subfolders"]:
            subfolder_path = os.path.join(category_path, subfolder)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
    
    # Create General folder with file type subfolders
    general_path = os.path.join(base_path, GENERAL_FOLDER)
    if not os.path.exists(general_path):
        os.makedirs(general_path)
    
    # Create file type subfolders in General
    for file_type in FILE_TYPES.keys():
        type_path = os.path.join(general_path, file_type)
        if not os.path.exists(type_path):
            os.makedirs(type_path)
    
    # Create "Other" subfolder in General for unrecognized types
    other_path = os.path.join(general_path, "Other")
    if not os.path.exists(other_path):
        os.makedirs(other_path)

def get_file_type(file_extension):
    """Get the file type category based on extension"""
    file_extension = file_extension.lower()
    for file_type, extensions in FILE_TYPES.items():
        if file_extension in extensions:
            return file_type
    return "Other"

def get_main_category(filename):
    """Check if filename matches any main category keywords"""
    filename_lower = filename.lower()
    for category, settings in MAIN_CATEGORIES.items():
        for keyword in settings["keywords"]:
            if keyword.lower() in filename_lower:
                return category
    return None

def get_subfolder_for_file_type(main_category, file_type):
    """Determine which subfolder the file type belongs in for a given main category"""
    if main_category is None:
        # Files go to General/[FileType]
        return file_type
    
    # Get the available subfolders for this main category
    available_subfolders = MAIN_CATEGORIES[main_category]["subfolders"]
    
    # Map file types to document categories
    if file_type in ["PDFs", "Word Documents", "Spreadsheets", "Presentations", "Text Files"]:
        if "Documents" in available_subfolders:
            return "Documents"
        elif "PDFs" in available_subfolders and file_type == "PDFs":
            return "PDFs"
    
    # Check if the file type is directly available as a subfolder
    if file_type in available_subfolders:
        return file_type
    
    # Check for Images, Videos, Audio
    if file_type in available_subfolders:
        return file_type
    
    # Default to "Other" if available
    if "Other" in available_subfolders:
        return "Other"
    
    # Fallback
    return available_subfolders[0] if available_subfolders else "Other"

def organize_file(file_path):
    """Organize a single file into the appropriate folder structure"""
    try:
        # Wait to ensure file is fully downloaded
        time.sleep(1)
        
        if not os.path.exists(file_path):
            return
        
        if os.path.isdir(file_path):
            return
        
        filename = os.path.basename(file_path)
        file_extension = os.path.splitext(filename)[1]
        
        # Determine main category based on filename
        main_category = get_main_category(filename)
        
        # Determine file type
        file_type = get_file_type(file_extension)
        
        # Determine the destination path
        if main_category:
            # File matches a main category (Work, Personal, etc.)
            subfolder = get_subfolder_for_file_type(main_category, file_type)
            destination_folder = os.path.join(DOWNLOADS_FOLDER, main_category, subfolder)
            path_display = f"{main_category}/{subfolder}"
        else:
            # File goes to General folder, organized by file type
            destination_folder = os.path.join(DOWNLOADS_FOLDER, GENERAL_FOLDER, file_type)
            path_display = f"{GENERAL_FOLDER}/{file_type}"
        
        # Create destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        
        destination_path = os.path.join(destination_folder, filename)
        
        # Handle duplicate filenames
        if os.path.exists(destination_path):
            base_name = os.path.splitext(filename)[0]
            extension = os.path.splitext(filename)[1]
            counter = 1
            
            while os.path.exists(destination_path):
                new_filename = f"{base_name}_{counter}{extension}"
                destination_path = os.path.join(destination_folder, new_filename)
                counter += 1
        
        # Move the file
        shutil.move(file_path, destination_path)
        print(f"✓ Organized: {filename} → {path_display}/")
        
    except Exception as e:
        print(f"✗ Error organizing {file_path}: {e}")

class DownloadHandler(FileSystemEventHandler):
    """Handles file system events"""
    
    def on_created(self, event):
        """Called when a file is created/downloaded"""
        if not event.is_directory:
            file_path = event.src_path
            if os.path.dirname(file_path) == DOWNLOADS_FOLDER:
                print(f"New file detected: {os.path.basename(file_path)}")
                organize_file(file_path)

def organize_existing_files():
    """Organize files that are already in Downloads folder"""
    print("Organizing existing files...\n")
    file_count = 0
    
    for filename in os.listdir(DOWNLOADS_FOLDER):
        file_path = os.path.join(DOWNLOADS_FOLDER, filename)
        if os.path.isfile(file_path):
            organize_file(file_path)
            file_count += 1
    
    print(f"\nOrganized {file_count} existing files.\n")

def start_monitoring():
    """Start monitoring the Downloads folder"""
    # Create folder structure
    create_folder_structure(DOWNLOADS_FOLDER)
    
    print("📁 Folder structure created:\n")
    print("Main Categories (based on filename keywords):")
    for category, settings in MAIN_CATEGORIES.items():
        print(f"  - {category}/")
        for subfolder in settings["subfolders"]:
            print(f"      └─ {subfolder}/")
    print(f"\n  - {GENERAL_FOLDER}/ (for files not matching keywords)")
    for file_type in FILE_TYPES.keys():
        print(f"      └─ {file_type}/")
    print(f"      └─ Other/\n")
    
    # Ask if user wants to organize existing files
    response = input("Do you want to organize existing files in Downloads? (yes/no): ")
    if response.lower() == "yes":
        organize_existing_files()
    
    print(f"🔍 Now monitoring: {DOWNLOADS_FOLDER}")
    print("Files will be automatically organized as you download them.")
    print("Press Ctrl+C to stop monitoring.\n")
    
    # Set up the file system observer
    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, DOWNLOADS_FOLDER, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping file organizer...")
        observer.stop()
    
    observer.join()
    print("File organizer stopped.")

# === RUN THE SCRIPT ===
if __name__ == "__main__":
    print("=== Automatic File Organizer v2 ===\n")
    start_monitoring()