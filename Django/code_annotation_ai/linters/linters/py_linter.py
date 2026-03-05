import ast, json, subprocess

def check_python_syntax(file_path):
    try:
        with open(file_path, "r") as f:
            source = f.read()
        
        # Attempt parsing
        ast.parse(source)
        return None

    except SyntaxError as e:
        # Clean the code: remove tabs and newlines, normalize spaces
        annotation = {
            "file": e.filename,
            "line": e.lineno,
            "type": e.msg,
            "original_code": source,
            "suggested_fix": None,
            "explanation": []
        }

        return json.dumps(annotation)
    
def flake_checker(file_path):
    cmd = ["flake8", file_path, "--format=json"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    print(result.stdout)

    return json.loads(result.stdout)
    
print(flake_checker("C:\\Users\\natar\\Desktop\\shit.py"))
        