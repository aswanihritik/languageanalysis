import os

DEFAULT_IGNORE = {".git", "__pycache__", "node_modules"}


def _walk(path, ignorelist=None):
    """Recursively walks the directory and returns all files."""
    if ignorelist is None:
        ignorelist = DEFAULT_IGNORE

    files = []
    try:
        subfolder = [x for x in os.scandir(path)]
    except PermissionError:
        return files  # Skip folders without permission

    for i in subfolder:
        if i.is_dir() and i.name not in ignorelist:
            files.extend(_walk(i.path, ignorelist))
        elif i.is_file():
            files.append(i)
    return files


def _get_extension(name):
    """Extracts the file extension, returns 'no_ext' if none."""
    parts = name.rsplit(".", 1)
    return parts[-1].lower() if len(parts) > 1 else "no_ext"


def analyze_directory(path, ignorelist=None):
    """
    Analyzes the directory and returns:
      - total size per extension
      - percentage usage per extension
    """
    files = _walk(path, ignorelist)
    extension_sizes = {}

    for f in files:
        ext = _get_extension(f.name)
        extension_sizes[ext] = extension_sizes.get(ext, 0) + os.path.getsize(f.path)

    total_size = sum(extension_sizes.values())

    extension_percentages = {
        ext: round((size / total_size) * 100, 2) for ext, size in extension_sizes.items()
    }

    return {
        "sizes": extension_sizes,
        "percentages": extension_percentages,
        "total_size": total_size,
    }
