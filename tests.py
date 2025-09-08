from functions.run_python_file import run_python_file

if __name__ == "__main__":
    print("main.py:\n", run_python_file("calculator", "main.py"))
    print("main.py with args:\n", run_python_file("calculator", "main.py", ["3 + 5"]))
    print("tests.py:\n", run_python_file("calculator", "tests.py"))
    print("../main.py:\n", run_python_file("calculator", "../main.py"))
    print("nonexistent.py:\n", run_python_file("calculator", "nonexistent.py"))
