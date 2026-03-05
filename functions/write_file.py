import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        full_file_dir = os.path.normpath(os.path.join(abs_working_dir, file_path))
        valid_dir = os.path.commonpath([abs_working_dir, full_file_dir]) == abs_working_dir

        if not valid_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(full_file_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(full_file_dir), exist_ok=True)

        with open(full_file_dir, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"
    
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content into a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to write the content to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written into the file.",
            ),
        },
    ),
)