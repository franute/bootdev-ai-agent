import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes (runs) a python file especified as parameter (with optional params), returning the output of it.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The name of the file to be executed (run), it can be a file in the working directory or be prefixed with a relative path to the working directory.)",
                },
                "args": {
                    "type": "array[str]",
                    "description": "Optional list of arguments to pass to the specified python file when this is executed/run.",
                },
            },
        },
    },
}
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath("./")
        target_file_dir = os.path.normpath(os.path.join(working_dir_abs, working_directory))
        target_file = os.path.normpath(os.path.join(target_file_dir, file_path))

        valid_target_file = os.path.commonpath([target_file_dir, target_file]) == target_file_dir

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        result_list : list[str] = []

        if not args is None:
           command.extend(args)

        completed_process_status = subprocess.run(command, cwd=target_file_dir,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, timeout=30)

        if completed_process_status.returncode != 0:
            return f"Process exited with code {completed_process_status.returncode}"

        if completed_process_status.stdout is None and completed_process_status.stderr is None:
            return "No output produced"

        result_list.append(f"STDOUT: {completed_process_status.stdout}")
        result_list.append(f"STDERR: {completed_process_status.stderr}")

        return "\n".join(result_list)

    except Exception as e:
        return f"Error: executing Python file: {e}"
