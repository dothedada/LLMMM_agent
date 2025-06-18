from google.genai import types
from google.genai.types import FunctionCall

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file

functions = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(function_call: FunctionCall, verbose: bool = False) -> types.Content:

    # NOTE: revisar que no haya problema al llamar el content sin parametro
    # if not function_call.name or not function_call.args:
    #     return types.Content(
    #         role="tool",
    #         parts=[
    #             types.Part.from_function_response(
    #                 name="no params",
    #                 response={
    #                     "error": f"No params given: function -> {function_call.name}, args -> {function_call.args}"
    #                 },
    #             )
    #         ],
    #     )

    function_name = function_call.name
    function_args = function_call.args
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function = functions.get(function_name)
    if not function:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    function_result: str = function("./calculator", **function_call.args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name, response={"result": function_result}
            )
        ],
    )
