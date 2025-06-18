from google.genai import types
from functions.get_files_info import schema_get_files_info

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        # schema_get_files_content,
        # schema_run_python,
        # schema_write_file,
    ]
)
