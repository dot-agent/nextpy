"""Script to remove `__pycache__` and empty directories from a specified path.
Useful for post-test cleanups and maintaining a tidy workspace.
"""

import os
import shutil


def remove_pycache_and_empty_dirs(path: str):
    """Removes `__pycache__` folders and empty directories from the given path.

    Args:
        path (str): Directory path to clean up.
    """
    for root, dirs, _files in os.walk(path, topdown=False):
        # Remove `__pycache__` and empty directories
        for dir in dirs:
            if dir == '__pycache__':
                shutil.rmtree(os.path.join(root, dir))
        if not os.listdir(root) and root != path:
            os.rmdir(root)

if __name__ == "__main__":
    current_directory = os.getcwd()
    remove_pycache_and_empty_dirs(current_directory)
    print("Cleanup completed.")
