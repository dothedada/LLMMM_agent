import subprocess
from google.genai import types
import os


def run_python_file(working_directory: str, file_path: str) -> str:
    base_path = os.path.abspath(working_directory)
    work_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not work_path.startswith(base_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(work_path):
        return f'Error: File "{file_path}" not found.'

    _, extension = os.path.splitext(work_path)
    if extension != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        output = subprocess.run(
            ["python3", work_path],
            timeout=30,
            capture_output=True,
            cwd=base_path,
        )

        output_element: list[str] = []
        if output.stdout:
            output_element.append(f"STDOUT: {output.stdout.decode()}")
        if output.stderr:
            output_element.append(f"\nSTDERR: {output.stderr.decode()}")
        if output.returncode != 0:
            output_element.append(f"\nProcess exited with code {output.returncode}")

        return "\n".join(output_element) if output_element else "No output produced."

    except Exception as err:
        return f"Error: executing Python file: {err}"


schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file in the specified folder, constrined to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to the file that we want to execute, relative to the working directory.",
            ),
        },
    ),
)
