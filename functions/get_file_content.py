import os
from config import MAX_CHARS_READ

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath("./")
        target_file_dir = os.path.normpath(os.path.join(working_dir_abs, working_directory))
        target_file = os.path.normpath(os.path.join(target_file_dir, file_path))

        valid_target_file = os.path.commonpath([target_file_dir, target_file]) == target_file_dir

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        file_content_string = ""

        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS_READ)

            if f.read(1):
                file_content_string += f'[...File "{target_file}" truncated at {MAX_CHARS_READ} characters]'

        return file_content_string

    except Exception as e:
        return f'Error: {e}'
