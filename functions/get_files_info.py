import os


def get_files_info(working_directory: str, directory: str | None = None) -> str:

    base_path = os.path.abspath(working_directory)
    work_path = os.path.abspath(
        os.path.join(base_path, directory if directory is not None else ".")
    )

    if not work_path.startswith(base_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory\n'

    if not os.path.isdir(work_path):
        return f'Error: "{directory}" is not a directory'

    output: list[str] = []
    for file in os.listdir(work_path):
        try:
            file_path = os.path.join(work_path, file)
            size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)

            output.append(f"- {file}: file_size={size}, is_dir={is_dir}\n")

        except OSError as err:
            return f"Error: unable to get {file} data: {err}"

    if len(output) == 0:
        return f"{directory} is empty"

    return "".join(output)
