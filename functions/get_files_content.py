import os
import readline
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        full_file_dir = os.path.normpath(os.path.join(abs_working_dir, file_path))
        valid_dir = os.path.commonpath([abs_working_dir, full_file_dir]) == abs_working_dir

        if not valid_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(full_file_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(full_file_dir, "r") as f:
        
            file_contents = f.read(MAX_CHARS)
            if f.read(1):
                file_contents += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
                
        return file_contents

    except Exception as e:
        return f'Error reading file "{file_path}": {e}'


schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the first 10000 characters present in a file, and mentions whether the output was truncated or not if the file has more than 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the file from which content is to be fetched.",
            ),
        },
    ),
)