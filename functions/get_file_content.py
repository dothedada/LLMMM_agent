import os
from google.genai import types
from app.config import FILE_MAX_LENGTH


def get_file_content(working_directory: str, file_path: str) -> str:

    base_path = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not file_path.startswith(base_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(file_path, "r") as data:
        try:
            file = data.read(FILE_MAX_LENGTH)

            if len(file) == FILE_MAX_LENGTH:
                file += f'[...File "{file_path}" truncated at 10000 characters]'

            return file

        except Exception as err:
            return f'Error: cannot read file "{file_path}": {err}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to the file that we want to retrive the data, relative to the working directory.",
            ),
        },
    ),
)
