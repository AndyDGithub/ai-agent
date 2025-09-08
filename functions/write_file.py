import os 
from google import genai

def write_file(working_directory, file_path, content):
    try:
        # Crée le chemin absolu vers le dossier cible
        target_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory = os.path.abspath(working_directory)

        # Vérifie que le chemin cible est bien dans le dossier de travail
        if not target_path.startswith(working_directory):
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
        
        # Vérifie que le chemin cible cible existe, si non le créer
        if not os.path.exists(target_path):
            with open("exemple.txt", "w") as fichier:
                fichier.write(" ")

        with open(target_path, 'w', encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"
    

schema_write_file = genai.types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The file_path to overwrite or create and write, relative to the working directory. If not provided, it crash",
            ),
            "content": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The content to write in the file, relative to the working directory. If not provided, it write noting and delete previous content",
            ),
        },
    ),
)