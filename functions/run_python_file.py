import os
import subprocess
from google import genai

def run_python_file(working_directory, file_path, args=[]):
    try:
        # Crée le chemin absolu vers le fichier cible
        target_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory = os.path.abspath(working_directory)

        # Vérifie que le fichier est bien dans le dossier de travail
        if not target_path.startswith(working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # Vérifie que le fichier existe
        if not os.path.exists(target_path):
            return f'Error: File "{file_path}" not found.'
        
        # Vérifie que le fichier est bien un fichier Python
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Prépare la commande à exécuter
        command = ["python3", target_path] + args

        # Exécute le fichier avec un timeout de 30 secondes
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_directory
        )

        output = []
        if completed.stdout:
            output.append("STDOUT:\n" + completed.stdout)
        if completed.stderr:
            output.append("STDERR:\n" + completed.stderr)
        if completed.returncode != 0:
            output.append(f"Process exited with code {completed.returncode}")
        if not output:
            return "No output produced."

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = genai.types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The file_path to run, relative to the working directory. If needs to be a .py file",
            ),
        },
    ),
)