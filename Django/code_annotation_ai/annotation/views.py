from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from linters.linters.py_linter import *
from code_annotation_ai.settings import BASE_DIR

import ollama, json
import os


# Initialize the Ollama client
ollama_client = ollama.Client()


@csrf_exempt
def predict(request):
    test_file = (BASE_DIR / "annotation" / "views.py")

    if request.method != 'POST':
        return render(request, "send.html")

    # Get input (if needed)
    message = request.POST.get('input')

    # Run linters
    file_path = test_file
    base_py_syntax_result = check_python_syntax(file_path)
    base_pylint_result = flake_checker(file_path)

    # Build list of errors
    all_errors = []

    # Syntax errors
    if base_py_syntax_result:
        syntax_errors = json.loads(base_py_syntax_result)
        if isinstance(syntax_errors, list):
            all_errors.extend(syntax_errors)
        else:
            all_errors.append(syntax_errors)

    # Lint errors
    for fpath, errors in base_pylint_result.items():
        for e in errors:
            broken_func = get_broken_function(fpath, e["line_number"])
            all_errors.append({
                "file": e["filename"],
                "line": e["line_number"],
                "type": e["code"],
                "original_code": broken_func,
                "suggested_fix": None,
                "explanation": []
            })

    # Send each error to Ollama individually to avoid hallucinations
    
    prompt = f"""
        Input data:
        {json.dumps(all_errors)}
        """
        
    annotation = ollama_client.generate(
        model="qwen2.5-coder:7b",
        system="""
            You are an AI assistant that fixes Python code syntax and lint errors.
            Return output **only in JSON**, strictly following this schema:

            {{
                "file": "<file where error occurred>",
                "line": "<line number of error>",
                "type": "<error type>",
                "original_code": "<the code that caused the error>",
                "suggested_fix": "<corrected code>",
                "explanation": [
                    "<short explanation 1>",
                    "<short explanation 2>",
                    "<short explanation 3>"
                ]
            }}
            
            
            Rules:
            - Only return valid JSON.
            - Do NOT include any text outside the JSON.
            - Include at least 3 explanations per error.
            - Fix the code exactly.
            - Only produce the JSON object, nothing else.
        """,
        prompt=prompt
    )
    
    raw = annotation.response.strip()

    data = all_errors  # default if AI parsing fails

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # fallback if model returned multiple objects
        raw = raw.lstrip("[{").rstrip("}]")
        raw = "{" + raw + "}"
        try:
            data = json.loads(raw)
        except Exception as e:
            print("Failed to parse AI response:", e)
            # data is already assigned to all_errors

        return JsonResponse(data, safe=False)


def get_broken_function(file_path, error_line):
    """Return only the function that contains the error line."""
    if not os.path.exists(file_path):
        return ""

    with open(file_path, "r") as f:
        lines = f.readlines()

    # Find the start of the function
    start = error_line - 1
    while start > 0 and not lines[start].strip().startswith("def "):
        start -= 1

    # Find the end of the function
    end = start + 1
    while end < len(lines) and not lines[end].strip().startswith("def "):
        end += 1

    snippet = "".join(lines[start:end])
    return snippet