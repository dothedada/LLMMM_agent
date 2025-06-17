import os


def write_file(working_directory, file_path, content):
    base_path = os.path.abspath(working_directory)
    work_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not work_path.startswith(base_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    base_dir = os.path.dirname(work_path)
    print("base_dir", base_dir)

    if not os.path.exists(base_dir):
        try:
            os.makedirs(base_dir)
        except Exception as err:
            return f'Error: cannot make folders to path "{work_path}": {err}'

    with open(work_path, "w") as file:
        try:
            file.write(content)
            return f'Successfully wrote to "{work_path}" ({len(content)} characters written)'
        except Exception as err:
            return f'Error: cannot write data into "{work_path}": {err}'
