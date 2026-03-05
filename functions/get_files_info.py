import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        full_target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
        valid_dir = os.path.commonpath([abs_working_dir, full_target_dir]) == abs_working_dir

        if not valid_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(directory):
            f'Error: "{directory}" is not a directory'

        contents = ""
        for i in os.listdir(full_target_dir):
            contents += f" - {i}: file_size={os.path.getsize(os.path.join(full_target_dir, i))}, is_dir={os.path.isdir(os.path.join(full_target_dir, i))}\n"
        
        return contents

    except Exception as e:
        return f"Error: {e}"

    

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)