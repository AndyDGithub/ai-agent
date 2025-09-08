import os
from google import genai

def get_files_info(working_directory, directory="."):
    try:
        # Crée le chemin absolu vers le dossier cible
        target_path = os.path.abspath(os.path.join(working_directory, directory))
        working_directory = os.path.abspath(working_directory)

        # Vérifie que le chemin cible est bien dans le dossier de travail
        if not target_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Vérifie que le chemin cible est bien un dossier
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'

        # Liste les fichiers et dossiers
        entries = os.listdir(target_path)
        result_lines = []

        for entry in entries:
            entry_path = os.path.join(target_path, entry)
            is_dir = os.path.isdir(entry_path)
            try:
                size = os.path.getsize(entry_path)
            except OSError as e:
                size = "unknown"
            result_lines.append(f'- {entry}: file_size={size} bytes, is_dir={is_dir}')

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: {str(e)}"


schema_get_files_info = genai.types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "directory": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)