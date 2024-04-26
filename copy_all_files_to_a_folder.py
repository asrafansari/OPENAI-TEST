import os
import shutil

# Define the source and destination directories
source_dir = os.environ.get('REPO_NAME')  # Replace with your repository's path
destination_dir = f"{os.environ.get('REPO_NAME')}-copied"   # Replace with your desired destination path

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# List of allowed file extensions
code_extensions = ['.py', '.js', '.java', '.dart', '.c', '.cpp', '.h', '.html', '.css', '.php', '.rb', '.go', '.swift']

# Function to add a comment with the original file path
def add_comment_with_path(file_path, original_path):
    # Check if the file has a recognized code file extension
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension not in code_extensions:
        return  # Skip non-code files

    # Define the comment based on the file extension
    comment_syntax = {
        '.py': '#',
        '.js': '//',
        '.java': '//',
        '.dart': '//',
        '.c': '//',
        '.cpp': '//',
        '.h': '//',
        '.html': '<!--',
        '.css': '/*',
        '.php': '<?php //',
        '.rb': '#',
        '.go': '//',
        '.swift': '//'
        # Add more file extensions and comment syntaxes as needed
    }

    comment_char = comment_syntax.get(file_extension, '#')  # Default to '#' if extension not found

    # Read the original file content
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Add the path comment and a newline at the beginning of the content
    content.insert(0, f"{comment_char} File Path: {original_path}\n\n")

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(content)

# Function to move and annotate files
def move_and_annotate_files(current_dir, destination_dir):
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            # Construct the original file path
            original_file_path = os.path.join(root, file)

            # Construct the new file path
            new_file_path = os.path.join(destination_dir, file)
            file_extension = os.path.splitext(original_file_path)[1].lower()

            if file_extension not in code_extensions:
                continue
            # Move the file to the destination directory
            shutil.copy(original_file_path, new_file_path)

            # Add a comment with the original file path
            add_comment_with_path(new_file_path, original_file_path)

# Call the function to move and annotate files
move_and_annotate_files(source_dir, destination_dir)

# Print a success message
print(f"All code files from directories and subdirectories have been moved to {destination_dir} and annotated with their original paths.")