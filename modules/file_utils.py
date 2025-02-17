# modules/file_utils.py 
import os
from pathlib import Path
import fnmatch
import logging

def read_file(filepath):
    """Reads the content of a file, returning it as a string."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            logging.debug(f"Read file: {filepath}")
            return content
    except OSError as e:
        logging.warning(f"Error reading {filepath}: {e}")
        return ""

def collect_files(root_dir, ignored_dirs, other_exts, necessary_files, code_exts):
    """
    Collects Python and other relevant files from the project directory.
    
    Returns:
        tuple: (list_of_code_files, list_of_other_files)
    """
    code_files = []
    other_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Ignore specified directories using pattern matching
        dirnames[:] = [d for d in dirnames if not any(fnmatch.fnmatch(d, pattern) for pattern in ignored_dirs)]
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root_dir)
            ext = Path(filename).suffix.lower()

            if ext in code_exts:
                code_files.append(rel_path)
            elif ext in other_exts or filename.lower() in necessary_files:
                other_files.append(rel_path)

    logging.info(f"Collected {len(code_files)} code files and {len(other_files)} other files.")
    return code_files, other_files

def collect_folder_structure(root_dir, ignored_dirs):
    """
    Collects the folder structure of the project.
    
    Returns:
        dict: A dictionary representing the folder structure.
    """
    folder_structure = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Ignore specified directories
        dirnames[:] = [d for d in dirnames if not any(fnmatch.fnmatch(d, pattern) for pattern in ignored_dirs)]
        rel_dir = os.path.relpath(dirpath, root_dir)
        folder_structure[rel_dir] = {
            'subdirectories': dirnames,
            'files': filenames
        }
    logging.info("Collected folder structure.")
    return folder_structure
import os
import logging

def get_ignored_dirs(root_dir, config_ignore_list):
    """
    Returns a set of directory ignore patterns.
    
    If a .gitignore file is present in the project root, this function parses it and extracts
    directory patterns (lines ending with '/'). Otherwise, it falls back to the list provided in
    config.yaml.
    
    Args:
        root_dir (str): The root directory of the project.
        config_ignore_list (list): The list of directory patterns from config.yaml to ignore.
    
    Returns:
        set: A set of directory patterns that should be ignored.
    """
    gitignore_path = os.path.join(root_dir, '.gitignore')
    patterns = []
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f.readlines():
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    # If the pattern ends with '/', we treat it as a directory exclusion.
                    if line.endswith('/'):
                        pattern = line.rstrip('/')
                        patterns.append(pattern)
        except Exception as e:
            logging.warning(f"Error reading .gitignore: {e}. Using config.yaml ignore list instead.")
            patterns = config_ignore_list
    else:
        patterns = config_ignore_list
    return set(patterns)