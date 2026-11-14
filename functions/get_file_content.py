import os
from config import MAX_CHARS_READ

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns the content of the provided file or up to config.MAX_CHARS_READ characters from it.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The name of the file to be opened, it can be a file in the working directory or be prefixed with a relative path to the working directory.)",
                },
            },
        },
    },
}
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
