# move_files.py

import shutil
import os

source_file = "/Users/sergali/Desktop/git/practisePP2/practise1/python_basic/PractisePP2/lab6/file_handling/sample.txt"
destination_dir = "test_dir"

if os.path.exists(source_file):
    shutil.move(source_file, destination_dir)
    print("File moved successfully.")
else:
    print("Source file not found.")