from google.genai import types
import os


def get_files_info(working_directory: str, directory: str | None = None) -> str:

    base_path = os.path.abspath(working_directory)
    work_path = base_path

    if directory:
        work_path = os.path.abspath(os.path.join(working_directory, directory))

    if not work_path.startswith(base_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory\n'

    if not os.path.isdir(work_path):
        return f'Error: "{directory}" is not a directory'

    try:
        output: list[str] = []
        for file in os.listdir(work_path):
            file_path = os.path.join(work_path, file)
            size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)

            output.append(f"- {file}: file_size={size}, is_dir={is_dir}\n")

        return "\n".join(output)

    except Exception as err:
        return f"Error listing the files: {err}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
