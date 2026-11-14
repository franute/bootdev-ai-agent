import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes some text into a specific file, building the intermediate folders if they don't exist.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The name of the file to be written to, it can be a file in the working directory or be prefixed with a relative path to the working directory.)",
                },
                "content": {
                    "type": "string",
                    "description": "The text content to be written to the file"
                }
            },
        },
    },
}
def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath("./")
        target_file_dir = os.path.normpath(os.path.join(working_dir_abs, working_directory))
        target_file = os.path.normpath(os.path.join(target_file_dir, file_path))

        valid_target_file = os.path.commonpath([target_file_dir, target_file]) == target_file_dir

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(target_file_dir, exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'
