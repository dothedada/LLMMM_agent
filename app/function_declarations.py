from google.genai import types


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


schema_get_files_content = types.FunctionDeclaration(
    name="get_files_content",
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


schema_run_python = types.FunctionDeclaration(
    name="run_python",
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


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the content into a file or overwrite the content if the file already exists, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to the file that we want to create or overwrite, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The data that we want to put into the file",
            ),
        },
    ),
)


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        # schema_get_files_content,
        # schema_run_python,
        # schema_write_file,
    ]
)
