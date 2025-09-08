import os
from functions.config import MAX_FILE_CHARACTERS
from google import genai

def get_file_content(working_directory, file_path):
    try:
        # Crée le chemin absolu vers le dossier cible
        target_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory = os.path.abspath(working_directory)

        # Vérifie que le chemin cible est bien dans le dossier de travail
        if not target_path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Vérifie que le chemin cible est bien un dossier
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Lecture du contenu du fichier
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Troncature si nécessaire
        if len(content) > MAX_FILE_CHARACTERS:
            content = content[:MAX_FILE_CHARACTERS] + f'\n[...File "{file_path}" truncated at {MAX_FILE_CHARACTERS} characters]'

        return content

    except Exception as e:
        return f"Error: {str(e)}"
    

schema_get_file_content = genai.types.FunctionDeclaration(
    name="get_file_content",
    description="Read file content",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The file_path to read, relative to the working directory. If not provided, it crash",
            ),
        },
    ),
)